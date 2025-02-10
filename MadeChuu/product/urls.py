from django.urls import path 
from . import views

urlpatterns = [
    path('',views.product, name='product'),
    path('shop1/', views.shop1, name='shop1'),# Add this line
     path('shop2/', views.shop2, name='shop2'),
]