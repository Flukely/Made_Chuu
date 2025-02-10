from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main import models

@staff_member_required
def dashboard_admin(request):
    return render(request, 'Dashboard.html')

@staff_member_required
def comment_admin(request):
    reviews = models.Review.objects.all()
    products = models.Product.objects.all()
    return render(request, 'CommentAdmin.html', {'reviews': reviews, 'products': products})

@csrf_exempt
def add_reply(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        reply_text = request.POST.get('reply_text')

        try:
            review = models.Review.objects.get(review_id=review_id)
            review.review_text_admin = reply_text
            review.save()
            return redirect('admin_comment')
        except models.Review.DoesNotExist:
            return redirect('admin_comment')

    return redirect('admin_comment')