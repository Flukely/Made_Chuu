from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Subquery
from main.models import Product, Review, OrderProduct, Order
from .forms import ReviewForm
import json

@login_required
def review_page(request):
    """ แสดงรายการสินค้าที่สามารถรีวิวได้ """
    user = request.user

    # ดึง user จาก order ของ OrderProduct
    order_user_subquery = Order.objects.filter(order_id=OuterRef('order_id')).values('user')

    # ตรวจสอบว่าออเดอร์นี้ถูกรีวิวไปแล้วหรือยัง
    reviewed_orders = Review.objects.filter(product=OuterRef('product'), order=OuterRef('order'))

    # ดึงรายการ OrderProduct ที่เป็นของผู้ใช้และยังไม่ได้รีวิว
    product_orders = (
        OrderProduct.objects
        .annotate(order_user=Subquery(order_user_subquery))
        .filter(order__user=user)  # ✅ กรอง order ที่เป็นของ user
        .annotate(is_reviewed=Exists(reviewed_orders))
        .filter(is_reviewed=False)  # ✅ กรองเฉพาะที่ยังไม่ได้รีวิว
        .select_related('product', 'order')
    )

    # 🔍 Debug: เช็คข้อมูลที่ดึงมา
    data = list(product_orders.values("order_id", "product_id", "product__product_name"))
    if not data:
        print("❌ ไม่พบสินค้าที่รีวิวได้!")

    return render(request, 'review/review.html', {'product_orders': product_orders})

@login_required
def submit_review(request, product_id, order_id):
    """ จัดการการส่งรีวิวสินค้า """
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    
    # ดึง order ที่เกี่ยวข้อง
    order_product = OrderProduct.objects.filter(
        product=product, order_id=order_id, order__user=user
    ).select_related('order').first()

    if not order_product:
        return JsonResponse({'success': False, 'message': 'Invalid order or already reviewed'})

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.order = order_product.order
            review.save()
            return JsonResponse({'success': True, 'product_id': product_id, 'order_id': order_id})

        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
