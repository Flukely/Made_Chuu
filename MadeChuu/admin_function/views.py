from django.shortcuts import render , redirect ,get_object_or_404
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.admin.views.decorators import staff_member_required
from .filters import *
from .forms import ProductForm , PromotionForm ,ProductSelectionForm
from main.models import *
from django.core.paginator import Paginator
from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models import Sum , F
from django.utils.timezone import now
from django.utils import timezone
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
from django.http import JsonResponse
import numpy as np
from django.db.models.functions import TruncDate
from plotly.subplots import make_subplots

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

## test
@staff_member_required
def dashboard_admin(request):
    today = timezone.localtime(timezone.now()).date()
    shop_id = request.session['shop_id']
    products = Product.objects.filter(shop_id=shop_id)
    categorys = Category.objects.filter(shop_id=shop_id)
    
    # Basic counts
    orders_all = Order.objects.filter(shop_id=shop_id).exclude(status_order__status_name__in=['ดำเนินการคืนเงิน']).count()
    orders_today = Order.objects.filter(order_date__date=today, shop_id=shop_id).count()
    users_all = User.objects.all().count()
    users_today = User.objects.filter(join_date=today).count()
    revenue_all = Order.objects.filter(shop_id=shop_id).exclude(status_order__status_name__in=['รอการตรวจสอบ', 'ตรวจสอบจ่ายเงิน']).aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    revenue_today = Order.objects.filter(order_date__date=today, shop_id=shop_id).exclude(status_order__status_name__in=['รอการตรวจสอบ', 'ตรวจสอบจ่ายเงิน']).aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0

    # รับค่าจากฟอร์ม
    selected_product_graph1_id = request.GET.get('product_graph1')
    selected_product_graph2_id = request.GET.get('product_graph2')
    selected_product_graph3_id = request.GET.get('product_graph3')
    selected_product_graph4_id = request.GET.get('product_graph4')


    # กำหนดช่วงเวลาตาม filter_type
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')
    if start_date_filter and end_date_filter:
        start_date_filter = datetime.strptime(start_date_filter, '%Y-%m-%d').date()
        end_date_filter = datetime.strptime(end_date_filter, '%Y-%m-%d').date()

        # ตรวจสอบว่าห้ามเลือกวันที่สิ้นสุดเกินวันนี้
        if end_date_filter > timezone.localtime(timezone.now()).date():
            end_date_filter = timezone.localtime(timezone.now()).date()

        # ตรวจสอบว่าห้ามเลือกวันที่เริ่มต้นมากกว่าวันที่สิ้นสุด
        if start_date_filter > end_date_filter:
            return redirect('Dashboardtest')
    else:
        # กำหนดค่าเริ่มต้นหากไม่ได้เลือกวันที่
        end_date_filter = timezone.localtime(timezone.now()).date()
        start_date_filter = end_date_filter - timedelta(days=30)  # ค่าเริ่มต้น: 30 วันก่อนหน้า

    # สร้าง labels ตามช่วงวันที่ที่เลือก
    labels = [(start_date_filter + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date_filter - start_date_filter).days + 1)]

    selected_products = [
        selected_product_graph1_id,
        selected_product_graph2_id,
        selected_product_graph3_id,
        selected_product_graph4_id
    ]


    # ดึงข้อมูลสินค้ายอดนิยม (สำหรับกรณีไม่เลือกสินค้า)
    top_products = OrderProduct.objects.filter(
        product__shop_id=shop_id
    ).values('product__product_name').annotate(
        total_sales=Sum(F('quantity') * F('product__price'))
    ).order_by('-total_sales')[:4]


    ### กราฟรายได้ ---------------------------------------------------

    if any(selected_products):  # หากมีการเลือกสินค้า
        order_products = OrderProduct.objects.filter(
            order__shop_id=shop_id,
            product__product_id__in=[p for p in selected_products if p]
        ).values(
            'product__product_name', 
            'order__order_date'
        ).annotate(
            total_quantity=Sum('quantity')
        )
    else:  # หากไม่มีการเลือกสินค้า
        top_product_ids = [product['product__product_name'] for product in top_products]
        order_products = OrderProduct.objects.filter(
            order__shop_id=shop_id,
            product__product_name__in=top_product_ids
        ).values(
            'product__product_name', 
            'order__order_date'
        ).annotate(
            total_quantity=Sum('quantity')
        )

    
    # สร้าง product_data และเก็บข้อมูลวันที่
    product_data = {}
    for label in labels:
        for item in order_products:
            product_name = item['product__product_name']
            order_date = item['order__order_date'].date()  # เปลี่ยนให้เป็น date object

            if product_name not in product_data:
                product_data[product_name] = [0] * len(labels)

            if order_date.strftime('%Y-%m-%d') == label:
                index = labels.index(label)
                total_quantity = item['total_quantity']  # ใช้จำนวนสินค้าที่ขายได้
                product_data[product_name][index] += total_quantity



    colors = px.colors.qualitative.Vivid
    dash_styles = ['solid', 'dash', 'dot', 'dashdot']

    revenue_fig = go.Figure()

    for i, (product_name, revenue_list) in enumerate(product_data.items()):
        revenue_fig.add_trace(go.Scatter(
            x=labels,
            y=revenue_list,
            mode='lines+markers',
            name=product_name,
            line=dict(
                color=colors[i % len(colors)],
                width=3,
                dash=dash_styles[i % len(dash_styles)]
            ),
            marker=dict(size=6),
            hovertemplate=f'<b>{product_name}</b><br>วันที่ %{{x}}<br>จำนวน: <b>%{{y:,.0f}} ชิ้น</b><extra></extra>'
        ))

    revenue_fig.update_layout(
        title=dict(
            text='<b>กราฟยอดขายตามช่วงเวลา (แยกตามสินค้า)</b>',
            font=dict(size=24, family='Prompt', color='#2a3f5f'),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            title=dict(text='<b>วันที่</b>', font=dict(size=14)),
            tickangle=45,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            title=dict(text='<b>จำนวนสินค้า (ชิ้น)</b>', font=dict(size=14)),
            tickformat=',.0f',
            gridcolor='rgba(0,0,0,0.1)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        margin=dict(t=100, b=150, l=80, r=50),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            bordercolor='rgba(0,0,0,0.5)'
        )
    )

    # แปลงกราฟเป็น HTML
    revenue_plot = plot(revenue_fig, output_type='div', include_plotlyjs=True)

    ### END กราฟรายได้ ---------------------------------------------------

    ### แผนที่ประเทศไทย 
    province_coords = {
        'กรุงเทพมหานคร': {'lat': 13.7563, 'lon': 100.5018},
        'สมุทรปราการ': {'lat': 13.5993, 'lon': 100.5967},
        'นนทบุรี': {'lat': 13.8623, 'lon': 100.5149},
        'ปทุมธานี': {'lat': 14.0208, 'lon': 100.5253},
        'พระนครศรีอยุธยา': {'lat': 14.3692, 'lon': 100.5870},
        'อ่างทอง': {'lat': 14.5894, 'lon': 100.4529},
        'ลพบุรี': {'lat': 14.7995, 'lon': 100.6534},
        'สิงห์บุรี': {'lat': 14.8936, 'lon': 100.3965},
        'ชัยนาท': {'lat': 15.1856, 'lon': 100.1251},
        'สระบุรี': {'lat': 14.5286, 'lon': 100.9104},
        'ชลบุรี': {'lat': 13.3611, 'lon': 100.9847},
        'ระยอง': {'lat': 12.6814, 'lon': 101.2814},
        'จันทบุรี': {'lat': 12.6113, 'lon': 102.1039},
        'ตราด': {'lat': 12.2428, 'lon': 102.5175},
        'ฉะเชิงเทรา': {'lat': 13.6904, 'lon': 101.0779},
        'ปราจีนบุรี': {'lat': 14.0509, 'lon': 101.3686},
        'นครนายก': {'lat': 14.2069, 'lon': 101.2128},
        'สระแก้ว': {'lat': 13.8240, 'lon': 102.0643},
        'นครราชสีมา': {'lat': 14.9718, 'lon': 102.1016},
        'บุรีรัมย์': {'lat': 14.9950, 'lon': 103.1027},
        'สุรินทร์': {'lat': 14.8828, 'lon': 103.4936},
        'ศรีสะเกษ': {'lat': 15.1186, 'lon': 104.3229},
        'อุบลราชธานี': {'lat': 15.2298, 'lon': 104.8594},
        'ยโสธร': {'lat': 15.7954, 'lon': 104.1491},
        'ชัยภูมิ': {'lat': 15.8067, 'lon': 102.0318},
        'อำนาจเจริญ': {'lat': 15.8656, 'lon': 104.6288},
        'หนองบัวลำภู': {'lat': 17.2218, 'lon': 102.4264},
        'ขอนแก่น': {'lat': 16.4322, 'lon': 102.8236},
        'อุดรธานี': {'lat': 17.4158, 'lon': 102.7870},
        'เลย': {'lat': 17.4860, 'lon': 101.7223},
        'หนองคาย': {'lat': 17.8785, 'lon': 102.7420},
        'มหาสารคาม': {'lat': 16.1840, 'lon': 103.3007},
        'ร้อยเอ็ด': {'lat': 16.0538, 'lon': 103.6520},
        'กาฬสินธุ์': {'lat': 16.4329, 'lon': 103.5086},
        'สกลนคร': {'lat': 17.1585, 'lon': 104.1469},
        'นครพนม': {'lat': 17.3926, 'lon': 104.7693},
        'มุกดาหาร': {'lat': 16.5436, 'lon': 104.7234},
        'เชียงใหม่': {'lat': 18.7883, 'lon': 98.9853},
        'ลำพูน': {'lat': 18.5745, 'lon': 99.0087},
        'ลำปาง': {'lat': 18.2898, 'lon': 99.4909},
        'อุตรดิตถ์': {'lat': 17.6257, 'lon': 100.0972},
        'แพร่': {'lat': 18.1443, 'lon': 100.1406},
        'น่าน': {'lat': 18.7756, 'lon': 100.7714},
        'พะเยา': {'lat': 19.1920, 'lon': 99.8788},
        'เชียงราย': {'lat': 19.9086, 'lon': 99.8325},
        'แม่ฮ่องสอน': {'lat': 19.3020, 'lon': 97.9654},
        'นครสวรรค์': {'lat': 15.6975, 'lon': 100.1194},
        'อุทัยธานี': {'lat': 15.3796, 'lon': 100.0245},
        'กำแพงเพชร': {'lat': 16.2530, 'lon': 99.4909},
        'ตาก': {'lat': 16.8847, 'lon': 99.1293},
        'สุโขทัย': {'lat': 17.0056, 'lon': 99.8264},
        'พิษณุโลก': {'lat': 16.8211, 'lon': 100.2659},
        'พิจิตร': {'lat': 16.4419, 'lon': 100.3487},
        'เพชรบูรณ์': {'lat': 16.4189, 'lon': 101.1539},
        'ราชบุรี': {'lat': 13.5283, 'lon': 99.8136},
        'กาญจนบุรี': {'lat': 14.0228, 'lon': 99.5328},
        'สุพรรณบุรี': {'lat': 14.4745, 'lon': 100.1206},
        'นครปฐม': {'lat': 13.8199, 'lon': 100.0623},
        'สมุทรสาคร': {'lat': 13.5475, 'lon': 100.2736},
        'สมุทรสงคราม': {'lat': 13.4098, 'lon': 100.0028},
        'เพชรบุรี': {'lat': 13.1086, 'lon': 99.9457},
        'ประจวบคีรีขันธ์': {'lat': 11.8157, 'lon': 99.7844},
        'นครศรีธรรมราช': {'lat': 8.4304, 'lon': 99.9637},
        'กระบี่': {'lat': 8.0863, 'lon': 98.9063},
        'พังงา': {'lat': 8.4505, 'lon': 98.5256},
        'ภูเก็ต': {'lat': 7.8804, 'lon': 98.3923},
        'สุราษฎร์ธานี': {'lat': 9.1396, 'lon': 99.3306},
        'ระนอง': {'lat': 9.9529, 'lon': 98.6084},
        'ชุมพร': {'lat': 10.4930, 'lon': 99.1802},
        'สงขลา': {'lat': 7.0086, 'lon': 100.4767},
        'สตูล': {'lat': 6.6239, 'lon': 100.0668},
        'ตรัง': {'lat': 7.5563, 'lon': 99.6114},
        'พัทลุง': {'lat': 7.6176, 'lon': 100.0638},
        'ปัตตานี': {'lat': 6.8684, 'lon': 101.2509},
        'ยะลา': {'lat': 6.5414, 'lon': 101.2804},
        'นราธิวาส': {'lat': 6.4255, 'lon': 101.8253},
        'บึงกาฬ': {'lat': 18.3609, 'lon': 103.6465}
    }

    # รับค่าจากฟอร์ม category_map
    selected_category = request.GET.get('category_map', None)

    # ดึงข้อมูลการสั่งซื้อแยกตามจังหวัด
    if(selected_category == 'all_category_map' or selected_category is None):
        orders_by_province_and_product = OrderProduct.objects.filter(
            order__shop_id=shop_id
        ).values(
            'order__user__province',  # จังหวัด
            'product_id',
            'product__product_name'  # สินค้า
        ).annotate(
            total_quantity=Sum('quantity')  # รวมจำนวนสินค้าที่สั่ง
        ).order_by('-total_quantity')
    else:
        orders_by_province_and_product = OrderProduct.objects.filter(
            order__shop_id=shop_id,product__category__category_name=selected_category
        ).values(
            'order__user__province',  # จังหวัด
            'product_id',
            'product__product_name'  # สินค้า
        ).annotate(
            total_quantity=Sum('quantity')  # รวมจำนวนสินค้าที่สั่ง
        ).order_by('-total_quantity')

    # แปลงข้อมูลเป็น DataFrame
    import pandas as pd
    df_orders_products = pd.DataFrame(list(orders_by_province_and_product))
    df_orders_products.rename(columns={
        'order__user__province': 'Province',
        'product_id': 'ProductID',
        'product__product_name': 'ProductName',
        'total_quantity': 'total_quantity'
    }, inplace=True)


    # รวม total_quantity ตาม Province
    df_bubble = df_orders_products.groupby('Province').agg({
        'total_quantity': 'sum',  # รวม total_quantity
        'ProductID': lambda x: ', '.join(map(str, x)),  # รวม ProductID เป็นข้อความ
    }).reset_index()

    # สร้าง hover_data สำหรับรายละเอียดสินค้า
    df_bubble['ProductDetails'] = df_orders_products.groupby('Province').apply(
        lambda x: '<br>'.join(f"{row['ProductName']}: {row['total_quantity']} ชิ้น" for _, row in x.iterrows())
    ).reset_index(drop=True)


    df_orders_products['lat'] = df_orders_products['Province'].apply(lambda x: province_coords[x]['lat'] if x in province_coords else None)
    df_orders_products['lon'] = df_orders_products['Province'].apply(lambda x: province_coords[x]['lon'] if x in province_coords else None)

    # สร้าง Choropleth Map
    choropleth_fig = px.choropleth(
        df_orders_products,
        geojson="https://raw.githubusercontent.com/apisit/thailand.json/master/thailand.json",
        locations='Province',
        featureidkey="properties.name",
        color='total_quantity',
        hover_name='Province',
        hover_data=['total_quantity'],
        title='<b>ประเภทสินค้าที่ซื้อมากที่สุดแบ่งตามภาคในประเทศไทย</b>',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        width=800,
        height=700
    )
    
    choropleth_fig.update_geos(
        fitbounds="locations",
        visible=True,
        showcountries=True,  # แสดงเส้นแบ่งประเทศ
        countrycolor="Black",
        showsubunits=True,
        projection_type="mercator",
        subunitcolor="Gray",
    )
    
    choropleth_fig.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        title_x=0.5,
        legend_title_text='สินค้า',
        font=dict(family="Prompt", size=16)
    )
    
    # แปลงกราฟเป็น HTML
    choropleth_plot = plot(choropleth_fig, output_type='div', include_plotlyjs=True)

    # สร้าง Bubble Map
    bubble_fig = px.scatter_geo(
        df_bubble,
        lat=df_bubble['Province'].apply(lambda x: province_coords[x]['lat'] if x in province_coords else None),
        lon=df_bubble['Province'].apply(lambda x: province_coords[x]['lon'] if x in province_coords else None),
        size='total_quantity',  # ขนาดของ Bubble ตาม total_quantity รวม
        hover_name='Province',
        hover_data={'total_quantity': True, 'ProductDetails': True},  # แสดงรายละเอียดสินค้า
        title='<b>สินค้าที่สั่งซื้อในแต่ละจังหวัด</b>',
        scope='asia',
        color='total_quantity',  # ใช้สีแสดง total_quantity รวม
        color_continuous_scale=px.colors.sequential.Inferno,
        width=1000,
        height=700
    )
    bubble_fig.update_traces(
        marker=dict(
            sizemode='area',
            sizeref=0.05,  # ค่าน้อยลง = Bubble ใหญ่ขึ้น
            sizemin=4
        )
    )
    
    bubble_fig.update_geos(
        visible=True,
        resolution=50,
        showcountries=True,
        countrycolor="Black",
        showsubunits=True,
        subunitcolor="white",
        lonaxis_range=[97, 106],
        lataxis_range=[5, 21]
    )
    
    bubble_fig.update_layout(
        width=None,
        autosize = True,
        margin={"r":0,"t":50,"l":0,"b":0},
        title_x=0.5,
        legend_title_text='สินค้า',
        font=dict(family="Prompt", size=13)
    )
    
    # แปลงกราฟเป็น HTML
    bubble_plot = plot(bubble_fig, output_type='div', include_plotlyjs=True)

    ### END_แผนที่ประเทศไทย

    # 1. Shop-wide gender ratio analysis
    shop_customers = User.objects.filter(order__shop_id=shop_id).distinct()
    shop_gender_counts = shop_customers.values('gender').annotate(count=Count('gender')).order_by('-count')
    
    # Calculate percentages for shop data
    shop_total = sum(item['count'] for item in shop_gender_counts)
    shop_gender_data = []
    for item in shop_gender_counts:
        percentage = (item['count'] / shop_total) * 100 if shop_total > 0 else 0
        shop_gender_data.append({
            'gender': item['gender'],
            'count': item['count'],
            'percentage': round(percentage, 2)
        })
    
    # 2. Product-specific gender analysis
    product1_id = request.GET.get('product1')
    product2_id = request.GET.get('product2')
    
    product1 = None
    product2 = None
    product1_gender_counts = []
    product2_gender_counts = []
    
    # Process product 1
    if product1_id:
        try:
            product1 = Product.objects.get(product_id=product1_id, shop_id=shop_id)
            product1_customers = User.objects.filter(
                order__orderproduct__product_id=product1_id,
                order__shop_id=shop_id
            ).distinct()
            product1_gender_counts = product1_customers.values('gender').annotate(count=Count('gender')).order_by('-count')
        except Product.DoesNotExist:
            pass
    
    # Process product 2
    if product2_id:
        try:
            product2 = Product.objects.get(product_id=product2_id, shop_id=shop_id)
            product2_customers = User.objects.filter(
                order__orderproduct__product_id=product2_id,
                order__shop_id=shop_id
            ).distinct()
            product2_gender_counts = product2_customers.values('gender').annotate(count=Count('gender')).order_by('-count')
        except Product.DoesNotExist:
            pass
    
    # Function to create pie chart
    def create_pie_chart(labels, values, title):
        colors = ['#FFA07A', '#20B2AA', '#778899']  # สีสำหรับผู้ชาย, ผู้หญิง, อื่นๆ
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors[:len(labels)], line=dict(color='white', width=2)),
            textinfo='percent+value',
            texttemplate='%{label}<br>%{value} คน<br>(%{percent})',
            hoverinfo='label+percent+value',
            textfont=dict(size=14)
        )])
        
        fig.update_layout(
            title=dict(
                text=f'<b>{title}</b>',
                font=dict(size=18, family='Prompt'),
                x=0.5,
                y=0.95
            ),
            height=400,
            margin=dict(t=100, b=50, l=50, r=50),
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=False,
            annotations=[dict(
                text=f'รวม<br>{sum(values):,} คน',
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False
            )]
        )
        
        return plot(fig, output_type='div', include_plotlyjs=True)
    
    # Create charts
    shop_gender_labels = [item['gender'] for item in shop_gender_counts]
    shop_gender_values = [item['count'] for item in shop_gender_counts]
    shop_pie_div = create_pie_chart(
        shop_gender_labels, 
        shop_gender_values, 
        "อัตราส่วนเพศลูกค้าที่ซื้อสินค้า"
    )
    
    # Product 1 chart
    product1_pie_div = None
    if product1:
        product1_gender_labels = [item['gender'] for item in product1_gender_counts]
        product1_gender_values = [item['count'] for item in product1_gender_counts]
        product1_pie_div = create_pie_chart(
            product1_gender_labels,
            product1_gender_values,
            f"อัตราส่วนเพศผู้ซื้อ : {product1.product_name}"
        )
        
        # Calculate percentages for product 1
        product1_total = sum(item['count'] for item in product1_gender_counts)
        product1_gender_data = []
        for item in product1_gender_counts:
            percentage = (item['count'] / product1_total) * 100 if product1_total > 0 else 0
            product1_gender_data.append({
                'gender': item['gender'],
                'count': item['count'],
                'percentage': round(percentage, 2)
            })
    else:
        product1_gender_data = []
    
    # Product 2 chart
    product2_pie_div = None
    if product2:
        product2_gender_labels = [item['gender'] for item in product2_gender_counts]
        product2_gender_values = [item['count'] for item in product2_gender_counts]
        product2_pie_div = create_pie_chart(
            product2_gender_labels,
            product2_gender_values,
            f"อัตราส่วนเพศผู้ซื้อ : {product2.product_name}"
        )
        
        # Calculate percentages for product 2
        product2_total = sum(item['count'] for item in product2_gender_counts)
        product2_gender_data = []
        for item in product2_gender_counts:
            percentage = (item['count'] / product2_total) * 100 if product2_total > 0 else 0
            product2_gender_data.append({
                'gender': item['gender'],
                'count': item['count'],
                'percentage': round(percentage, 2)
            })
    else:
        product2_gender_data = []




    #### --------------------สินค้าขายดี 10 อันดับ -----------------------------------------------------------
    top_start_date = request.GET.get("top_start_date")
    top_end_date = request.GET.get("top_end_date")
    top_category = request.GET.get("top_category")
    # Get top 10 best-selling products by total sales (quantity * price)
    # Create base query
    top_products_query = OrderProduct.objects.filter(
        product__shop_id=shop_id
    )

    # Apply date filter if dates are provided
    if top_start_date and top_end_date:
        top_products_query = top_products_query.filter(
            order__order_date__gte=top_start_date,
            order__order_date__lte=top_end_date
        )

    # Apply category filter if category is provided
    if top_category and top_category != 'top_category_all':
    # First try to convert to integer (in case it's an ID)
        try:
            category_id = int(top_category)
            top_products_query = top_products_query.filter(
                product__category_id=category_id
            )
        except ValueError:
            # If not an integer, filter by category name
            top_products_query = top_products_query.filter(
                product__category__category_name=top_category
            )

    # Get top 10 best-selling products by total sales (quantity * price)
    top_products = top_products_query.values(
        'product__product_name'
    ).annotate(
        total_sales=Sum(F('quantity') * F('product__price'))
    ).order_by('-total_sales')[:10]

    # Prepare data for the chart
    product_names = [p['product__product_name'] for p in top_products]
    sales_values = [float(p['total_sales']) for p in top_products]

    # Create the bar chart with enhanced styling
    custom_pink_scale = ['#8B0033', '#B80047', '#E6005C', '#FF2A79', '#FF5A94', '#FF8AAF', '#FFB3C6', '#FFE4EC']

    top_seller_fig = go.Figure(
        go.Bar(
            x=product_names,
            y=sales_values,
            marker=dict(
                color=custom_pink_scale,
                line=dict(color=custom_pink_scale, width=1.5)  # Add border to bars
            ),
            text=sales_values,
            texttemplate='<b>%{text:,.0f}</b> บาท',
            textposition='outside',
            textfont=dict(
                family="Arial",
                size=12,
                color='#264653'
            ),
            hovertemplate='<b>%{x}</b><br>ยอดขายรวม: <b>%{y:,.0f} บาท</b><extra></extra>',
            hoverlabel=dict(
                bgcolor="#264653",
                font_size=14,
                font_family="Arial"
            ),
            width=0.7  # Adjust bar width
        )
    )

    # Customize the layout with professional styling
    top_seller_fig.update_layout(
        title=dict(
            text='<b> สินค้าขายดีประจำร้าน</b>',
            font=dict(
                family="Arial",
                size=20,
                color='#264653'
            ),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(
                text='<b>ชื่อสินค้า</b>',
                font=dict(size=14, color='#264653')
            ),
            tickfont=dict(size=12, color='#6D6875'),
            tickangle=45,
            gridcolor='#f0f0f0',
            linecolor='#f0f0f0',
            showline=True
        ),
        yaxis=dict(
            title=dict(
                text='<b>ยอดขายรวม (บาท)</b>',
                font=dict(size=14, color='#264653')
            ),
            tickformat=',.0f',
            gridcolor='#f0f0f0',
            zerolinecolor='#f0f0f0',
            range=[0, max(sales_values) * 1.2] if sales_values else [0, 1],
            tickfont=dict(size=12, color='#6D6875')
        ),
        height=550,
        width=900,
        margin=dict(l=80, r=50, b=180, t=80, pad=10),
        plot_bgcolor='white',
        paper_bgcolor='white',
        hovermode='x unified',
        showlegend=False,
        bargap=0.2,  # Gap between bars
        uniformtext=dict(
            minsize=10,
            mode='hide'
        )
    )

        # Convert to HTML div
    top_seller_chart = plot(top_seller_fig, output_type='div', include_plotlyjs=False)
    #### --------------------END สินค้าขายดี 10 อันดับ -----------------------------------------------------------

    
    
    context = {
        'title': 'Dashboard',
        'today': today,
        'yesterday': today - timedelta(days=1),
        'shop_pie_chart': shop_pie_div,
        'product1_pie_chart': product1_pie_div,
        'product2_pie_chart': product2_pie_div,
        'orders_all': orders_all,
        'categorys':categorys,
        'products': products,
        'start_date_filter': start_date_filter,
        'end_date_filter':end_date_filter,
        'selected_product_graph1_id': int(selected_product_graph1_id) if selected_product_graph1_id else None,
        'selected_product_graph2_id': int(selected_product_graph2_id) if selected_product_graph2_id else None,
        'selected_product_graph3_id': int(selected_product_graph3_id) if selected_product_graph3_id else None,
        'selected_product_graph4_id': int(selected_product_graph4_id) if selected_product_graph4_id else None,
        'selected_product1_id': int(product1_id) if product1_id else None,
        'selected_product2_id': int(product2_id) if product2_id else None,
        'selected_category': selected_category,
        'product1': product1,
        'product2': product2,
        'revenue_all':revenue_all,
        'revenue_today':revenue_today,
        'orders_today': orders_today,
        'users_all': users_all,
        'users_today': users_today,
        'shop_gender_data': shop_gender_data,
        'product1_gender_data': product1_gender_data,
        'product2_gender_data': product2_gender_data,
        'choropleth_plot': choropleth_plot,
        'bubble_plot': bubble_plot,
        'revenue_plot': revenue_plot,
        'top_seller_chart':top_seller_chart,
        'top_start_date':top_start_date,
        'top_end_date':top_end_date,
        'top_category':top_category,
    }
    
    return render(request, 'admin_function/Dashboard.html', context)


###############################################################################################
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