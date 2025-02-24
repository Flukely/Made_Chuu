from django.shortcuts import render, redirect, get_object_or_404
from main.models import Order, Claim, OrderProduct  # นำเข้าโมเดลจาก main.models
from .forms import ClaimForm

def claim_request(request, order_id=1):
    user_id = request.session.get('user_id')  # รองรับทั้ง /claim/ และ /claim/1/
    order = get_object_or_404(Order, order_id=order_id)
    orderproduct = get_object_or_404(OrderProduct, order=order)  # ใช้ get_object_or_404 แทน OrderProduct.objects.get
    if request.method == "POST":
        form = ClaimForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            if order:
                claim.order = order  # ถ้ามี Order ให้เชื่อมโยง
            claim.claim_status = "กำลังดำเนินการ"  # Set initial status
            claim.save()
            return redirect('claim_success', claim_id=claim.claim_id)  # เปลี่ยนไปยังหน้า claim_success
    else:
        form = ClaimForm()

    return render(request, 'claim_form.html', {'form': form, 'order': order, 'orderproduct': orderproduct})

def claim_status(request, claim_id=1):
    user_id = request.session.get('user_id')
    claim = get_object_or_404(Claim, claim_id=claim_id)  # ใช้ get_object_or_404 แทน Claim.objects.get
    orderproduct = get_object_or_404(OrderProduct, order_id=claim.order.order_id)  # ใช้ get_object_or_404 แทน OrderProduct.objects.get
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
    user_id = request.session.get('user_id')
    claim = get_object_or_404(Claim, claim_id=claim_id)
    return render(request, 'claim_success.html', {'claim': claim})

