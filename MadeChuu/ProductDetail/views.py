from django.shortcuts import render, get_object_or_404, redirect
from main.models import *
from django.db.models import Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

def product_detail(request):#product_id
    product = get_object_or_404(Product, pk=17)#pk=product_id
#   product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product_id=product.product_id)#filter(product, product_id)
    reviews_avg = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'product_detail.html', {"product": product,"reviews": reviews,"average_rating": reviews_avg})

@login_required(login_url='login')
def add_cart(request, product_id):
    try:
        product = get_object_or_404(Product, product_id=product_id)
        user_id = request.session.get('user_id')

        if not user_id:
            messages.error(request, "You need to be logged in to add items to the cart.")
            return redirect('login')

        quantity = int(request.POST.get('quantity', 1))
        logger.info(f"Adding product {product_id} with quantity {quantity} to cart for user {user_id}")

        cart, created = Cart.objects.get_or_create(user_id=user_id, defaults={'total_price': 0})
        logger.info(f"Cart created: {created}, Cart ID: {cart.id}")

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        logger.info(f"CartItem created: {created}, CartItem ID: {cart_item.id}")

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        logger.info(f"CartItem saved with quantity {cart_item.quantity}")

        # Update total price in the cart
        cart.total_price += product.price * quantity
        cart.save()
        logger.info(f"Cart total price updated to {cart.total_price}")

        messages.success(request, "Item added to cart successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        messages.error(request, f"An error occurred: {e}")
    
    return redirect('product_detail')