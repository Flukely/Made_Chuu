from django.shortcuts import render, get_object_or_404, redirect
from main.models import *
from django.db.models import Avg

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product_id=product.product_id)
    reviews_avg = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'product_detail.html', {"product": product,"reviews": reviews,"average_rating": reviews_avg})

def add_cart(request , product_id):
    request.session['user_id'] = 17
    product = get_object_or_404(Product, product_id=product_id)
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect ('login')
    
    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user_id=user_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product , quantity=quantity)

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    cart.save()
    
    return redirect('product_detail',product_id)