from django import forms
from main.models import Payment, Order, OrderProduct

class PaymentForm(forms.ModelForm):
    order_details = forms.CharField(
        label="รายละเอียดคำสั่งซื้อ",
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'readonly': 'readonly',
            'rows': 1,  # Set initial rows
            'style': 'resize: none;'  # Disable manual resizing
        }),
        required=False
    )

    class Meta:
        model = Payment
        fields = ['payment_image']
        widgets = {
            'payment_image': forms.FileInput(attrs={'class': 'form-control', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)
        if user:
            orders = Order.objects.filter(
                user=user
            ).exclude(
                order_id__in=Payment.objects.values_list("order_id", flat=True)
            ).select_related('user')
            if orders.exists():
                self.order = orders.first()  # Set the first order for the user
                self.fields['order_details'].initial = self.label_from_instance(self.order)
            else:
                self.order = None  # No orders available for the user

    def save(self, commit=True):
        payment = super().save(commit=False)
        if self.order:
            payment.order_id = self.order.order_id  # Set the order_id before saving
        if commit:
            payment.save()
        return payment

    def label_from_instance(self, obj):
        products = OrderProduct.objects.filter(order=obj)
        product_details = ", ".join([f"{p.product.product_name} (จำนวน: {p.quantity} ชิ้น)" for p in products])
        return f"คุณ: {obj.user.user_name}, หมายเลขคำสั่งซื้อ: {obj.order_id}, สินค้า: {product_details}, ราคารวม: {obj.total_price} บาท"