# filepath: /c:/Users/milk/OneDrive - Naresuan University/เดสก์ท็อป/MadeChuu/MadeChuu/index/views.py
from django.shortcuts import render
from django.shortcuts import render
from main.models import Product

def index(request):
    products = Product.objects.all()
    return render(request, 'index/index.html',{ 'products': products })