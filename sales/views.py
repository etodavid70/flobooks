from django.shortcuts import render
from rest_framework import serializers
from rest_framework.exceptions import NotFound


# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Sale, Invoice, Item, Customer, Purchase
from tax.models import VAT

from decimal import Decimal

from .serializers import SaleSerializer, InvoiceSerializer, ItemSerializer, CustomerSerializer, AccountsSerializer, PurchaseSerializer
from .serializers import InventorySerializer, AccountsSerializerPurchase
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from .permissions import IsBaseUserOrSubuser
from decimal import Decimal


#for sales

class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    permission_classes = [IsAuthenticated, IsBaseUserOrSubuser]


    def perform_create(self, serializer):
        user = self.request.user
        sale = serializer.save()
        item = sale.item

        # Check if there is enough stock
        if item.quantity < sale.quantity:

            raise serializers.ValidationError("Not enough stock available.")

        # Decrease the item's quantity by the quantity sold
        item.quantity -= sale.quantity

        # Save the updated item
        item.save()

        total_amount = sale.amount * sale.quantity

        vat_amount = Decimal('0.00')




        if user.start_tax:
            vat_percentage = Decimal('0.075')

            # Calculate VAT (7.5% of total_amount)
            vat_amount = vat_percentage * total_amount

            # Assuming a single VAT record
            vat_record, created = VAT.objects.get_or_create(id=1)
            vat_record.add_vat(vat_amount)


        Invoice.objects.create(sale=sale, total_amount=total_amount,
        status=sale.status)
        # Store vat_amount in the serializer context so it can be returned in the response
        self.vat_amount = vat_amount

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
            # Add VAT amount to the response
        response.data['vat_amount'] = str(self.vat_amount)  # Convert Decimal to string
        return response



class UserSalesListView(generics.ListAPIView):
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        # Filter sales by items owned by the current user
        return Sale.objects.filter(item__user=user)


#for purchases

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


class UserPurchasesListView(generics.ListAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        # Filter purchases by items owned by the current user
        return Purchase.objects.filter(item__user=user)


#for invoice

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


# for items and inventory

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



class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsBaseUserOrSubuser]

    def get_queryset(self):
        # Ensure that the user can only edit or delete their own items
        return self.queryset.filter(user=self.request.user)

    # def delete(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class InventoryListView(generics.ListAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsBaseUserOrSubuser]

    def get_queryset(self):
        user = self.request.user
        return Item.objects.filter(user=user)


class ItemQueryView(generics.GenericAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        item_id = request.query_params.get('id')
        if not item_id:
            return Response({"error": "ID query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Item.objects.get(pk=item_id, user=request.user)
            serializer = self.get_serializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            raise NotFound("Item not found.")





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