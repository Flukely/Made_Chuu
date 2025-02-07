from django.shortcuts import render , redirect ,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
from .filters import ProductFilter , DeliveryFilter
from .forms import ProductForm 

def admin_function(request):
    return render(request, 'admin_function/Dashboard.html')

def ChatAdmin(request):
    return render(request, 'admin_function/ChatsAdmin.html')


def OrderAdmin(request):
    #Query from model Order
    Order_wait_status = Order.objects.filter(status_order = "wait")
    Order_confirm_status = Order.objects.filter(status_order = "confirm")
    Order_Detail = OrderProducts.objects.all()
    return render(request, 'admin_function/OrderAdmin.html',
                  {'Orders_wait': Order_wait_status , 
                   'Orders_confirm': Order_confirm_status,
                   'Order_Detail': Order_Detail})

def DeliveryAdmin(request):
    Delivery_filter = DeliveryFilter(request.GET, queryset=Delivery.objects.all())
    return render(request, 'admin_function/DeliveryAdmin.html', {"deliverys_filter": Delivery_filter})

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
    if request.method == 'POST':
        add_form = ProductForm(request.POST, request.FILES)
        if add_form.is_valid():
            add_form.save()
            return redirect('ProductsAdmin') 
    elif 'edit_product' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            edit_form = ProductForm(request.POST, request.FILES, instance=product)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('ProductsAdmin')
    else:
        add_form = ProductForm()
        edit_form = ProductForm()
    return render(request, "admin_function/ProductsAdmin.html", {"products":product_filter , 'form': add_form , 'edit_form': edit_form})
