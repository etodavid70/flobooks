from django.shortcuts import render
from rest_framework import serializers
from rest_framework.exceptions import NotFound


# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Sale, Invoice, Item, Customer, Purchase, AccountsReceivable
from tax.models import VAT

from decimal import Decimal

from .serializers import SaleSerializer, InvoiceSerializer, ItemSerializer, CustomerSerializer, AccountsSerializer, PurchaseSerializer
from .serializers import InventorySerializer, AccountsSerializerPurchase
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from .permissions import IsBaseUserOrSubuser
from decimal import Decimal
from rest_framework.views import APIView


class ItemNameIdView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        # Fetch items assigned to the logged-in user
        items = Item.objects.filter(user=request.user)

        # Create a dictionary with item name as key and id as value
        item_dict = {item.name: item.id for item in items}

        # Return the dictionary as a JSON response
        return Response(item_dict)

class CustomerNameIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch all customers
        customers  = Customer.objects.filter(user=request.user)


        # Create a dictionary with customer name as key and id as value
        customer_dict = {customer.name: customer.id for customer in customers}

        # Return the dictionary as a JSON response
        return Response(customer_dict)

class CustomerCreateView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter customers by the authenticated user
        return self.queryset.filter(user=self.request.user)


class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsBaseUserOrSubuser]

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data

        items = data.get('items', [])
        cash_payment = Decimal(data.get('cash', 0))
        bank_payment = Decimal(data.get('bank', 0))
        total_payment = cash_payment + bank_payment

        total_cost_of_goods = Decimal('0.00')
        created_sales = []  # Collect sales created

        for item_data in items:
            item_id = item_data.get('item')
            quantity = item_data.get('quantity')

            # Fetch the item by item ID
            try:
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                raise serializers.ValidationError(f"Item with id {item_id} does not exist.")

            # Calculate the total cost for this item (unit price * quantity)
            item_cost = item.price * quantity
            total_cost_of_goods += item_cost

            # Check if there is enough stock for each item
            if item.quantity < quantity:
                raise serializers.ValidationError(f"Not enough stock available for item {item.name}.")

            # Decrease the item's quantity by the quantity sold
            item.quantity -= quantity
            item.save()

            # Create a sale for each item and add it to the created_sales list
            sale = Sale.objects.create(
                customer=data['customer'],
                item=item,
                quantity=quantity,
                amount=item.price * quantity,
                status=data['status']
            )
            created_sales.append(sale)  # Add each sale to the list

        # Check if the customer has paid enough
        if total_payment < total_cost_of_goods:
            raise serializers.ValidationError(f"Total payment {total_payment} is less than the cost of goods bought {total_cost_of_goods}.")

        vat_amount = Decimal('0.00')

        # VAT Calculation if applicable
        if user.start_tax:
            vat_percentage = Decimal('0.075')
            vat_amount = vat_percentage * total_cost_of_goods
            vat_record, created = VAT.objects.get_or_create(id=1)
            vat_record.add_vat(vat_amount)

        # Create an invoice after all sales are saved
        # Invoice.objects.create(
        #     customer=data['customer'],
        #     total_amount=total_cost_of_goods,
        #     status=data['status']
        # )

        # Store the sales and vat_amount in the serializer context
        self.created_sales = created_sales
        self.vat_amount = vat_amount
        self.total_cost_of_goods = total_cost_of_goods

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)

        # Serialize the list of created sales
        sales_serializer = SaleSerializer(self.created_sales, many=True)

        user_details = {
            'business_name': request.user.businessName,
            'email': request.user.email,
            'phone_number': request.user.phoneNumber,
            'address': request.user.businessAddress,

        }

        # Return the response with VAT and total cost of goods
        response = Response({
            'customer': request.data['customer'],

             'user_details': user_details,
            'sales': sales_serializer.data, # Return all created sales
            'vat_amount': str(self.vat_amount),
            'total_cost_of_goods': str(self.total_cost_of_goods),
            'status': request.data['status'],
        })

        return response

class SaleCreateCreditView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsBaseUserOrSubuser]

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data

        # Extract customer ID from the request data
        customer_id = data.get('customer')

        # Fetch the customer object by ID
        try:
            customer = Customer.objects.get(id=customer_id, user=user)
        except Customer.DoesNotExist:
            raise serializers.ValidationError(f"Customer with id {customer_id} does not exist.")

        items = data.get('items', [])
        cash_payment = Decimal(data.get('cash', 0))
        bank_payment = Decimal(data.get('bank', 0))
        total_payment = cash_payment + bank_payment

        total_cost_of_goods = Decimal('0.00')
        created_sales = []  # Collect sales created

        for item_data in items:
            item_id = item_data.get('item')
            quantity = item_data.get('quantity')

            # Fetch the item by item ID
            try:
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                raise serializers.ValidationError(f"Item with id {item_id} does not exist.")

            # Calculate the total cost for this item (unit price * quantity)
            item_cost = item.price * quantity
            total_cost_of_goods += item_cost

            # Check if there is enough stock for each item
            if item.quantity < quantity:
                raise serializers.ValidationError(f"Not enough stock available for item {item.name}.")

            # Decrease the item's quantity by the quantity sold
            item.quantity -= quantity
            item.save()

            # Create a sale for each item and add it to the created_sales list
            sale = Sale.objects.create(
                customer=customer,  # Use the fetched customer object
                item=item,
                quantity=quantity,
                amount=item.price * quantity,
                status='Credit'
            )
            created_sales.append(sale)  # Add each sale to the list

        # Calculate the balance to be paid (total cost of goods - total payment)
        balance = total_cost_of_goods - total_payment

        # Update the user's accounts receivable if the balance is positive (credit sale)
        if balance > 0:
            accounts_receivable, created = AccountsReceivable.objects.get_or_create(user=user)
            accounts_receivable.amount += balance  # Increase the accounts receivable
            accounts_receivable.save()

        vat_amount = Decimal('0.00')

        # VAT Calculation if applicable
        if user.start_tax:
            vat_percentage = Decimal('0.075')
            vat_amount = vat_percentage * total_cost_of_goods
            vat_record, created = VAT.objects.get_or_create(id=1)
            vat_record.add_vat(vat_amount)

        # Store the sales and vat_amount in the serializer context
        self.created_sales = created_sales
        self.vat_amount = vat_amount
        self.total_cost_of_goods = total_cost_of_goods
        self.customer = customer  # Save customer details for the response

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)

        # Serialize the list of created sales
        sales_serializer = SaleSerializer(self.created_sales, many=True)

        user_details = {
            'business_name': request.user.businessName,
            'email': request.user.email,
            'phone_number': request.user.phoneNumber,
            'address': request.user.businessAddress,
        }

        status = "Credit"

        # Return the response with VAT, total cost of goods, and customer details
        response = Response({
            'customer': {
                'id': self.customer.id,
                'name': self.customer.name,
                'phone_number': self.customer.phoneNumber,
                'address': self.customer.address,
            },
            'user_details': user_details,
            'sales': sales_serializer.data,  # Return all created sales
            'vat_amount': str(self.vat_amount),
            'total_cost_of_goods': str(self.total_cost_of_goods),
            'status': status,
        })

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