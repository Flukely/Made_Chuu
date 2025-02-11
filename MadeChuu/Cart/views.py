from django.shortcuts import render, redirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from main.models import Cart, Product, User, Order, OrderProduct , CartItem


def AddCart(request):
    user_id = request.session.get('user_id', 1)
    if not user_id:
        return redirect('login')  

    detail_product = Product.objects.all()
    detail_cart = Cart.objects.filter(user_id=user_id)  
    detail_user = User.objects.filter(user_id=user_id)
    detail_cartitem = CartItem.objects.filter(cart__user_id=user_id)  

    for item in detail_cartitem:
        item.total_price = item.quantity * item.product.price  

    return render(request, 'AddCart.html', {
        "detail_cart": detail_cart,
        "detail_product": detail_product,
        "detail_user": detail_user,
        "detail_cartitem": detail_cartitem 
    })

    
def Confirm_Cart(request):                     #หน้ายืนยันการสั่งซื้อ
    detail_product = Product.objects.all()
    detail_cart = Cart.objects.all()
    detail_user = User.objects.all()
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
    return redirect('AddCart')

@csrf_exempt
def place_order(request):                 #ขั้นตอนการส่งข้อมูลไปยัง Order 
    if request.method == 'POST': 
        data = json.loads(request.body)
        items = data.get('items', []) 
        total_price = data.get('total_price', 0)

        if not items:
            return JsonResponse({'success': False, 'message': 'ไม่มีสินค้าที่เลือก'})

        user = User.objects.first() 
        
        order = Order.objects.create(
            user=user,
            quantity=len(items),
            total_price=total_price,
            status_order=None, 
            place_delivery=user.address,
            shipper=None, 
            tracking_num='',
            delivery_date=None
        )
        for item in items:
            product = Product.objects.get(id=item['id']) 
            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=item['quantity']
            )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
   

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

    
    




