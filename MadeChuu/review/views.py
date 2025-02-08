from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Product, Review, OrderProducts
from .forms import ReviewForm
from django.http import JsonResponse
from django.db.models import Count

def review_page(request):
    products = Product.objects.all()
    product_orders = {}

    for product in products:
        orders = OrderProducts.objects.filter(product=product).exclude(
            order__in=Review.objects.filter(product=product).values('order')
        )
        product_orders[product] = orders

    context = {
        'product_orders': product_orders,
    }
    return render(request, 'review/review.html', context)

def submit_review(request, product_id, order_id):
    product = get_object_or_404(Product, pk=product_id)
    order = get_object_or_404(OrderProducts, product=product, order__pk=order_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.order = order.order
            review.save()
            return redirect('review_page')
    else:
        form = ReviewForm()
    return render(request, 'review/review.html', {'form': form, 'product': product, 'order': order})