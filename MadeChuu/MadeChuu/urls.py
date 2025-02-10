from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('payment/', include('payment.urls')),
    path('receipt/', include('receipt.urls')),  # เพิ่มบรรทัดนี้เพื่อรวม URL pattern ของแอป receipt
]