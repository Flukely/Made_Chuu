from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.review_page, name='review_page'),
    path('submit_review/<int:product_id>/<int:order_id>/', views.submit_review, name='submit_review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
