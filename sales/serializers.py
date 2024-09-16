from rest_framework import serializers
from .models import Customer, Item, Sale, Invoice, Accounts, Purchase, AccountsPurchase

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']



class ItemSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Add this line
    date_registered = serializers.ReadOnlyField()

    class Meta:
        model = Item
        fields = ['id', "date_registered", 'name', 'price', "quantity", "user"]


# class SaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sale
#         fields = ['id', 'customer', 'item', 'amount', 'quantity', 'date', 'status']


class SaleSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    unitPrice = serializers.CharField(source='item.price', read_only=True)
    userBusinessName = serializers.CharField(source='item.user.businessName', read_only=True)


    class Meta:
        model = Sale
        fields = ['id', 'customer', 'date', 'item', 'item_name',  'unitPrice', 'quantity', 'amount',  'status', "userBusinessName"]




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


class InvoiceSerializer(serializers.ModelSerializer):
    sale = SaleSerializer()

    class Meta:
        model = Invoice
        fields = ['id', 'sale', 'date', 'total_amount', 'status']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['business_name'] = instance.sale.item.user.businessName
        ret['business_address'] = instance.sale.item.user.businessAddress
        ret['business_phoneNumber'] = instance.sale.item.user.phoneNumber
        ret['business_email'] = instance.sale.item.user.email

        # ret['item_name'] = instance.sale.item.name
        # ret['unit_price'] = instance.sale.item.price
        return ret

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['sales_id', 'cash_account', 'bank_account']


class AccountsSerializerPurchase(serializers.ModelSerializer):
    class Meta:
        model = AccountsPurchase
        fields = ['purchase_id', 'cash_account', 'bank_account']