from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Subquery
from main.models import Product, Review, OrderProduct, Order
from .forms import ReviewForm
import json

@login_required(login_url='/login/')
def review_page(request, order_id=None):
    """ แสดงรายการสินค้าที่สามารถรีวิวได้ โดยสามารถกรองตาม order ที่เลือก """
    user = request.user

    # ดึง order ที่มีสถานะ "จัดส่งสำเร็จ" (ปรับชื่อ status ตามที่คุณใช้จริง)
    completed_orders = Order.objects.filter(
        user=user,
        status_order__status_name="จัดส่งสำเร็จ"  # ปรับชื่อ field ตามโครงสร้างจริง
    )

    # ตรวจสอบว่าออเดอร์นี้ถูกรีวิวไปแล้วหรือยัง
    reviewed_orders = Review.objects.filter(
        product=OuterRef('product'), 
        order=OuterRef('order')
    )

    # สร้าง queryset เริ่มต้น
    product_orders_query = (
        OrderProduct.objects
        .filter(order__in=completed_orders)  # กรองเฉพาะ order ที่จัดส่งสำเร็จ
        .annotate(is_reviewed=Exists(reviewed_orders))
        .filter(is_reviewed=False)  # กรองเฉพาะที่ยังไม่ได้รีวิว
        .select_related('product', 'order')
    )

    # ถ้ามีการระบุ order_id ให้กรองเฉพาะ order นั้น
    if order_id:
        product_orders_query = product_orders_query.filter(order_id=order_id)

    product_orders = product_orders_query.all()

    # ดึงรายการออร์เดอร์ทั้งหมดของผู้ใช้เพื่อแสดงใน dropdown (เฉพาะที่จัดส่งสำเร็จ)
    user_orders = completed_orders.order_by('-order_date')

    return render(request, 'review.html', {
        'product_orders': product_orders,
        'user_orders': user_orders,
        'selected_order_id': int(order_id) if order_id else None
    })

@login_required(login_url='/login/')
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