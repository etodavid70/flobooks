from django.urls import path
from .views import AddEntryCreateView, AddEntryListView

urlpatterns = [
    path('general_ledger/add-entry/', AddEntryCreateView.as_view(), name='add-entry'),
    path('general_ledger/data/', AddEntryListView.as_view(), name='user-entries'),
]
