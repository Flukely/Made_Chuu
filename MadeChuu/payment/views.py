from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from .models import Order, Payment
from .form import Payment

def payment(request):
    if request.method == "POST":
        form = Payment(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.payment_date = now()
            payment.payment_status = "wait"
            payment.save()
            messages.success(request, "อัปโหลดสลิปสำเร็จ!")
            return redirect('payment:payment')
    else:
        form = Payment()

    return render(request, 'payment.html', {'form': form})
