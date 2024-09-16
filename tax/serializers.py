# serializers.py
from rest_framework import serializers
from .models import VAT
from onboarding.models import CustomUser

class VATSerializer(serializers.ModelSerializer):
    class Meta:
        model = VAT
        fields = ['total_vat']




class UserStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['state']  # You can include more fields if necessary
