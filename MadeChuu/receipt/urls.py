from django.urls import path
from receipt import views

app_name = "receipt"

urlpatterns = [
    path('', views.index, name='index'),
    path('receipt/<int:receipt_id>/', views.receipt, name='receipt'),  # ใช้ receipt_id ใน URL
]