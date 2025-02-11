from django.urls import path 
from product import views

urlpatterns = [
    path('',views.product, name='product'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('add_cart/<int:product_id>/',views.add_cart, name='add_cart1'),
]