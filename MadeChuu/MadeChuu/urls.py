from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),  # URL สำหรับ admin site ของ Django
    path('admin_function/', include('admin_function.urls')),  # URL สำหรับ admin_function
    path('', include('main.urls')),  # URL สำหรับแอปหลัก 
    path('review/', include('review.urls')), # URL สำหรับ review
    path('payment/', include('payment.urls')), # URL สำหรับ payment
    path('receipt/', include('receipt.urls')), # URL สำหรับ receipt
    path('tracking/', include('tracking.urls')), # URL สำหรับ tracking
    path('product/', include('product.urls')), # URL สำหรับ product
    path('claim/', include('claim.urls')), # URL สำหรับ claim
    path('chat/', include('chat.urls')), # URL สำหรับ chat
    path('ProductDetail/', include('ProductDetail.urls')), # URL สำหรับ ProductDetail
    path('Cart/', include('Cart.urls')), # URL สำหรับ cart
    path('accounts/', include('accounts.urls')), # URL สำหรับ accounts
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

