from django import forms
from main.models import *
from django.utils.safestring import mark_safe

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'quantity', 'category','product_image' ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'total_price', 'status_order', 'place_delivery', 'shipper', 'tracking_num', 'delivery_date']

class ProductCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        return mark_safe(output.replace(
            '<ul id="',
            '<ul class="product-checkbox-list" id="'
        ))

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['promotion_name', 'promotion_type', 'discount', 
                 'description', 'start_date', 'end_date', 'promotion_image']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ProductSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        shop_id = kwargs.pop('shop_id', None)
        category_id = kwargs.pop('category_id', None)
        super().__init__(*args, **kwargs)
        
        queryset = Product.objects.select_related('shop', 'category').all()
        
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        self.fields['products'] = forms.ModelMultipleChoiceField(
            queryset=queryset,
            widget=forms.CheckboxSelectMultiple,
            required=True
        )
        