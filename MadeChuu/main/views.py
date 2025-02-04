from django.shortcuts import render
from .models import Order , OrderProducts
def index(request):
    return render(request, 'index.html')

def ChatAdmin(request):
    return render(request , "ChatsAdmin.html")

def OrderAdmin(request):
    #Query from model Order
    data = Order.objects.all()
    return render(request , "OrderAdmin.html" , {'Orders':data})

def Dashboard(request):
    return render(request , "Dashboard.html")

def ProductAdmin(request):
    return render(request , "ProductsAdmin.html")

def PromotionsAdmin(request):
    return render(request , "PromotionsAdmin.html")

def CommentAdmin(request):
    return render(request , "CommentAdmin.html")