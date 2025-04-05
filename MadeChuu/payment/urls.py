from django.urls import path
from . import views

app_name = 'payment'  # กำหนด namespace เป็น 'payment'

urlpatterns = [
    path('<int:order_id>/', views.payment, name='payment'),  # URL pattern สำหรับการชำระเงิน
]