


from .models import Subuser
from rest_framework import serializers
from django.contrib.auth.hashers import check_password, make_password
from onboarding.models import CustomUser


class PackageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['present_package']

    def validate_present_package(self, value):
        valid_choices = [choice[0] for choice in CustomUser.PACKAGE_CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(f"Invalid present_package. Expected one of: {valid_choices}")
        return value

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


class SubuserLoginSerializer(serializers.Serializer):
    subuser_email = serializers.EmailField()
    subuser_password = serializers.CharField(write_only=True)



