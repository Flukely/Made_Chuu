from main import views
from .views import chat
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',views.index),
    path('chat/', chat, name='chat')
]
