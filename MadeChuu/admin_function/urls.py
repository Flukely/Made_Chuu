from django.urls import path, include
from . import views
from django.conf import settings
from  django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', staff_member_required(views.dashboard_admin), name='admin_function'),
    path('Dashboard/', staff_member_required(views.dashboard_admin), name='Dashboard'),

    #Promotions
    path('add_promotion/', views.add_promotion, name='add_promotion'),
    path('promotion_list/', views.promotion_list, name='promotion_list'),
    path('delete_promotion/<int:promotion_id>/', views.delete_promotion, name='delete_promotion'),
    path('promotions/edit/<int:promotion_id>/', views.edit_promotion, name='edit_promotion'),

    #Products
    path('ProductsAdmin/',views.product_list, name = 'ProductsAdmin'),
    path('add_product/',views.product_list, name = 'add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    #Reviews
    path('review-dashboard/', views.review_dashboard, name='review_dashboard'),
    path('review-admin/', views.review_admin, name='review_admin'),
    path('add_reply', views.add_reply, name = 'add_reply'),
    
    #Orders
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('payments/update/<int:payment_id>/', views.update_payment_status, name='update_payment_status'),
    path('admin/orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('admin/orders/<int:order_id>/transport/', views.admin_order_transport, name='admin_order_transport'),
    path('admin/orders/claim/<int:claim_id>/', views.update_claim_status, name='update_claim_status'),
    
    
    path('django_plotly_dash/', include('django_plotly_dash.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)