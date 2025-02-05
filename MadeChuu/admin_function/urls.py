from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_function, name='admin_function'),
    path('ChatsAdmin/',views.ChatAdmin , name = 'ChatsAdmin'),
    path('OrderAdmin/',views.OrderAdmin, name = 'OrderAdmin'),
    path('Dashboard/',views.Dashboard, name = 'Dashboard'),
    path('CommentsAdmin/',views.CommentAdmin, name = 'CommentsAdmin'),
    path('ProductsAdmin/',views.ProductAdmin, name = 'ProductsAdmin'),
    path('PromotionsAdmin/',views.PromotionsAdmin, name = 'PromotionsAdmin'),
]