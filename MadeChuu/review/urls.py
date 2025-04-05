from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('', views.review_page, name='review_page'),
    path('<int:order_id>/', views.review_page, name='review_page_by_order'),
    path('submit_review/<int:product_id>/<int:order_id>/', views.submit_review, name='submit_review'),
]