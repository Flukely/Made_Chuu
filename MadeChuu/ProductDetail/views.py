from django.shortcuts import render, get_object_or_404
from main.models import Product, Review
import json

def product_detail(request):
    product = get_object_or_404(Product, pk=1)
    reviews = Review.objects.all()
    reviews_avg = Review.objects.all()
    return render(request, 'product_detail.html', {"product": product,"reviews": reviews})