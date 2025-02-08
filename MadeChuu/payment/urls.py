from django.urls import path # นำเข้าฟังก์ชัน path จาก Django
from payment import views # 🔥 เพิ่มบรรทัดนี้เพื่อเรียกใช้ views จาก payment

app_name = "payment"  # 🔥 เพิ่มบรรทัดนี้เพื่อกำหนด namespace

urlpatterns = [ # กำหนด URL ของแอปพลิเคชัน payment
    path('', views.payment, name='payment'), # 🔥 เพิ่มบรรทัดนี้เพื่อกำหนด path สำหรับหน้า payment
]
