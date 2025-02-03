from django.urls import path
from main import views
from .views import chat

urlpatterns = [
    path('',views.index),
    path('chat/', chat, name='chat')
]
