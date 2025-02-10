from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),  # URL สำหรับ admin site ของ Django
    path('admin_function/', include('admin_function.urls')),  # URL สำหรับ admin_function
    path('', include('main.urls')),  # URL สำหรับแอปหลัก
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)