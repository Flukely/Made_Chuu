from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .form import PaymentForm  # Ensure the correct import
from main.models import Order, Receipt, PaymentStatus, StatusOrder

@login_required
def payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES, user=request.user)  # Pass the user to the form
        if form.is_valid():
            payment = form.save(commit=False)
            payment.payment_date = now()
            payment.payment_status = get_object_or_404(PaymentStatus, payment_status_name="รอการตรวจสอบ")
            
            if not payment.order_id:
                messages.error(request, "ไม่พบคำสั่งซื้อ กรุณาลองใหม่อีกครั้ง")
                return redirect('payment:payment')
            
            payment.save()
            
            # Update the order status here
            order = get_object_or_404(Order, order_id=payment.order_id)
            order.status_order = get_object_or_404(StatusOrder, status_name="ตรวจสอบจ่ายเงิน")  # Change the status to "Waiting"
            order.save()
            
            messages.success(request, "อัปโหลดสลิปสำเร็จ!\nร้านค้ากำลังตรวจสอบคำสั่งซื้อ และแจ้งผลผ่านทางหน้าติดตามสถานะคำสั่งซื้อ")
            return redirect('payment:payment')
        else:
            messages.error(request, "กรุณากรอกข้อมูลการชำระเงินให้ครบถ้วน")
    else:
        form = PaymentForm(user=request.user)  # Pass the user to the form

    return render(request, 'payment.html', {'form': form})