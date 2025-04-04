from django.urls import path
from ProductDetail import views

app_name = 'ProductDetail'

urlpatterns = [
    path('product/<int:product_id>/', views.product_detail, name ="product_detail"),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
]