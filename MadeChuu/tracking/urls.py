from django.urls import path
from . import views
from tracking.views import track

urlpatterns = [
    path('', views.track, name='track'),
]