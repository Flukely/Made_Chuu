from django import forms # นำเข้า forms จาก Django
from main.models import Payment, Order, OrderProduct # นำเข้าโมเดล Payment และ Order จาก main.models

# สร้างฟอร์มสำหรับการชำระเงินโดยใช้ ModelForm
class Paymentform(forms.ModelForm): # สร้างคลาส Paymentform โดยสืบทอดจาก forms.ModelForm
    # ฟิลด์ order ใช้ ModelChoiceField เพื่อให้ผู้ใช้เลือกคำสั่งซื้อที่ยังไม่มีการชำระเงิน
    order_id = forms.ModelChoiceField( # สร้างฟิลด์ order_id โดยใช้ ModelChoiceField
        queryset=Order.objects.exclude( # กำหนด queryset ให้เป็น Order โดยตัดคำสั่งซื้อที่มีการชำระเงินแล้วออก
            order_id__in=Payment.objects.values_list("order_id", flat=True)  # ดึง order_id ทั้งหมดที่มีอยู่ใน Payment แล้วตัดออกจากตัวเลือก
        ),
        label="รายละเอียดคำสั่งซื้อ",  # ตั้งชื่อ Label สำหรับแสดงผลในฟอร์ม
        empty_label="-- โปรดเลือกคำสั่งซื้อ --",  # ข้อความเริ่มต้นของ dropdown
        widget=forms.Select(attrs={'class': 'form-control'}),  # กำหนด class CSS เพื่อใช้กับ Bootstrap
        to_field_name="order_id"  # ใช้ order_id เป็นค่าในฟอร์ม
    )

    class Meta: # กำหนดคุณสมบัติของฟอร์ม
        model = Payment  # ระบุโมเดลที่ใช้สร้างฟอร์ม
        fields = ['order_id', 'payment_image']  # ระบุฟิลด์ที่ต้องการให้แสดงในฟอร์ม
        widgets = { # กำหนด widget ให้กับฟิลด์ payment_image เป็น FileInput
            'payment_image': forms.FileInput(attrs={'class': 'form-control', 'required': 'required'}),  # กำหนดให้ฟิลด์อัปโหลดไฟล์เป็น required
        }

    def __init__(self, *args, **kwargs): # สร้างเมทอด __init__ สำหรับกำหนด queryset ให้กับฟิลด์ order_id
        super().__init__(*args, **kwargs) # เรียกใช้เมทอด __init__ ของคลาสแม่
        self.fields['order_id'].queryset = Order.objects.exclude( # กำหนด queryset ให้กับฟิลด์ order_id โดยตัดคำสั่งซื้อที่มีการชำระเงินแล้วออก
            order_id__in=Payment.objects.values_list("order_id", flat=True) # ดึง order_id ทั้งหมดที่มีอยู่ใน Payment แล้วตัดออกจากตัวเลือก
        ).select_related('user_id') # ใช้ select_related เพื่อดึงข้อมูลของผู้ใช้ที่สั่งซื้อมาด้วย
        self.fields['order_id'].label_from_instance = self.label_from_instance # กำหนดเมทอด label_from_instance ให้กับฟิลด์ order_id

    def label_from_instance(self, obj): # สร้างเมทอด label_from_instance สำหรับกำหนดข้อความที่แสดงใน dropdown
        products = OrderProduct.objects.filter(order_id=obj) # ดึงข้อมูลสินค้าที่อยู่ในคำสั่งซื้อ
        product_details = ", ".join([f"{p.product_id.product_name} (จำนวน: {p.quantity} ชิ้น)" for p in products]) # สร้างข้อความรายละเอียดสินค้า
        return f"คุณ: {obj.user_id.user_name}, หมายเลขคำสั่งซื้อ: {obj.order_id}, สินค้า: {product_details}, ราคารวม: {obj.total_price} บาท" # สร้างข้อความที่แสดงใน dropdown