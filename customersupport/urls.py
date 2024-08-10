# urls.py

from django.urls import path
from .views import CreateSupportRequest

urlpatterns = [
    path('request-support/', CreateSupportRequest.as_view(), name='create_support_request'),

]
