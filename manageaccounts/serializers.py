from .models import Subuser
from rest_framework import serializers
from django.contrib.auth.hashers import check_password, make_password


class SubuserSerializer(serializers.ModelSerializer):
    class Meta:

        model = Subuser
        fields =["subuser_name","subuser_email", "subuser_password"]

        extra_kwargs = {
            'subuser_password': {'write_only': True}  # Password is write-only(displayed)
        }


    def validate_subuser_password(self, value: str) -> str:
        """Hash the subuser_password using make_password."""
        return make_password(value)
    