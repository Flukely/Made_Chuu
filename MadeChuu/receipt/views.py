from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Receipt, OrderProduct, Order, Payment, Product, Shop, User

@login_required(login_url='/login/')
def check_receipt(request):
    """ หน้าตรวจสอบใบเสร็จ แสดงการชำระเงินของผู้ใช้ที่ล็อกอิน """
    user_payments = Payment.objects.filter(order__user=request.user).order_by('-payment_date')
    payments_with_items = []

    for payment in user_payments:
        order_items = OrderProduct.objects.filter(order=payment.order)
        items_with_price = [
            {
                'product_name': item.product.product_name,
                'quantity': item.quantity,
                'price': item.product.price,
            }
            for item in order_items
        ]
        payments_with_items.append({
            'payment': payment,
            'items_with_price': items_with_price,
        })

    return render(request, 'check_receipt.html', {'payments_with_items': payments_with_items})

@login_required(login_url='/login/')
def receipt(request, order_id):
    """ แสดงรายละเอียดใบเสร็จ หรือแจ้งเตือนหากยังไม่มีใบเสร็จ """
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    receipt = Receipt.objects.filter(order=order).first()

    if not receipt:
        return render(request, 'receipt.html', {'message': "กำลังดำเนินการ", 'order': order})

    order_items = OrderProduct.objects.filter(order=order)
    items_with_price = [
        {
            'product_name': item.product.product_name,
            'quantity': item.quantity,
            'price': item.product.price,
        }
        for item in order_items
    ]

    store_name = order_items.first().product.shop.shop_name if order_items else "ไม่พบร้านค้า"

    return render(request, 'receipt.html', {
        'receipt': receipt,
        'order': order,
        'store_name': store_name,
        'items_with_price': items_with_price,
        'logged_in_user': request.user,
    })