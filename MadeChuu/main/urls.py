from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),  # หน้าแรก
    path('payment/', views.payment, name='payment'),  # หน้า ชำระเงิน
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)