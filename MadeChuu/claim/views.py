from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from main.models import Order, Claim, OrderProduct, ClaimStatus, StatusOrder
from .forms import ClaimForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def claim_request(request, order_id):
    user = request.user
    order = get_object_or_404(Order, order_id=order_id, user=user)
    orderproduct = OrderProduct.objects.filter(order=order)

    if request.method == "POST":
        form = ClaimForm(request.POST, request.FILES)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.order = order
            
            # Get or create the default claim status
            claim_status, created = ClaimStatus.objects.get_or_create(
                claim_status_name="กำลังดำเนินการ",
                defaults={'claim_status_name': "กำลังดำเนินการ"}
            )
            claim.claim_status = claim_status
            claim.save()

            # Get or create the order status
            order_status, created = StatusOrder.objects.get_or_create(
                status_name="เคลม",
                defaults={'status_name': "เคลม"}
            )
            order.status_order = order_status
            order.save()

            return redirect(reverse('claim:claim_success', kwargs={'claim_id': claim.claim_id}))

    else:
        form = ClaimForm()

    return render(request, 'claim_form.html', {'form': form, 'order': order, 'orderproduct': orderproduct, 'user': user})

@login_required(login_url='/login/')
def claim_status(request, claim_id):
    user = request.user
    claim = get_object_or_404(Claim, claim_id=claim_id, order__user=user)
    orderproduct = OrderProduct.objects.filter(order=claim.order)

    context = {
        'product_image_url': claim.claim_image,
        'orderproduct': orderproduct,
        'product_price': claim.order.total_price,
        'promtpay_number': claim.promtpay_number,
        'request_datetime': claim.claim_date,
        'request_id': claim.claim_id,
        'reason': claim.reason,
        'order_id': claim.order.order_id,
        'status': claim.claim_status.claim_status_name,
    }
    return render(request, 'claim_status.html', context)

@login_required(login_url='/login/')
def claim_success(request, claim_id):
    user = request.user
    claim = get_object_or_404(Claim, claim_id=claim_id, order__user=user)
    return render(request, 'claim_success.html', {'claim': claim})

@login_required(login_url='/login/')
def cancel_claim(request, claim_id):
    claim = get_object_or_404(Claim, pk=claim_id)
    order = claim.order  # ดึง order โดยตรงจาก claim

    # เปลี่ยนสถานะเคลมเป็น "ยกเลิกคำขอ"
    claim.claim_status = get_object_or_404(ClaimStatus, claim_status_name="ยกเลิกคำขอ")
    claim.save()
    
    # เปลี่ยนสถานะออเดอร์กลับเป็น "จัดส่งสำเร็จ"
    order.status_order = get_object_or_404(StatusOrder, status_name="จัดส่งสำเร็จ")
    order.save()

    # ใช้ reverse() เพื่อ redirect ไปยังหน้า track โดยส่ง order_id
    return redirect(reverse('tracking:tracking', kwargs={'order_id': order.order_id}))

@login_required(login_url='/login/')
def claim_conditions(request):
    return render(request, 'Claim_conditions.html')
    