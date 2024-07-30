from rest_framework import serializers
from .models import Customer, Item, Sale, Invoice, Accounts

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name']



class ItemSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Add this line

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', "user"]








# class SaleSerializer(serializers.ModelSerializer):
    # class Meta:
        # model = Sale
        # fields = ['id', 'customer', 'item', 'amount', 'date', 'status']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'customer', 'item', 'amount', 'quantity', 'date', 'status']


class InvoiceSerializer(serializers.ModelSerializer):
    sale = SaleSerializer()

    class Meta:
        model = Invoice
        fields = ['id', 'sale', 'date', 'total_amount', 'status']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('user', None)
        return ret


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['sales_id', 'cash_account', 'bank_account']