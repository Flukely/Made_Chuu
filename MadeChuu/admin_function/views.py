from django.shortcuts import render
from .models import Order , Product
from .filters import ProductFilter

def admin_function(request):
    return render(request, 'admin_function/Dashboard.html')

def ChatAdmin(request):
    return render(request, 'admin_function/ChatsAdmin.html')

def OrderAdmin(request):
    #Query from model Order
    Order_wait_status = Order.objects.filter(status_order = "wait")
    return render(request, 'admin_function/OrderAdmin.html',{'Orders_wait': Order_wait_status})

def Dashboard(request):
    return render(request, 'admin_function/Dashboard.html')

def CommentAdmin(request):
    return render(request, 'admin_function/CommentAdmin.html')

def ProductAdmin(request):
    return render(request, 'admin_function/ProductsAdmin.html')

def PromotionsAdmin(request):
    return render(request, 'admin_function/PromotionsAdmin.html')

def product_list(request):
    product_filter = ProductFilter(request.GET, queryset=Product.objects.all())
    return render(request, "admin_function/ProductsAdmin.html", {"products":product_filter})
