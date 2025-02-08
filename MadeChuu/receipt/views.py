from django.shortcuts import render, get_object_or_404
from main.models import Receipt, OrderProduct, User  # นำเข้าโมเดล Receipt, OrderProduct และ User

def index(request):
    return render(request, 'receipt.html')

def receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id)  # แก้ไขการค้นหา
    order_items = OrderProduct.objects.filter(order_id=receipt.order_id)  # ดึงรายการสินค้าในคำสั่งซื้อ
    user = get_object_or_404(User, user_id=receipt.order_id.user_id.user_id)  # ดึงข้อมูลผู้ใช้
    store_name = order_items.first().product_id.shop_id.shop_name if order_items.exists() else 'No Shop'  # ดึงชื่อร้านค้า
    return render(request, 'receipt.html', {'receipt': receipt, 'order_items': order_items, 'user': user, 'store_name': store_name})