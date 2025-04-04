from django.http import HttpResponse
from django.shortcuts import render
from main.models import *
import random

def index(request):
    products = list(Product.objects.all())  
    random.shuffle(products)  # สุ่มลำดับสินค้า
    context = {"product": products[:4]}  # ส่งแค่ 4 ชิ้นไปยัง template
    return render(request, 'index.html',context)