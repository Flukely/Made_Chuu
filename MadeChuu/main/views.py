from django.shortcuts import render
from .models import Order , OrderProducts
def index(request):
    return render(request, 'admin/index.html')

def ChatAdmin(request):
    return render(request , "admin/ChatsAdmin.html")

def OrderAdmin(request):
    #Query from model Order
    data = Order.objects.all()
    return render(request , "admin/OrderAdmin.html" , {'Orders':data})

def Dashboard(request):
    return render(request , "admin/Dashboard.html")

def ProductAdmin(request):
    return render(request , "admin/ProductsAdmin.html")

def PromotionsAdmin(request):
    return render(request , "admin/PromotionsAdmin.html")

def CommentAdmin(request):
    return render(request , "admin/CommentAdmin.html")