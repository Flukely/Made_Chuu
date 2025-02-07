from django.urls import path
from receipt import views

app_name = "receipt"

urlpatterns = [
    path('', views.index, name='index'),
    path('receipt/<int:user_id>/', views.receipt, name='receipt'),  # ใช้ user_id ใน URL
]
