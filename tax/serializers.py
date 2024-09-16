# serializers.py
from rest_framework import serializers
from .models import VAT

class VATSerializer(serializers.ModelSerializer):
    class Meta:
        model = VAT
        fields = ['total_vat']
