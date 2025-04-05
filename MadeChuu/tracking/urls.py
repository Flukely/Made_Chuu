from django.urls import path
from . import views
from tracking.views import track

app_name = 'tracking'

urlpatterns = [
    path('<int:order_id>/', views.track, name='tracking'),
    path('', views.track_view, name='track_view'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('refund/<int:order_id>/', views.refund_info, name='refund_info'),
    path('submit/<int:order_id>/', views.submit_order, name='submit_order'),
]