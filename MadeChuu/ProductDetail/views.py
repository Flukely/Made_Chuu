from django.shortcuts import render, get_object_or_404
from main.models import Product

def product_detail(request):
    product = get_object_or_404(Product, pk=20)
    return render(request, 'product_detail.html', {"product": product})