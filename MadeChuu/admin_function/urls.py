from django.urls import path
from . import views
from django.conf import settings
from  django.conf.urls.static import static

urlpatterns = [
    path('', views.admin_function, name='admin_function'),

    path('ChatsAdmin/',views.ChatAdmin , name = 'ChatsAdmin'),

    path('OrderAdmin/',views.OrderAdmin, name = 'OrderAdmin'),

    path('Dashboard/',views.Dashboard, name = 'Dashboard'),

    path('CommentsAdmin/',views.CommentAdmin, name = 'CommentsAdmin'),

    path('ProductsAdmin/',views.product_list, name = 'ProductsAdmin'),

    path('PromotionsAdmin/',views.PromotionsAdmin, name = 'PromotionsAdmin'),
    
    path('add_product/',views.product_list, name = 'add_product'),

    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),

    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)