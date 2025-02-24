from django.urls import path
from receipt import views

app_name = "receipt"

urlpatterns = [
    path('check/', views.check_receipt, name='check_receipt'),  # หน้าตรวจสอบใบเสร็จ
    path('<int:order_id>/', views.receipt, name='receipt'),  # ตรวจสอบใบเสร็จจาก order_id
]