from django.shortcuts import render, redirect # นำเข้าฟังก์ชัน render และ redirect จาก Django
from django.contrib import messages 
from django.utils.timezone import now 
from .form import PaymentForm 
from main.models import Order  # นำเข้าโมเดล Order

# ฟังก์ชันสำหรับจัดการการชำระเงิน
def payment(request): 
    if request.method == "POST":  
        form = PaymentForm(request.POST, request.FILES)  # รับข้อมูลจากฟอร์ม
        if form.is_valid():  # ตรวจสอบว่าข้อมูลที่กรอกถูกต้องหรือไม่
            payment = form.save(commit=False)  # บันทึกข้อมูลแต่ยังไม่ commit เข้า DB
            payment.payment_date = now()  # กำหนดวันที่ชำระเงินเป็นเวลาปัจจุบัน
            payment.payment_status = "รอการตรวจสอบ"  # กำหนดสถานะเริ่มต้นเป็น "รอตรวจสอบ"
            
            # ตรวจสอบว่ามี order_id ใน request.POST หรือไม่ หากไม่มีให้ใช้ order_id จาก session
            order_id = request.POST.get('order_id') or request.session.get('order_id')
            if order_id:
                payment.order_id = order_id  # กำหนด order_id ให้กับ payment
            else:
                messages.error(request, "ไม่พบคำสั่งซื้อ กรุณาลองใหม่อีกครั้ง")
                return redirect('payment:payment')
            
            payment.save()  # บันทึกข้อมูลลงฐานข้อมูล
            messages.success(request, "อัปโหลดสลิปสำเร็จ!\nร้านค้ากำลังตรวจสอบคำสั่งซื้อ และแจ้งผลผ่านทางหน้าติดตามสถานะคำสั่งซื้อ")  # แสดงข้อความแจ้งเตือนเมื่ออัปโหลดสำเร็จ
            return redirect('payment:payment')  # รีไดเรกไปยังหน้าชำระเงินอีกครั้ง
    else: # ถ้าเป็น GET
        form = PaymentForm()  

    return render(request, 'payment.html', {'form': form})  # ส่งฟอร์มไปยัง template 'payment.html'