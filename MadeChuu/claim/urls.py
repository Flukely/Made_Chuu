from django.urls import path
from .views import *

urlpatterns = [
    #path('', claim_request, name='claim_request_default'),  # รองรับ /claim/
    path('<int:order_id>/', claim_request, name='claim_request'),  # รองรับ /claim/1/
    path('', claim_request, name='claim_request_default'),  # รองรับ /claim/
    path('claim_status/<int:claim_id>/', claim_status, name='claim_status'),
    path('claim_success/<int:claim_id>/', claim_success, name='claim_success'),
    path('cancel_claim/<int:claim_id>/', cancel_claim, name='cancel_claim'),
    

    
]