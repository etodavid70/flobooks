from rest_framework import serializers
from .models import AddEntry

class AddEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddEntry
        fields = ['title', 'debit', 'credit']  # Exclude 'user' field here
