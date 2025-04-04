from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from main.models import Cart, Product, User, Order, OrderProduct , CartItem , Shop, StatusOrder , PromotionProduct
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def AddCart(request ):
    user_id = request.session.get('user_id')
    request.session['user_id'] = user_id
   
    detail_product = Product.objects.all()
    detail_cart = Cart.objects.filter(user_id=user_id)  
    detail_user = User.objects.filter(user_id=user_id)
    detail_cartitem = CartItem.objects.filter(cart__user_id=user_id).select_related('product__shop')
  
    for item in detail_cartitem:
        promotion = item.product.promotionproduct_set.first()
        if promotion and promotion.promotion_id and promotion.promotion_id.discount:
            discount = promotion.promotion_id.discount
            discounted_price = item.product.price * (1 - discount / 100)
            item.total_price = item.quantity * discounted_price
        else:
            item.total_price = item.quantity * item.product.price
    item.save()

    return render(request, 'AddCart.html', {
        "detail_cart": detail_cart,
        "detail_product": detail_product,
        "detail_user": detail_user,
        "detail_cartitem": detail_cartitem ,
       
    })

def Confirm_Cart(request):                     #หน้ายืนยันการสั่งซื้อ
    user_id = request.session.get('user_id')
    
    detail_product = Product.objects.all()
    detail_cart = Cart.objects.all()
    detail_user = User.objects.filter(user_id=user_id)
    detail_cartitem = CartItem.objects.all()
    
    return render(request, 'Confirm_Cart.html', {
        "detail_cart": detail_cart,
        "detail_product": detail_product,
        "detail_user": detail_user ,
        "detail_cartitem": detail_cartitem
    })

def delete(request, id):                  #ลบสินค้าในตะกร้า อันนี้ปุ่มลบนะในหน้า AddCart
    try:
        cart_item = CartItem.objects.get(id=id)   
        cart_item.delete()
        message = "ลบสินค้าเรียบร้อยแล้ว"
    except CartItem.DoesNotExist: 
        raise Http404("ไม่มีสินค้าในตะกร้า")
    return redirect('Cart:AddCart')

@csrf_exempt
def place_order(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        order_data = json.loads(request.POST.get('order_data'))
        print(order_data)
        items = order_data.get('items', [])
        total_price = order_data.get('total_price', 0)
        if not items:
            return JsonResponse({'success': False, 'message': 'ไม่มีสินค้าที่เลือก'})

        user = User.objects.get(user_id=user_id)
        
        for item in items:
            product = Product.objects.get(product_id=item['product_id'])
            shop_id = product.shop.shop_id  # Assuming a ForeignKey relationship
            shop_instance = product.shop
            break
        
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            place_delivery=user.address,
            shop=shop_instance,
            status_order= StatusOrder.objects.get(status_name="รอจ่ายเงิน"),
            shipper=None,
            tracking_num='',
            delivery_date=None
        )
        

        for item in items:
            product = Product.objects.get(product_id=item['product_id'])
            # Convert item['quantity'] to an integer
            quantity_to_subtract = int(item['quantity'])
            if product.quantity >= quantity_to_subtract:
                product.quantity -= quantity_to_subtract
                product.save()
                OrderProduct.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity_to_subtract
                )
            else:
                 raise ValueError("จำนวนสินค้าไม่เพียงพอ")

        # ลบสินค้าที่เลือกในฐานข้อมูล
        item_ids = [item['product_id'] for item in items]
        CartItem.objects.filter(cart__user_id=user_id, product_id__in=item_ids).delete()

        return redirect('payment:payment')
    return redirect('payment:payment')
   

@csrf_exempt          
def delete_cart_items(request):                   #กดสั่งซื้อสินค้าแล้วลบสินค้าในตะกร้าที่เลือกไว้
    if request.method == 'POST':
        data = json.loads(request.body)
        items = data.get('items', [])

        if items:  
            item_ids = [item['id'] for item in items]  
            CartItem.objects.filter(id__in=item_ids).delete()  

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)
