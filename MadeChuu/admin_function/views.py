from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.shortcuts import render , redirect ,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from .filters import *
from .forms import ProductForm , OrderForm , PromotionForm , ProductSelectionForm
from main.models import *
from django.core.paginator import Paginator
from django.db.models import Count ,Q
from datetime import datetime, timedelta
from django.db.models import Sum , F
from django.utils.timezone import now
from django.utils import timezone


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
    return render(request, 'admin_function/promotion_list.html')

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
    today = timezone.localtime(timezone.now()).date()
    shop_id = request.session['shop_id']=1
    product_of_shop_all = Product.objects.filter(shop_id=shop_id).count()
    product_of_shop = Product.objects.filter(shop_id=shop_id)
    category = Category.objects.filter(shop_id=shop_id)
    category_counts = Product.objects.filter(shop_id=shop_id) \
        .values('category__category_name') \
        .annotate(total=Count('product_id'))
    orders_all = Order.objects.filter(shop_id=shop_id).count()
    orders_today = Order.objects.filter(order_date__date=today, shop_id=shop_id).count()
    users_all = User.objects.all().count()
    users_today = User.objects.filter(join_date=today).count()
    
    gender_counts = User.objects.values('gender').annotate(total = Count('user_id'))
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

    else:  # default to month filter
        start_date = today.replace(day=1)
        labels = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((today - start_date).days + 1)]

    # กรองข้อมูล Order ตามช่วงเวลาที่เลือก


    orders = Order.objects.filter(order_date__date__gte=start_date).exclude(status_order__status_order_id__in=[1, 2]).filter(orderproduct__product__shop_id=shop_id)


    # รวมยอดสั่งซื้อตามช่วงเวลาที่เลือก
    order_data = []
    for label in labels:
        # Convert label string to datetime, then make it timezone-aware
        label_date = timezone.make_aware(datetime.strptime(label, '%Y-%m-%d'), timezone.get_current_timezone())

        # ใช้ label_date.date() เพื่อให้ตรงกับ order_date__date
        total = orders.filter(order_date__date=label_date.date()).exclude(
            status_order__status_order_id__in=[1, 2]
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0

        order_data.append(total)

    order_products = OrderProduct.objects.filter(order__shop_id=shop_id) \
    .values('product__product_name', 'order__order_date') \
    .annotate(total_quantity=Sum('quantity'))

    
    # สร้าง product_data และเก็บข้อมูลวันที่
    product_data = {}
    for label in labels:
        for item in order_products:
            product_name = item['product__product_name']
            order_date = item['order__order_date'].date()  # เปลี่ยนให้เป็น date object

            product = Product.objects.get(product_name=product_name, shop_id=shop_id)  # Assuming product_name is unique
            unit_price = product.price  # Assuming 'unit_price' is the field storing the product price
            
            if product_name not in product_data:
                product_data[product_name] = [0] * len(labels)

            # เปรียบเทียบ order_date กับ labels (เพื่อแยกข้อมูล)
            if isinstance(label, str):
                if order_date.strftime('%Y-%m-%d') == label:  # Compare dates in string format
                    index = labels.index(label)
                    total_price = item['total_quantity'] * unit_price
                    product_data[product_name][index] += total_price
            elif isinstance(label, int):
                if order_date == label:  # Compare with month number in the case of the '1year' filter
                    index = labels.index(label)
                    total_price = item['total_quantity'] * unit_price
                    product_data[product_name][index] += total_price
    

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
        'orders_today' : orders_today,
        'product_data' : product_data,

    }
    return render(request, 'admin_function/Dashboard.html', context)


@staff_member_required
def comment_admin(request):
    reviews = Review.objects.all()
    products = Product.objects.all()
    return render(request, 'admin_function/CommentAdmin.html', {'reviews': reviews, 'products': products})

