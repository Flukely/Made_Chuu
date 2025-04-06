from django import forms
from main.models import *
from django.utils.safestring import mark_safe
from django.core.validators import MinValueValidator

class ProductForm(forms.ModelForm):
    # เพิ่ม field customization และ validation
    product_name = forms.CharField(
        label='ชื่อสินค้า',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'กรุณากรอกชื่อสินค้า'
        }),
        max_length=255,
        required=True
    )
    
    description = forms.CharField(
        label='รายละเอียดสินค้า',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'อธิบายรายละเอียดสินค้า...'
        }),
        required=False
    )
    
    price = forms.DecimalField(
        label='ราคา',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0'
        }),
        validators=[MinValueValidator(0)],
        required=True
    )
    
    quantity = forms.IntegerField(
        label='จำนวนในสต็อก',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        }),
        validators=[MinValueValidator(0)],
        required=True
    )
    
    category = forms.ModelChoiceField(
        label='หมวดหมู่',
        queryset=Category.objects.none(),  # จะตั้งค่าใน __init__
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        required=True
    )
    
    product_image = forms.ImageField(
        label='รูปภาพสินค้า',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        required=False
    )

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'quantity', 'category', 'product_image']
    
    def __init__(self, *args, **kwargs):
        # ดึง shop_id จาก kwargs ถ้ามี (สำหรับกรณีที่ต้องการกรองหมวดหมู่ตามร้าน)
        shop_id = kwargs.pop('shop_id', None)
        super().__init__(*args, **kwargs)
        
        # กรองหมวดหมู่เฉพาะของร้านนี้
        if shop_id:
            self.fields['category'].queryset = Category.objects.filter(shop_id=shop_id)
        else:
            self.fields['category'].queryset = Category.objects.all()
        
        # ปรับแต่ง error messages
        self.fields['product_name'].error_messages = {
            'required': 'กรุณากรอกชื่อสินค้า'
        }
        self.fields['price'].error_messages = {
            'required': 'กรุณากรอกราคาสินค้า',
            'min_value': 'ราคาต้องไม่ต่ำกว่า 0 บาท'
        }
        self.fields['quantity'].error_messages = {
            'required': 'กรุณากรอกจำนวนสินค้า',
            'min_value': 'จำนวนต้องไม่ต่ำกว่า 0'
        }
        self.fields['category'].error_messages = {
            'required': 'กรุณาเลือกหมวดหมู่'
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError("ราคาต้องมากกว่า 0 บาท")
        return price
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError("จำนวนสินค้าไม่สามารถเป็นลบได้")
        return quantity
    
    def clean(self):
        cleaned_data = super().clean()
        # สามารถเพิ่ม validation ระหว่าง field ได้ที่นี่
        return cleaned_data

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
        