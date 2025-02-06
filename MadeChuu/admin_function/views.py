from django.shortcuts import render , redirect ,get_object_or_404
from .models import Order , Product
from .filters import ProductFilter
from .forms import ProductForm

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
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ProductsAdmin')  # เปลี่ยนเป็นชื่อ URL ของหน้ารายการสินค้า
    elif 'edit_product' in request.POST:
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            edit_form = ProductForm(request.POST, request.FILES, instance=product)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('ProductsAdmin')
    else:
        form = ProductForm()
        edit_form = ProductForm()
    return render(request, "admin_function/ProductsAdmin.html", {"products":product_filter , 'form': form , 'edit_form': edit_form})
