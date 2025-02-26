from django import forms
from main.models import CartItem

class CartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']