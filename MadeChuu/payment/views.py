from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .form import PaymentForm
from main.models import Order, PaymentStatus, StatusOrder
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    # ตรวจสอบว่ามีการชำระเงินสำหรับคำสั่งซื้อนี้แล้วหรือไม่
    if hasattr(order, 'payment') and order.payment:
        messages.info(request, "คำสั่งซื้อนี้ได้รับการชำระเงินแล้ว")
        return redirect('receipt:check_receipt')
    
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # ตรวจสอบอีกครั้งเพื่อป้องกันการส่งซ้ำ
            if hasattr(order, 'payment') and order.payment:
                messages.info(request, "คำสั่งซื้อนี้ได้รับการชำระเงินแล้ว")
                return redirect('receipt:check_receipt')
                
            payment = form.save(commit=False)
            payment.payment_date = now()
            payment_status, created = PaymentStatus.objects.get_or_create(
                payment_status_name="รอการตรวจสอบ",
                defaults={'payment_status_name': "รอการตรวจสอบ"}
            )
            payment.payment_status = payment_status
            payment.order = order
            payment.save()

            status_order, created = StatusOrder.objects.get_or_create(
                status_name="ตรวจสอบจ่ายเงิน",
                defaults={'status_name': "ตรวจสอบจ่ายเงิน"}
            )
            order.status_order = status_order
            order.save()

            messages.success(request, "อัปโหลดสลิปสำเร็จ! ร้านค้ากำลังตรวจสอบคำสั่งซื้อ")
            return redirect('payment:payment', order_id=order_id)
        else:
            messages.error(request, "กรุณากรอกข้อมูลการชำระเงินให้ครบถ้วน")
    else:
        form = PaymentForm(user=request.user)

    return render(request, 'payment.html', {
        'form': form,
        'order_id': order_id,
        'shop_qr_code': order.shop.qr_code.url if order.shop.qr_code else None
    })