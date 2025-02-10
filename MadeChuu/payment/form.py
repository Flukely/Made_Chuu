from django import forms # นำเข้า forms จาก Django
from main.models import Payment, Order, OrderProduct # นำเข้าโมเดล Payment และ Order จาก main.models

class PaymentForm(forms.ModelForm): 
    order_id = forms.ModelChoiceField( 
        queryset=Order.objects.exclude( 
            order_id__in=Payment.objects.values_list("order_id", flat=True)
        ), 
        label="รายละเอียดคำสั่งซื้อ", 
        empty_label="-- โปรดเลือกคำสั่งซื้อ --", 
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name="order_id" 
    )

    class Meta: 
        model = Payment  
        fields = ['order_id', 'payment_image']  
        widgets = { 
            'payment_image': forms.FileInput(attrs={'class': 'form-control', 'required': 'required'}),  
        }

    def __init__(self, *args, **kwargs): # สร้างเมธอด __init__ สำหรับกำหนดค่าให้กับ order_id
        super().__init__(*args, **kwargs)  
        self.fields['order_id'].queryset = Order.objects.exclude( 
            order_id__in=Payment.objects.values_list("order_id", flat=True) 
        ).select_related('user') 
        self.fields['order_id'].label_from_instance = self.label_from_instance 

    def label_from_instance(self, obj): 
        products = OrderProduct.objects.filter(order=obj) 
        product_details = ", ".join([f"{p.product.product_name} (จำนวน: {p.quantity} ชิ้น)" for p in products]) 
        return f"คุณ: {obj.user.user_name}, หมายเลขคำสั่งซื้อ: {obj.order_id}, สินค้า: {product_details}, ราคารวม: {obj.total_price} บาท"