from django.shortcuts import render, get_object_or_404
from main.models import Order, Product, OrderProduct

def track_view(request):
    return render(request, 'track/tracking.html')

def track(request, order_id=1):  # รับค่า order_id
    user = request.user  # ดึงข้อมูลผู้ใช้ที่ล็อกอินอยู่
    order = get_object_or_404(Order, pk=order_id, user=user)  # ดึงข้อมูล Order ที่ตรงกับ order_id และผู้ใช้ที่ล็อกอินอยู่
    orderproducts = OrderProduct.objects.filter(order=order)  # ดึงข้อมูล OrderProduct ที่เกี่ยวข้องกับ Order นี้
    products = Product.objects.filter(orderproduct__order=order)  # ดึงข้อมูลสินค้าอื่นๆ ที่เกี่ยวข้องกับ Order นี้
    all_products = Product.objects.all()
    return render(request, 'tracking1.html', {'order': order, 'orderproducts': orderproducts, 'products': products , 'all_products': all_products})  # ส่งข้อมูลไปแสดงผลที่ tracking1.html