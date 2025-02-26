from django.urls import path
from . import views

urlpatterns = [
    path('AddCart/', views.AddCart, name='AddCart'),
    path('Confirm_Cart/', views.Confirm_Cart, name='Confirm_Cart'),
    path('place_order/', views.place_order, name='place_order'), 
    path('delete_cart_items/', views.delete_cart_items, name='delete_cart_items'),
    path('delete/<int:id>/', views.delete, name='delete'),

]
