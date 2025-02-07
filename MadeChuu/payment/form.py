from django import forms
from .models import Payment, Order, OrderProducts

# สร้างฟอร์มสำหรับการชำระเงินโดยใช้ ModelForm
class Paymentform(forms.ModelForm):
    # ฟิลด์ order ใช้ ModelChoiceField เพื่อให้ผู้ใช้เลือกคำสั่งซื้อที่ยังไม่มีการชำระเงิน
    order = forms.ModelChoiceField(
        queryset=Order.objects.exclude(
            order_id__in=Payment.objects.values_list("order_id", flat=True)  # ดึง order_id ทั้งหมดที่มีอยู่ใน Payment แล้วตัดออกจากตัวเลือก
        ),
        label="รายละเอียดคำสั่งซื้อ",  # ตั้งชื่อ Label สำหรับแสดงผลในฟอร์ม
        empty_label="-- โปรดเลือกคำสั่งซื้อ --",  # ข้อความเริ่มต้นของ dropdown
        widget=forms.Select(attrs={'class': 'form-control'}),  # กำหนด class CSS เพื่อใช้กับ Bootstrap
        to_field_name="order_id"  # ใช้ order_id เป็นค่าในฟอร์ม
    )

    class Meta:
        model = Payment  # ระบุโมเดลที่ใช้สร้างฟอร์ม
        fields = ['order', 'image_payment']  # ระบุฟิลด์ที่ต้องการให้แสดงในฟอร์ม
        widgets = {
            'image_payment': forms.FileInput(attrs={'class': 'form-control', 'required': 'required'}),  # กำหนดให้ฟิลด์อัปโหลดไฟล์เป็น required
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order'].queryset = Order.objects.exclude(
            order_id__in=Payment.objects.values_list("order_id", flat=True)
        ).select_related('user')
        self.fields['order'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        products = OrderProducts.objects.filter(order=obj)
        product_details = ", ".join([f"{p.product.product_name} (จำนวน: {p.quantity} ชิ้น)" for p in products])
        return f"คุณ: {obj.user.user_name}, หมายเลขคำสั่งซื้อ: {obj.order_id}, สินค้า: {product_details}, ราคารวม: {obj.total_price} บาท"
