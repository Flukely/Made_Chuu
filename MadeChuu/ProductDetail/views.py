from django.shortcuts import render, get_object_or_404
from main.models import Product, Review
from django.db.models import Avg

def product_detail(request):#product_id
    product = get_object_or_404(Product, pk=1)#pk=product_id
#   product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.all()#filter(product, product_id)
    reviews_avg = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'product_detail.html', {"product": product,"reviews": reviews,"average_rating": reviews_avg})