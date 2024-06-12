from rest_framework import serializers
from .models import CustomUser, UserPhoto


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True}  # Password is write-only(displayed)
        }



class PhotoSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model= UserPhoto
        fields =['user', 'business_logo']


class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()




# class SubuserSerializer(serializers.ModelSerializer):
#     class Meta:

#         model = Subuser
#         fields =["subuser_name","subuser_email", "subuser_password"]
