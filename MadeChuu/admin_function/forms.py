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
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # กำหนด CSS class และ placeholder ให้แต่ละ field
        self.fields['promotion_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'กรุณากรอกชื่อโปรโมชัน'
        })
        
        self.fields['promotion_type'].widget.attrs.update({
            'class': 'form-select'  # ใช้ form-select สำหรับ dropdown
        })
        
        self.fields['discount'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '0-100%'
        })
        
        # กำหนดให้วันที่ใช้ HTML5 date picker
        self.fields['start_date'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
        
        self.fields['end_date'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
        
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'รายละเอียดโปรโมชัน...'
        })
        
        self.fields['promotion_image'].widget.attrs.update({
            'class': 'form-control'
        })

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
        