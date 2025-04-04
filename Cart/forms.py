from django import forms
from main.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'price', 'quantity','description','product_image']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'user_name','address','phone_num','province']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_id','total_price','order_date','user_id']