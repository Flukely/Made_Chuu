from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_function, name='admin_function'),

    path('ChatsAdmin/',views.ChatAdmin , name = 'ChatsAdmin'),

    path('OrderAdmin/',views.OrderAdmin, name = 'OrderAdmin'),

    path('Dashboard/',views.Dashboard, name = 'Dashboard'),

    path('CommentsAdmin/',views.CommentAdmin, name = 'CommentsAdmin'),

    path('ProductsAdmin/',views.product_list, name = 'ProductsAdmin'),

    path('DeliveryAdmin/',views.DeliveryAdmin, name = 'DeliveryAdmin'),

    path('add_product/',views.product_list, name = 'add_product'),

    path('PromotionsAdmin/',views.PromotionsAdmin, name = 'PromotionsAdmin'),
]