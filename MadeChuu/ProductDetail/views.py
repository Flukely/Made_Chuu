from django.shortcuts import render, get_object_or_404
from main.models import Product, Review

def product_detail(request):
    product = get_object_or_404(Product, pk=1)
    reviews = get_object_or_404(Review, pk=1)
    return render(request, 'product_detail.html', {"product": product,"reviews": reviews})