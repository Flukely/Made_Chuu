from django.urls import path
from main import views
urlpatterns = [
    path('',views.index),
    path('ChatsAdmin/',views.ChatAdmin , name = 'ChatsAdmin'),
    path('OrderAdmin/',views.OrderAdmin, name = 'OrderAdmin'),
    path('Dashboard/',views.Dashboard, name = 'Dashboard'),
    path('CommentsAdmin/',views.CommentAdmin, name = 'CommentsAdmin'),
    path('ProductsAdmin/',views.ProductAdmin, name = 'ProductsAdmin'),
    path('PromotionsAdmin/',views.PromotionsAdmin, name = 'PromotionsAdmin')

]
