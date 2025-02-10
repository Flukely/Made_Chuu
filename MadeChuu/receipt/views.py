from django.shortcuts import render, get_object_or_404
from main.models import Receipt, OrderProduct, User, Order, Product, Shop  # นำเข้าโมเดล Shop

def index(request):
    return render(request, 'receipt.html')

def receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, pk=receipt_id)  # แก้ไขการค้นหา
    order_items = OrderProduct.objects.filter(order_id=receipt.order_id)  # ดึงรายการสินค้าในคำสั่งซื้อ
    order = get_object_or_404(Order, pk=receipt.order_id)  # ดึงข้อมูลคำสั่งซื้อ
    user = get_object_or_404(User, user_id=order.user_id)  # ดึงข้อมูลผู้ใช้
    first_item = order_items.first()
    product = get_object_or_404(Product, pk=first_item.product_id) if first_item else None
    store_name = get_object_or_404(Shop, pk=product.shop_id).shop_name if product else 'No Shop'  # ดึงชื่อร้านค้า
    
    # สร้างรายการสินค้าพร้อมราคา
    items_with_price = []
    for item in order_items:
        product = get_object_or_404(Product, pk=item.product_id)
        items_with_price.append({
            'product_name': product.product_name,  # ใช้ product_name แทน name
            'quantity': item.quantity,
            'price': product.price,
        })
    
    return render(request, 'receipt.html', {
        'receipt': receipt,
        'order_items': order_items,
        'user': user,
        'store_name': store_name,
        'items_with_price': items_with_price,  # ส่งรายการสินค้าพร้อมราคาไปยังเทมเพลต
    })