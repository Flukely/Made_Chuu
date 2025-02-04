from django.shortcuts import render
from .models import Order , OrderProducts
def index(request):
    return render(request, 'index.html')

def ChatAdmin(request):
    return render(request , "ChatAdmin.html")

def OrderAdmin(request):
    #Query from model Order
    data = Order.objects.all()
    return render(request , "OrderCheckAdmin.html" , {'Orders':data})