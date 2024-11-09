from django.urls import path
from .views import SaleCreateView, InvoiceDetailView, ItemCreateView, CustomerCreateView, sales_accounts,purchase_accounts, InventoryListView, PurchaseCreateView, SaleCreateCreditView
from .views import ItemDetailView, ItemQueryView, UserSalesListView, UserPurchasesListView, CustomerDetailView, CustomerNameIdView,ItemNameIdView

urlpatterns = [
    path('api/sales/', SaleCreateView.as_view(), name='sale_create'),
     path('api/sales-credit/', SaleCreateCreditView.as_view(), name='sale_credit'),

     path('customers/', CustomerCreateView.as_view(), name='customer-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
      path('customer-dropdpown/', CustomerNameIdView.as_view(), name='customer-name-id'),

     path('api/purchase/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('api/invoices/<int:sale__id>/', InvoiceDetailView.as_view(), name='invoice_detail'),


    path('api/items/', ItemCreateView.as_view(), name='item_create'),
    path('api/items-dropdown/',  ItemNameIdView.as_view(), name='item-name-id'),



    #  path('api/customer/', CustomerCreateView.as_view(), name='customer_create'),
     path('api/salesaccounts/', sales_accounts, name='sales_accounts'),
     path('api/purchaseaccounts/', purchase_accounts, name='purchase_accounts'),
    path('api/inventory/', InventoryListView.as_view(), name='inventory'),
 path('api/products/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
  path('api/product-query/', ItemQueryView.as_view(), name='item-query'),
  path('api/all-sales/', UserSalesListView.as_view(), name='user-sales'),
    path('api/all-purchases/', UserPurchasesListView.as_view(), name='user-purchases'),


]


