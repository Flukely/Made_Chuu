from django.shortcuts import render, get_object_or_404
from receipt.models import Receipt  # นำเข้าโมเดล Receipt
from receipt.models import OrderProducts  # นำเข้าโมเดล OrderProducts

def index(request):
    return render(request, 'receipt.html')

def receipt(request, user_id):
    receipt = get_object_or_404(Receipt, order__user_id=user_id)  # แก้ไขการค้นหา
    order_items = OrderProducts.objects.filter(order=receipt.order)  # ดึงรายการสินค้าในคำสั่งซื้อ
    user = receipt.order.user  # ดึงข้อมูลผู้ใช้
    store_name = order_items.first().product.shop.shop_name if order_items.exists() else 'No Shop'  # ดึงชื่อร้านค้า
    return render(request, 'receipt.html', {'receipt': receipt, 'order_items': order_items, 'user': user, 'store_name': store_name})