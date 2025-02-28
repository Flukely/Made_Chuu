from django.http import HttpResponse
from django.shortcuts import render
from main.models import Product
import random

def product_view(request):
    products = list(Product.objects.all())  
    random.shuffle(products)  # สุ่มลำดับสินค้า
    context = {"product": products[:4]}  # ส่งแค่ 4 ชิ้นไปยัง template
    return render(request, "your_template.html", context)


def index(request):
    product = Product.objects.all()
    return render(request, 'index.html', {'product': product})