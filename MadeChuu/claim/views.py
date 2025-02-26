from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from main.models import Order, Claim, OrderProduct  # นำเข้าโมเดลจาก main.models
from .forms import ClaimForm

def claim_request(request, order_id=3):  # รองรับทั้ง /claim/ และ /claim/1/
    user = request.user  # ดึงข้อมูลผู้ใช้
    order = get_object_or_404(Order, order_id=order_id, user=user)  # เชื่อมโยงกับผู้ใช้
    orderproduct = get_object_or_404(OrderProduct, order=order)  # ใช้ get_object_or_404 แทน OrderProduct.objects.get

    if request.method == "POST":
        form = ClaimForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.order = order  # เชื่อมโยงกับ Order
            claim.claim_status = "กำลังดำเนินการ"  # กำหนดสถานะเริ่มต้น
            claim.save()

            return redirect(reverse('claim_success', kwargs={'claim_id': claim.claim_id}))  # ใช้ reverse() แก้ปัญหา URL

    else:
        form = ClaimForm()   

    return render(request, 'claim_form.html', {'form': form, 'order': order, 'orderproduct': orderproduct, 'user': user})

def claim_status(request, claim_id=3):
    user = request.user
    claim = get_object_or_404(Claim, claim_id=claim_id, order__user=user)  # กรองตามผู้ใช้
    orderproduct = get_object_or_404(OrderProduct, order=claim.order)  # ใช้ get_object_or_404 แทน OrderProduct.objects.get

    context = {
        'product_image_url': claim.claim_image,
        'product_name': orderproduct.product.product_name,
        'product_price': claim.order.total_price,
        'promtpay_number': claim.promtpay_number,
        'request_datetime': claim.claim_date,
        'request_id': claim.claim_id,
        'reason': claim.reason,
        'order_id': claim.order.order_id,
        'status': claim.claim_status,
    }
    return render(request, 'claim_status.html', context)

def claim_success(request, claim_id=3):
    user = request.user
    claim = get_object_or_404(Claim, claim_id=claim_id, order__user=user)  # เชื่อมโยงกับผู้ใช้
    return render(request, 'claim_success.html', {'claim': claim})


def cancel_claim(request, claim_id):
    claim = get_object_or_404(Claim, pk=claim_id)
    claim.claim_status = "ยกเลิกคำขอ"
    claim.save()
    return redirect('track', order_id=claim.order_id)