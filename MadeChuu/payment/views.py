from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from .models import Order, Payment
from .form import Paymentform

def payment(request):
    if request.method == "POST":
        form = Paymentform(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.payment_date = now()
            payment.payment_status = "wait"
            payment.save()
            messages.success(request, "อัปโหลดสลิปสำเร็จ!\nร้านค้ากำลังตรวจสอบคำสั่งซื้อ และแจ้งผลผ่านทางหน้าติดตามสถานะคำสั่งซื้อ")
            return redirect('payment:payment')
    else:
        form = Paymentform()

    return render(request, 'payment.html', {'form': form})