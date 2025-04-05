from django.urls import path
from . import views

app_name = 'user_profile'  # กำหนด namespace

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
]