from django.urls import path
from .views import register, user_login, logout_view
from product.views import product

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', product, name='product'),
]