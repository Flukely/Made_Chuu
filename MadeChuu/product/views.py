from django.shortcuts import render
from main.models import Product, Category, Shop
from .filters import ProductFilter

def product(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    product_filter = ProductFilter(request.GET, queryset=Product.objects.all())
    return render(request, 'product.html', {'filter': product_filter, categories: 'categories'})
def shop1(request):
    shop = Shop.objects.get(shop_id=1)
    products = Product.objects.filter(shop=shop)[:16]
    categories = Category.objects.all()
    return render(request, 'shop1.html', {'products': products, 'categories': categories, 'shop': shop})
def shop2(request):
    shop = Shop.objects.get(shop_id=2)
    products = Product.objects.filter(shop=shop)[:29]
    categories = Category.objects.all()
    return render(request, 'shop2.html', {'products': products, 'categories': categories, 'shop': shop})