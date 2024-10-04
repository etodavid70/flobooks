from django.urls import path
# from .views import VATRetrieveView

# urlpatterns = [
#     path('vat/', VATRetrieveView.as_view(), name='vat-detail'),
# ]

# urls.py
from django.urls import path
from .views import VATRetrieveView, VATStatusView, VATMarkAsPaidView, SetCommencementDateView,  UserStateView, StateURLView


urlpatterns = [
      path('vat/', VATRetrieveView.as_view(), name='vat-detail'),
    path('vat/status/', VATStatusView.as_view(), name='vat-status'),
    path('vat/pay/', VATMarkAsPaidView.as_view(), name='vat-pay'),
    path('vat/commencement/', SetCommencementDateView.as_view(), name='vat-commencement'),
    path('user/state/', UserStateView.as_view(), name='user-state'),
    path('user/state-portal/', StateURLView.as_view(), name='state_url_view'),
]
