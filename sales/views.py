from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Sale, Invoice, Item, Customer
from .serializers import SaleSerializer, InvoiceSerializer, ItemSerializer, CustomerSerializer
from django.http import JsonResponse

# class SaleCreateView(generics.CreateAPIView):
    # queryset = Sale.objects.all()
    # serializer_class = SaleSerializer
# 
    # def perform_create(self, serializer):
        # sale = serializer.save()
        # Invoice.objects.create(sale=sale, total_amount=sale.amount, status=sale.status)

class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def perform_create(self, serializer):
        sale = serializer.save()
        Invoice.objects.create(sale=sale, total_amount=sale.amount * sale.quantity, status=sale.status)  # Adjust total_amount calculation


class InvoiceDetailView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'sale__id'




# class ItemCreateView(generics.CreateAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# from rest_framework.response import Response

class ItemCreateView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        item = Item.objects.get(pk=serializer.data['id'])
        response_serializer = ItemSerializer(item)
        response_data = response_serializer.data
        response_data.pop('user', None)  # Remove user from response data
        return JsonResponse(response_data, status=status.HTTP_201_CREATED, headers=headers, safe=False)



class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        customer= Customer.objects.get(pk=serializer.data['id'])
        response_serializer = CustomerSerializer(customer)
        response_data = response_serializer.data
        response_data.pop('user', None)  # Remove user from response data
        return JsonResponse(response_data, status=status.HTTP_201_CREATED, headers=headers, safe=False)

