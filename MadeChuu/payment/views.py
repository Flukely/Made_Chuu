from django.shortcuts import render, redirect # นำเข้าฟังก์ชัน render และ redirect จาก Django
from django.contrib import messages # นำเข้าฟังก์ชัน messages จาก Django
from django.utils.timezone import now # นำเข้าฟังก์ชัน now จาก Django
from .form import Paymentform # นำเข้าฟอร์ม Paymentform จากไฟล์ form.py

# ฟังก์ชันสำหรับจัดการการชำระเงิน
def payment(request): # ประกาศฟังก์ชัน payment รับ request เป็นพารามิเตอร์
    if request.method == "POST":  # ตรวจสอบว่ามีการส่งฟอร์มแบบ POST หรือไม่
        form = Paymentform(request.POST, request.FILES)  # รับข้อมูลจากฟอร์ม
        if form.is_valid():  # ตรวจสอบว่าข้อมูลที่กรอกถูกต้องหรือไม่
            payment = form.save(commit=False)  # บันทึกข้อมูลแต่ยังไม่ commit เข้า DB
            payment.payment_date = now()  # กำหนดวันที่ชำระเงินเป็นเวลาปัจจุบัน
            payment.payment_status = "wait"  # กำหนดสถานะเริ่มต้นเป็น "รอตรวจสอบ"
            payment.save()  # บันทึกข้อมูลลงฐานข้อมูล
            messages.success(request, "อัปโหลดสลิปสำเร็จ!\nร้านค้ากำลังตรวจสอบคำสั่งซื้อ และแจ้งผลผ่านทางหน้าติดตามสถานะคำสั่งซื้อ")  # แสดงข้อความแจ้งเตือนเมื่ออัปโหลดสำเร็จ
            return redirect('payment:payment')  # รีไดเรกไปยังหน้าชำระเงินอีกครั้ง
    else: # ถ้าเป็น GET
        form = Paymentform()  # ถ้าเป็น GET ให้แสดงฟอร์มเปล่า

    return render(request, 'payment.html', {'form': form})  # ส่งฟอร์มไปยัง template 'payment.html'