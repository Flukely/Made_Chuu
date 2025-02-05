from django import forms
from .models import Payment, Order

class Paymentform(forms.ModelForm):
    order = forms.ModelChoiceField(
        queryset=Order.objects.exclude(
            order_id__in=Payment.objects.values_list("order_id", flat=True)
        ),
        label="รายละเอียดคำสั่งซื้อ",
        empty_label="-- โปรดเลือกคำสั่งซื้อ --",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Payment
        fields = ['order', 'image_payment']
        widgets = {
            'image_payment': forms.FileInput(attrs={'class': 'form-control'}),
        }