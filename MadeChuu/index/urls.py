# filepath: /c:/Users/milk/OneDrive - Naresuan University/เดสก์ท็อป/MadeChuu/MadeChuu/index/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]