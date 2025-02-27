from django.urls import path
from . import views
from tracking.views import track

urlpatterns = [
    path('<int:order_id>/', views.track, name='tracking'),
    path('', views.track_view, name='track_view'),
]