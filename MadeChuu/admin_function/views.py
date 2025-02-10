from django.shortcuts import render , redirect ,get_object_or_404
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.admin.views.decorators import staff_member_required
from .filters import *
from .forms import ProductForm 
from main.models import *
from django.core.paginator import Paginator

def admin_function(request):
    return render(request, 'admin_function/Dashboard.html')

def ChatAdmin(request):
    return render(request, 'admin_function/ChatsAdmin.html')


def OrderAdmin(request):
    #Query from model Order
    order_filter = OrderFilter(request.GET, queryset=Order.objects.all())
    paginator = Paginator(order_filter.qs, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_function/OrderAdmin.html',{'orders':order_filter , 'page_obj': page_obj}) 

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
    else:
        add_form = ProductForm()
    return render(request, "admin_function/ProductsAdmin.html", 
                  {"products":product_filter , 
                   'form': add_form
                   })
@csrf_exempt
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('ProductsAdmin')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_function/Edit_ProductsAdmin.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    # ตรวจสอบว่าวิธีการของคำขอเป็น POST หรือไม่
    if request.method == 'POST':
        # ดึงข้อมูลสินค้าที่ต้องการลบจากฐานข้อมูล
        product = get_object_or_404(Product, product_id=product_id)
        # ลบสินค้าที่เลือก
        product.delete()
        # เปลี่ยนเส้นทางผู้ใช้กลับไปยังหน้า ProductsAdmin
        return redirect('ProductsAdmin')
    else:
        # ถ้าวิธีการของคำขอไม่ใช่ POST, เปลี่ยนเส้นทางกลับไปยังหน้า ProductsAdmin
        return redirect('ProductsAdmin')
    

@staff_member_required
def dashboard_admin(request):
    return render(request, 'admin_function/Dashboard.html')

@staff_member_required
def comment_admin(request):
    reviews = Review.objects.all()
    products = Product.objects.all()
    return render(request, 'admin_function/CommentAdmin.html', {'reviews': reviews, 'products': products})

@csrf_exempt
def add_reply(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        reply_text = request.POST.get('reply_text')

        try:
            review = models.Review.objects.get(review_id=review_id)
            review.review_text_admin = reply_text
            review.save()
            return redirect('admin_comment')
        except models.Review.DoesNotExist:
            return redirect('admin_comment')

    return redirect('admin_comment')


