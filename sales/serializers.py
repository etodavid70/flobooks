from rest_framework import serializers
from .models import Customer, Item, Sale, Invoice, Accounts, Purchase, AccountsPurchase

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phoneNumber', 'address']  # Include 'id' to make updates easier

    def create(self, validated_data):
        # Create a customer instance
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update the customer instance
        instance.name = validated_data.get('name', instance.name)
        instance.phoneNumber = validated_data.get('phoneNumber', instance.phoneNumber)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance


class ItemSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Add this line
    date_registered = serializers.ReadOnlyField()

    class Meta:
        model = Item
        fields = ['id', "date_registered", 'name', 'price', "quantity", "user"]





# class SaleSerializer(serializers.ModelSerializer):
#     item_name = serializers.CharField(source='item.name', read_only=True)
#     unitPrice = serializers.CharField(source='item.price', read_only=True)
#     userBusinessName = serializers.CharField(source='item.user.businessName', read_only=True)


#     class Meta:
#         model = Sale
#         fields = ['id', 'customer', 'date', "item", 'item_name',  'unitPrice', 'quantity', 'amount',  'status', "userBusinessName"]


class SaleSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    unitPrice = serializers.CharField(source='item.price', read_only=True)
    userBusinessName = serializers.CharField(source='item.user.businessName', read_only=True)


    class Meta:
        model = Sale
        fields = ['id', 'customer', 'date', 'item_name',  'unitPrice', 'quantity',  'status', "userBusinessName"]



class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'item', 'amount', 'quantity', 'date', 'status']


class InventorySerializer(serializers.ModelSerializer):
    # stock = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', "date_registered", 'name', "quantity"]

    # def get_stock(self, obj):
    #     return obj.quantity




# class InvoiceSerializer(serializers.ModelSerializer):
#     sale = SaleSerializer()

#     class Meta:
#         model = Invoice
#         fields = ['id', 'sale', 'date', 'total_amount', 'status']

#     def to_representation(self, instance):
#         ret = super().to_representation(instance)
#         ret.pop('user', None)
#         return ret


# class InvoiceSerializer(serializers.ModelSerializer):
#     sale = SaleSerializer()

#     class Meta:
#         model = Invoice
#         fields = ['id', 'sale', 'date', 'total_amount', 'status']

#     def to_representation(self, instance):
#         ret = super().to_representation(instance)
#         ret['business_name'] = instance.sale.item.user.businessName
#         ret['business_address'] = instance.sale.item.user.businessAddress
#         ret['business_phoneNumber'] = instance.sale.item.user.phoneNumber
#         ret['business_email'] = instance.sale.item.user.email

#         # ret['item_name'] = instance.sale.item.name
#         # ret['unit_price'] = instance.sale.item.price
#         return ret



class InvoiceSerializer(serializers.ModelSerializer):
    sales = SaleSerializer(many=True)  # Many sales per invoice

    class Meta:
        model = Invoice
        fields = ['id', 'sales', 'date', 'total_amount', 'status']

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # Since multiple sales belong to the same user, we can get the business info from the first sale's item user
        first_sale = instance.sales.first()
        ret['business_name'] = first_sale.item.user.businessName
        ret['business_address'] = first_sale.item.user.businessAddress
        ret['business_phoneNumber'] = first_sale.item.user.phoneNumber
        ret['business_email'] = first_sale.item.user.email

        return ret


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['sales_id', 'cash_account', 'bank_account']


class AccountsSerializerPurchase(serializers.ModelSerializer):
    class Meta:
        model = AccountsPurchase
        fields = ['purchase_id', 'cash_account', 'bank_account']