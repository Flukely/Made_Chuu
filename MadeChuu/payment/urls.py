from django.urls import path
from payment import views

app_name = "payment"  # 🔥 เพิ่มบรรทัดนี้เพื่อกำหนด namespace

urlpatterns = [
    path('', views.payment, name='payment'),
]
