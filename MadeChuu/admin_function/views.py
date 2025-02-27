from django.shortcuts import render , redirect ,get_object_or_404
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.admin.views.decorators import staff_member_required
from .filters import *
from .forms import ProductForm 
from main.models import *
from django.core.paginator import Paginator
from django.db.models import Count ,Q
from datetime import datetime, timedelta
from django.db.models import Sum
from django.utils.timezone import now

def admin_function(request):
    return render(request, 'admin_function/Dashboard.html')

def Dashboard(request):
    return render(request , 'admin_function/Dashboard.html')

def ChatAdmin(request):
    return render(request, 'admin_function/ChatsAdmin.html')

def OrderAdmin(request):
    #Query from model Order
    order_filter = OrderFilter(request.GET, queryset=Order.objects.all())
    paginator = Paginator(order_filter.qs, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_function/OrderAdmin.html',{'orders':order_filter , 'page_obj': page_obj}) 

def CommentAdmin(request):
    return render(request, 'admin_function/CommentAdmin.html')

def ProductAdmin(request):
    return render(request, 'admin_function/ProductsAdmin.html')

def PromotionsAdmin(request):
    return render(request, 'admin_function/PromotionsAdmin.html')

def product_list(request):
    request.session['shop_id'] = 1
    product_filter = ProductFilter(request.GET, queryset=Product.objects.all())
    if request.method == 'POST':
        add_form = ProductForm(request.POST, request.FILES)
        if add_form.is_valid():
            product = add_form.save(commit=False)
            product.shop_id = request.session.get('shop_id')
            product.save()
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
    

from datetime import timedelta
from django.db.models import Sum

@staff_member_required
def dashboard_admin(request):
    today = now().date()
    shop_id = request.session['shop_id'] = 1
    product_of_shop_all = Product.objects.filter(shop_id=shop_id).count()
    product_of_shop = Product.objects.filter(shop_id=shop_id)
    category = Category.objects.filter(shop_id=shop_id)
    category_counts = Product.objects.filter(shop_id=shop_id) \
        .values('category__category_name') \
        .annotate(total=Count('product_id'))
    gender_counts = User.objects.values('gender').annotate(total = Count('user_id'))
    orders_all = Order.objects.filter(shop_id=shop_id).count()
    orders_today = Order.objects.filter(order_date=today).filter(shop_id=shop_id).count()
    users_all = User.objects.all().count()
    users_today = User.objects.filter(join_date=today).count()
    

    gender_data = { 'male': 0, 'female': 0, 'other': 0 }
    for item in gender_counts:
        gender_data[item['gender'].lower()] = item['total']

    filter_type = request.GET.get('filter', 'month')  # เลือกช่วงเวลาที่ต้องการ เช่น day, month, year, 3 months, 6 months, 1 year

    # กำหนด start_date ตาม filter_type ที่เลือก
    if filter_type == '5days':
        start_date = today - timedelta(days=5)
        labels = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6)]  # 5 วันล่าสุด

    elif filter_type == '1month':
        start_date = today.replace(day=1)
        labels = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((today - start_date).days + 1)]  # 1 เดือนล่าสุด

    elif filter_type == '3months':
        start_date = today - timedelta(days=90)  # 3 เดือนล่าสุด
        labels = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(91)]

    elif filter_type == '6months':
        start_date = today - timedelta(days=180)  # 6 เดือนล่าสุด
        labels = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(181)]

    elif filter_type == '1year':
        start_date = today.replace(month=1, day=1)  # 1 ปีล่าสุด
        labels = [f"{i+1}" for i in range(12)]  # แสดงเป็นเดือน 1-12

    else:  # default to month filter
        start_date = today.replace(day=1)
        labels = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((today - start_date).days + 1)]

    # กรองข้อมูล Order ตามช่วงเวลาที่เลือก


    orders = Order.objects.filter(order_date__date__gte=start_date).exclude(status_order__status_order_id__in=[1, 2]).filter(orderproduct__product__shop_id=shop_id)


    # รวมยอดสั่งซื้อตามช่วงเวลาที่เลือก
    order_data = []
    for label in labels:
        if filter_type == '1year':
            # สำหรับกรณีปี (เดือน)
            total = orders.filter(order_date__month=int(label)).exclude(status_order__status_order_id__in=[1, 2]).aggregate(Sum('total_price'))['total_price__sum'] or 0
        else:
            # สำหรับกรณีอื่นๆ (วัน)
            total = orders.filter(order_date__date=label).exclude(status_order__status_order_id__in=[1, 2]).aggregate(Sum('total_price'))['total_price__sum'] or 0
        order_data.append(total)

    context = {
        'products': product_of_shop,
        'categories': category,
        'countProduct': product_of_shop_all,
        'category_counts': category_counts,
        'filter_type': filter_type,
        'labels': labels,
        'order_data': order_data,
        'gender_data' : gender_data,
        'users_all' : users_all,
        'users_today' : users_today,
        'orders_all' : orders_all,
        'orders_today' : orders_today

    }
    return render(request, 'admin_function/Dashboard.html', context)


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

def status_wait(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/status_wait.html', {'order': order})

def status_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/status_paid.html', {'order': order})

def status_packing(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/status_packing.html', {'order': order})

def status_prepare(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/status_prepare.html', {'order': order})

def status_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/status_delivery.html', {'order': order})

def status_ordersuccess(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/status_ordersuccess.html', {'order': order})

def status_claim(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/status_claim.html', {'order': order})


