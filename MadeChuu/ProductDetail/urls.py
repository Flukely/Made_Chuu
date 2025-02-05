from django.urls import path
from ProductDetail import views

urlpatterns = [
    path('', views.product_detail),
]