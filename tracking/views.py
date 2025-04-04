from django.shortcuts import render, get_object_or_404, redirect
from main.models import Order, Product, OrderProduct, Shop, Payment, StatusOrder, Claim, Refund
from .forms import RefundForm
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required

@login_required
def track_view(request):
    user_id = request.session.get('user_id')
    order = Order.objects.filter(user_id=user_id)
    shop = Shop.objects.all()
    orderproducts = OrderProduct.objects.filter(order__in=order)
    return render(request, 'tracking.html' , {'orders': order, 'shop': shop,'orderproducts': orderproducts})

@login_required
def track(request, order_id):  # รับค่า order_id
    user = request.user  # ดึงข้อมูล User ที่ login อยู่
    order = get_object_or_404(Order, pk=order_id, user=user)  # ดึงข้อมูล Order ที่ตรงกับ order_id
    orderproducts = OrderProduct.objects.filter(order=order)  # ดึงข้อมูล OrderProduct ที่เกี่ยวข้องกับ Order นี้
    products = Product.objects.filter(orderproduct__order=order)  # ดึงข้อมูลสินค้าอื่นๆ ที่เกี่ยวข้องกับ Order นี้
    all_products = Product.objects.all()
    if order.status_order.status_name == 'เตรียมของ' or order.status_order.status_name == 'จัดส่งสำเร็จ' or order.status_order.status_name == 'เตรียมจัดส่ง':
        payment = get_object_or_404(Payment, order=order)
    else:
        payment = None
        
    claim = Claim.objects.filter(order=order).first()    
        
    return render(request, 'tracking1.html', {'order': order, 'orderproducts': orderproducts, 'products': products , 'all_products': all_products, 'payment': payment, 'claim': claim})  # ส่งข้อมูลไปแสดงผลที่ tracking1.html

@login_required
@transaction.atomic
def cancel_order(request, order_id):
    user = request.user
    order = get_object_or_404(Order, order_id=order_id,user=user)
    if request.method == 'POST':
        if order.status_order.status_name == "เตรียมของ":
            # Get the "ยกเลิกคำสั่งซื้อ" status object
            cancel_status = get_object_or_404(StatusOrder, status_name="ยกเลิกคำสั่งซื้อ")
             # Loop through related OrderProducts
            order_products = OrderProduct.objects.filter(order=order)
            for op in order_products:
                # Return the quantity to the product
                op.product.quantity += op.quantity
                op.product.save()
           
            order.status_order = cancel_status
            order.save()
            messages.success(request, "ยกเลิกคำสั่งซื้อสำเร็จ!")
        else:
             messages.error(request, "ไม่สามารถยกเลิกคำสั่งซื้อได้ เนื่องจากสถานะคำสั่งซื้อไม่ได้อยู่ในขั้นตอนเตรียมสินค้า")

    return redirect('tracking:tracking', order_id=order_id)

@login_required
def refund_info(request, order_id):
    user = request.user
    order = get_object_or_404(Order, order_id=order_id, user=user)
    if request.method == 'POST':
        form = RefundForm(request.POST)
        if form.is_valid():
            refund = form.save(commit=False)
            refund.order = order
            refund.save()
            
            refund_status = get_object_or_404(StatusOrder, status_name="ดำเนินการคืนเงิน")
            order.status_order = refund_status
            order.save()
            
            messages.success(request, "ส่งข้อมูลการคืนเงินสำเร็จแล้ว!")
            return redirect('tracking:track_view')
    else:
        form = RefundForm()
    return render(request, 'refund_info.html', {'form': form, 'order': order})

def submit_order(request, order_id):
    user = request.user
    order = get_object_or_404(Order, order_id=order_id, user=user)
    if request.method == 'POST':
        order.status_order = get_object_or_404(StatusOrder, status_name="จัดส่งสำเร็จ")
        order.delivery_date = timezone.now()
        order.save()
        messages.success(request, "ยืนยันการรับสินค้าสำเร็จ!")
    return redirect('tracking:tracking', order_id=order_id)