from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from main.models import Cart, Product, User, Order, OrderProduct, CartItem, Shop, StatusOrder
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db import transaction

@login_required(login_url='/login/')
def AddCart(request):
    user_id = request.session.get('user_id')
    request.session['user_id'] = user_id

    detail_product = Product.objects.all()
    detail_cart = Cart.objects.filter(user_id=user_id)
    detail_user = User.objects.filter(user_id=user_id)
    detail_cartitem = CartItem.objects.filter(cart__user_id=user_id).select_related('product__shop')

    # คำนวณราคาสินค้าในตะกร้า (รวมโปรโมชั่น)
    for item in detail_cartitem:
        promotion = item.product.promotionproduct_set.first()
        if promotion:
            discount = promotion.promotion_id.discount / 100
            item.calculated_total_price = item.quantity * (item.product.price * (1 - discount))
            item.original_total_price = item.quantity * item.product.price
            item.has_promotion = True
        else:
            item.calculated_total_price = item.quantity * item.product.price
            item.original_total_price = item.calculated_total_price
            item.has_promotion = False

    return render(request, 'AddCart.html', {
        "detail_cart": detail_cart,
        "detail_product": detail_product,
        "detail_user": detail_user,
        "detail_cartitem": detail_cartitem,
    })

@login_required(login_url='/login/')
def Confirm_Cart(request):
    user_id = request.session.get('user_id')
    
    try:
        selected_items = json.loads(request.POST.get('selected_items', '[]'))
    except json.JSONDecodeError:
        selected_items = []

    if not selected_items:
        messages.error(request, "กรุณาเลือกสินค้าที่ต้องการชำระเงิน")
        return redirect('Cart:AddCart')

    # ตรวจสอบว่าสินค้าทั้งหมดมาจากร้านเดียวกัน
    shop_ids = set()
    detail_cartitem = []
    total_price = 0

    for item_id in selected_items:
        try:
            item = CartItem.objects.get(id=item_id, cart__user_id=user_id)
            # คำนวณราคาสำหรับแต่ละรายการ
            promotion = item.product.promotionproduct_set.first()
            if promotion:
                discount = promotion.promotion_id.discount / 100
                item.calculated_total_price = item.quantity * (item.product.price * (1 - discount))
                item.original_total_price = item.quantity * item.product.price
            else:
                item.calculated_total_price = item.quantity * item.product.price
                item.original_total_price = item.calculated_total_price
            
            detail_cartitem.append(item)
            shop_ids.add(item.product.shop.shop_id)
            total_price += item.calculated_total_price
        except CartItem.DoesNotExist:
            continue

    if len(shop_ids) > 1:
        messages.error(request, "ไม่สามารถสั่งซื้อสินค้าจากร้านค้าหลายร้านในคำสั่งซื้อเดียวกันได้")
        return redirect('Cart:AddCart')

    try:
        detail_user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        messages.error(request, "ไม่พบข้อมูลผู้ใช้")
        return redirect('Cart:AddCart')
    
    return render(request, 'Confirm_Cart.html', {
        "detail_cartitem": detail_cartitem,
        "total_price": total_price,
        "user_name": detail_user.user_name,
        "address": detail_user.address,
        "district": detail_user.district,
        "province": detail_user.province,
        "postal_code": detail_user.postal_code,
        "phone_number": detail_user.phone_num,
        "selected_items_json": json.dumps([item.id for item in detail_cartitem]),
    })

@login_required(login_url='/login/')
def delete(request, id):
    try:
        cart_item = CartItem.objects.get(id=id, cart__user_id=request.session.get('user_id'))
        cart_item.delete()
    except CartItem.DoesNotExist:
        messages.error(request, "ไม่มีสินค้าในตะกร้า")
    return redirect('Cart:AddCart')

@csrf_exempt
@login_required(login_url='/login/')
def place_order(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'User not logged in'}, status=401)

    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        total_price = data.get('total_price', 0)
        
        if not items:
            return JsonResponse({'success': False, 'message': 'ไม่มีสินค้าที่เลือก'})

        # ตรวจสอบว่าสินค้าทั้งหมดมาจากร้านเดียวกัน
        shop_ids = set()
        for item in items:
            try:
                product = Product.objects.get(product_id=item['product_id'])
                shop_ids.add(product.shop.shop_id)
            except Product.DoesNotExist:
                continue

        if len(shop_ids) > 1:
            return JsonResponse({'success': False, 'message': 'ไม่สามารถสั่งซื้อสินค้าจากร้านค้าหลายร้านในคำสั่งซื้อเดียวกันได้'})

        with transaction.atomic():
            user = User.objects.get(user_id=user_id)
            shop = Shop.objects.get(shop_id=shop_ids.pop())

            # ตรวจสอบและสร้างสถานะคำสั่งซื้อหากไม่มี
            status_order, created = StatusOrder.objects.get_or_create(
                status_name="รอจ่ายเงิน",
                defaults={'status_name': "รอจ่ายเงิน"}
            )

            order = Order.objects.create(
                user=user,
                total_price=total_price,
                place_delivery=user.address,
                shop=shop,
                status_order=status_order,
                shipper=None,
                tracking_num='',
                delivery_date=None
            )

            for item in items:
                product = Product.objects.get(product_id=item['product_id'])
                quantity = int(item['quantity'])
                
                if product.quantity < quantity:
                    raise ValueError(f"จำนวนสินค้า {product.product_name} ไม่เพียงพอ")
                
                product.quantity -= quantity
                product.save()
                
                OrderProduct.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                    discount=product.promotionproduct_set.first().promotion_id.discount if product.promotionproduct_set.first() else 0
                )

            # ลบสินค้าที่เลือกในตะกร้า
            item_ids = [item['product_id'] for item in items]
            CartItem.objects.filter(cart__user_id=user_id, product_id__in=item_ids).delete()

        return JsonResponse({
            'success': True,
            'redirect_url': reverse('payment:payment', kwargs={'order_id': order.order_id})
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)