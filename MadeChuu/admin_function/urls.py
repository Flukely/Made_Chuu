from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from admin_function import views


urlpatterns = [
    path('Dashboard', staff_member_required(views.dashboard_admin), name='admin_dashboard'),
    path('Comment', staff_member_required(views.comment_admin), name='admin_comment'),
    path('add_reply/', views.add_reply, name='add_reply'),
]