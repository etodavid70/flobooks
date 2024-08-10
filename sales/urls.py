from django.urls import path
from .views import SaleCreateView, InvoiceDetailView, ItemCreateView, CustomerCreateView, sales_accounts,purchase_accounts, InventoryListView, PurchaseCreateView

urlpatterns = [
    path('api/sales/', SaleCreateView.as_view(), name='sale_create'),
     path('api/purchase/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('api/invoices/<int:sale__id>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('api/items/', ItemCreateView.as_view(), name='item_create'),
     path('api/customer/', CustomerCreateView.as_view(), name='customer_create'),
     path('api/salesaccounts/', sales_accounts, name='sales_accounts'),
     path('api/purchaseaccounts/', purchase_accounts, name='purchase_accounts'),
    path('api/inventory/', InventoryListView.as_view(), name='inventory'),


]


