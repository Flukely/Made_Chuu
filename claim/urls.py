from django.urls import path
from .views import *

app_name = 'claim'

urlpatterns = [
    path('<int:order_id>/', claim_request, name='claim_request'),
    path('claim_status/<int:claim_id>/', claim_status, name='claim_status'),
    path('claim_success/<int:claim_id>/', claim_success, name='claim_success'),
    path('cancel_claim/<int:claim_id>/', cancel_claim, name='cancel_claim'),
]