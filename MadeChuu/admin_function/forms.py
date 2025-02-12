from django import forms
from main.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'quantity', 'category','product_image' ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'total_price', 'status_order', 'place_delivery', 'shipper', 'tracking_num', 'delivery_date']
