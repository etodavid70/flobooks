from django.shortcuts import render
from rest_framework import serializers

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Sale, Invoice, Item, Customer, Purchase
from .serializers import SaleSerializer, InvoiceSerializer, ItemSerializer, CustomerSerializer, AccountsSerializer, PurchaseSerializer
from .serializers import InventorySerializer, AccountsSerializerPurchase
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from .permissions import IsBaseUserOrSubuser



class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    permission_classes = [IsAuthenticated, IsBaseUserOrSubuser]


    def perform_create(self, serializer):
        sale = serializer.save()
        item = sale.item

        # Check if there is enough stock
        if item.quantity < sale.quantity:

            raise serializers.ValidationError("Not enough stock available.")

        # Decrease the item's quantity by the quantity sold
        item.quantity -= sale.quantity

        # Save the updated item
        item.save()

        Invoice.objects.create(sale=sale, total_amount=sale.amount * sale.quantity,
        status=sale.status)  # Adjust total_amount calculation


class PurchaseCreateView(generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    permission_classes = [IsAuthenticated, IsBaseUserOrSubuser]

    def perform_create(self, serializer):
        purchase = serializer.save()

        item = purchase.item




        # Decrease the item's quantity by the quantity sold
        item.quantity += purchase.quantity

        # Save the updated item
        item.save()

class InventoryListView(generics.ListAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsBaseUserOrSubuser]

    def get_queryset(self):
        user = self.request.user
        return Item.objects.filter(user=user)

# class UserInventoryListView(generics.ListAPIView):
#     serializer_class = InventorySerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Item.objects.filter(user=user)
#


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
    permission_classes = [IsAuthenticated, IsBaseUserOrSubuser]

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
    permission_classes = [IsAuthenticated, IsBaseUserOrSubuser]

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



@permission_classes([IsAuthenticated, IsBaseUserOrSubuser])
@api_view(['POST'])
def sales_accounts(request):
    if request.method == 'POST':
        serializer = AccountsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"data": serializer.data, "message": "successfully posted an account"}, status=status.HTTP_201_CREATED)
        return JsonResponse({"status": "error", "message": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated, IsBaseUserOrSubuser])
@api_view(['POST'])
def purchase_accounts(request):
    if request.method == 'POST':
        serializer = AccountsSerializerPurchase(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"data": serializer.data, "message": "successfully posted an account"}, status=status.HTTP_201_CREATED)
        return JsonResponse({"status": "error", "message": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)