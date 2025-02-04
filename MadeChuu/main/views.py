from django.shortcuts import render
from .models import Order, Payment
from django.core.files.storage import FileSystemStorage 
from django.http import HttpResponse
from django.utils.timezone import now

def index(request):
    return render(request, 'index.html')

def payment(request):
    if request.method == "POST":
        order_id = request.POST.get("order")  # ดึงค่า order_id จากฟอร์ม
        image = request.FILES.get("image_payment")  # ดึงไฟล์สลิปจากฟอร์ม
        
        if order_id and image:
            # ค้นหาคำสั่งซื้อที่เลือกจาก order_id
            try:
                order = Order.objects.get(order_id=order_id)  # หาคำสั่งซื้อจาก order_id
            except Order.DoesNotExist:
                return HttpResponse("คำสั่งซื้อไม่ถูกต้อง")

            # สร้างออเดอร์ในตาราง Payment
            payment = Payment.objects.create(
                order=order,
                payment_date=now(),  # กำหนดวันที่ชำระเงินเป็นเวลาปัจจุบัน
                payment_status="wait",  # กำหนดสถานะเริ่มต้นเป็น 'รอการตรวจสอบ'
                image_payment=image  # อัปโหลดไฟล์สลิป
            )

            return HttpResponse(f"อัปโหลดสลิปสำเร็จ! {payment.image_payment.url}")  

    # ดึงคำสั่งซื้อทั้งหมดที่ยังไม่มีการชำระเงิน
    orders = Order.objects.exclude(
        order_id__in=Payment.objects.values_list("order_id", flat=True)  # ใช้ order_id ของ Order
    )
    
    # หากไม่มีคำสั่งซื้อในระบบ
    if not orders:
        return render(request, 'payment.html', {'message': 'โปรดเลือกรายการจากหน้ารายการ'})
    
    return render(request, 'payment.html', {'orders': orders})
