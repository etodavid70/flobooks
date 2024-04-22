from django.shortcuts import render
from rest_framework import status
# Create your views here.
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
     
from django.core.exceptions import ObjectDoesNotExist



@csrf_exempt
@api_view(['POST'])
def signup(request):
    serializer =  CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        user=serializer.save()
        user.set_password(password)
        user.save()

        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()





class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
           
            user = authenticate(request, email=email, password=password)
            print(email, password, user)
            
            if user is not None:
                login(request, user)
                serializer = CustomUserSerializer(user)
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({'status': 'success', 'message': 'Authentication successful', 'data': {
                    'Authtoken': token.key,
                    'userdata': serializer.data
                }}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@csrf_exempt
def logout_view(request):
    logout(request)

    return JsonResponse({'message': 'User logged out!'})

























 
