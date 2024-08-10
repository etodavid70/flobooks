from rest_framework import serializers
from .models import Customer, Item, Sale, Invoice, Accounts, Purchase, AccountsPurchase

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']



class ItemSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Add this line

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', "quantity","user"]


# class SaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sale
#         fields = ['id', 'customer', 'item', 'amount', 'quantity', 'date', 'status']


class SaleSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    user_business_name = serializers.CharField(source='item.user.businessName', read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'customer', 'item', 'item_name', 'amount', 'quantity', 'date', 'status', 'user_business_name']



class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'item', 'amount', 'quantity', 'date', 'status']


class InventorySerializer(serializers.ModelSerializer):
    # stock = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', "quantity"]

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
        ret['item_name'] = instance.sale.item.name
        return ret

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['sales_id', 'cash_account', 'bank_account']


class AccountsSerializerPurchase(serializers.ModelSerializer):
    class Meta:
        model = AccountsPurchase
        fields = ['purchase_id', 'cash_account', 'bank_account']