@csrf_protect
def add_reply(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        reply_text = request.POST.get('reply_text')

        if not review_id or not reply_text:
            return JsonResponse({'success': False, 'error': 'Missing data'})

        try:
            review = Review.objects.get(review_id=review_id)
            review.review_text_admin = reply_text
            review.save()
            return JsonResponse({'success': True, 'reply_text': reply_text})
        except Review.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Review not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
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

def promotion_list(request):
    # ดึงข้อมูลโปรโมชันทั้งหมดและสินค้าที่เกี่ยวข้อง
    promotions = Promotion.objects.prefetch_related(
        'promotionproduct_set__product_id'
    ).all()
    
    context = {
        'promotions': promotions
    }
    return render(request, 'admin_function/promotion_list.html', context)

def add_promotion(request):
    # รับค่า filter จาก URL parameters
    shop_id = request.GET.get('shop_id')
    category_id = request.GET.get('category_id')
    
    # ดึงข้อมูล Shop และ Category สำหรับ dropdown
    shops = Shop.objects.all()
    categories = Category.objects.all()
    
    # กรอง categories ตาม shop_id ที่เลือก (ถ้ามี)
    if shop_id:
        categories = categories.filter(shop_id=shop_id)
    
    if request.method == 'POST':
        promotion_form = PromotionForm(request.POST, request.FILES)
        # ใช้ initial data สำหรับ product_form
        product_form = ProductSelectionForm(
            data=request.POST,
            shop_id=request.GET.get('shop_id'),
            category_id=request.GET.get('category_id')
        )
        
        if promotion_form.is_valid() and product_form.is_valid():
            promotion = promotion_form.save()
            selected_products = product_form.cleaned_data['products']
            
            # สร้าง PromotionProduct
            for product in selected_products:
                PromotionProduct.objects.create(
                    promotion_id=promotion,
                    product_id=product
                )
            
            return redirect('promotion_list')
    else:
        promotion_form = PromotionForm()
        product_form = ProductSelectionForm(
            shop_id=shop_id,
            category_id=category_id
        )
    
    context = {
        'promotion_form': promotion_form,
        'product_form': product_form,
        'shops': shops,
        'categories': categories,
        'selected_shop': int(shop_id) if shop_id else None,
        'selected_category': int(category_id) if category_id else None,
    }
    
    return render(request, 'admin_function/add_promotion.html', context)

# views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def edit_promotion(request, promotion_id):
    promotion = get_object_or_404(Promotion, pk=promotion_id)
    
    if request.method == 'POST':
        promotion_form = PromotionForm(request.POST, request.FILES, instance=promotion)
        product_form = ProductSelectionForm(
            request.POST,
            shop_id=request.GET.get('shop_id'),
            category_id=request.GET.get('category_id')
        )
        
        if promotion_form.is_valid() and product_form.is_valid():
            # อัปเดตโปรโมชัน
            promotion = promotion_form.save()
            
            # ลบสินค้าเก่าและเพิ่มสินค้าใหม่
            PromotionProduct.objects.filter(promotion_id=promotion).delete()
            for product in product_form.cleaned_data['products']:
                PromotionProduct.objects.create(
                    promotion_id=promotion,
                    product_id=product
                )
            
            messages.success(request, "อัปเดตโปรโมชันสำเร็จแล้ว!")
            return redirect('promotion_list')
    else:
        # เตรียมข้อมูลเริ่มต้น
        promotion_form = PromotionForm(instance=promotion)
        initial_products = [pp.product_id for pp in promotion.promotionproduct_set.all()]
        product_form = ProductSelectionForm(
            initial={'products': initial_products},
            shop_id=request.GET.get('shop_id'),
            category_id=request.GET.get('category_id')
        )
    
    shops = Shop.objects.all()
    categories = Category.objects.all()
    
    context = {
        'promotion_form': promotion_form,
        'product_form': product_form,
        'shops': shops,
        'categories': categories,
        'selected_shop': request.GET.get('shop_id'),
        'selected_category': request.GET.get('category_id'),
        'promotion': promotion,
    }
    
    return render(request, 'admin_function/edit_promotion.html', context)

# views.py
def delete_promotion(request, promotion_id):
    promotion = get_object_or_404(Promotion, pk=promotion_id)
    if request.method == 'POST':
        promotion.delete()
        messages.success(request, "ลบโปรโมชันสำเร็จแล้ว!")
        return redirect('promotion_list')
    return render(request, 'admin_function/confirm_delete.html', {'promotion': promotion})