from django.shortcuts import render, get_object_or_404
from main.models import Order, Product, OrderProduct , Shop

def track_view(request):
    user_id = request.session.get('user_id')
    order = Order.objects.filter(user_id=user_id)
    shop = Shop.objects.all()
    orderproducts = OrderProduct.objects.filter(order__in=order)
    return render(request, 'tracking.html' , {'orders': order, 'shop': shop,'orderproducts': orderproducts})

def track(request, order_id):  # รับค่า order_id
    user = request.user  # ดึงข้อมูล User ที่ login อยู่
    order = get_object_or_404(Order, pk=order_id, user=user)  # ดึงข้อมูล Order ที่ตรงกับ order_id
    orderproducts = OrderProduct.objects.filter(order=order)  # ดึงข้อมูล OrderProduct ที่เกี่ยวข้องกับ Order นี้
    products = Product.objects.filter(orderproduct__order=order)  # ดึงข้อมูลสินค้าอื่นๆ ที่เกี่ยวข้องกับ Order นี้
    all_products = Product.objects.all()
    return render(request, 'tracking1.html', {'order': order, 'orderproducts': orderproducts, 'products': products , 'all_products': all_products})  # ส่งข้อมูลไปแสดงผลที่ tracking1.html
