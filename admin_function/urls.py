from django.urls import path
from . import views
from django.conf import settings
from  django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', views.admin_function, name='admin_function'),

    path('ChatsAdmin/',views.ChatAdmin , name = 'ChatsAdmin'),

    path('OrderAdmin/',views.OrderAdmin, name = 'OrderAdmin'),

    path('Dashboard/', staff_member_required(views.dashboard_admin), name='Dashboard'),
    
    path('add_reply', views.add_reply, name = 'add_reply'),

    path('CommentAdmin/', staff_member_required(views.comment_admin), name='CommentAdmin'),



    path('add_promotion/', views.add_promotion, name='add_promotion'),
    path('promotion_list/', views.promotion_list, name='promotion_list'),
    path('delete_promotion/<int:promotion_id>/', views.delete_promotion, name='delete_promotion'),
    path('promotions/edit/<int:promotion_id>/', views.edit_promotion, name='edit_promotion'),



    path('ProductsAdmin/',views.product_list, name = 'ProductsAdmin'),

    path('PromotionsAdmin/',views.PromotionsAdmin, name = 'PromotionsAdmin'),
    
    path('add_product/',views.product_list, name = 'add_product'),

    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),

    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    path('status/wait/<int:order_id>/', views.status_wait, name='status_wait'),
    path('status/paid/<int:order_id>/', views.status_paid, name='status_paid'),
    path('status/packing/<int:order_id>/', views.status_packing, name='status_packing'),
    path('status/prepare/<int:order_id>/', views.status_prepare, name='status_prepare'),
    path('status/delivery/<int:order_id>/', views.status_delivery, name='status_delivery'),
    path('status/ordersuccess/<int:order_id>/', views.status_ordersuccess, name='status_ordersuccess'),
    path('status/claim/<int:order_id>/', views.status_claim, name='status_claim'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)