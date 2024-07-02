from django.urls import path
from .views import SaleCreateView, InvoiceDetailView, ItemCreateView, CustomerCreateView

urlpatterns = [
    path('api/sales/', SaleCreateView.as_view(), name='sale_create'),
    path('api/invoices/<int:sale__id>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('api/items/', ItemCreateView.as_view(), name='item_create'),
     path('api/customer/', CustomerCreateView.as_view(), name='customer_create'),

]


