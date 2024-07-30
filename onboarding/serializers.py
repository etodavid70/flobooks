from rest_framework import serializers
from .models import CustomUser, UserPhoto

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
    'password': {'write_only': True}  # Password is write-only(displayed)
}
    def validate_present_package(self, value):
        valid_choices = [choice[0] for choice in CustomUser.PACKAGE_CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(f"Invalid present_package. Expected one of: {valid_choices}")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


class PhotoSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model= UserPhoto
        fields =['user', 'business_logo']
