from django.shortcuts import render
from rest_framework import status
# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.utils.decorators import method_decorator

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


from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


     
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from django.middleware.csrf import get_token

@csrf_exempt
def getToken(request):
    csrf_token = get_token(request)


    print("CSRF Token:", csrf_token)
    return JsonResponse({"csrf token": csrf_token})

@csrf_exempt
@api_view(['POST'])
def signup(request):
    serializer =  CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        user=serializer.save()
        user.set_password(password)
        user.save()

        return JsonResponse({'email': serializer.data['email']}, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
           
            user = authenticate(request, email=email, password=password)
            # print(email, password, user)
            
            if user is not None:
                login(request, user)
                serializer = CustomUserSerializer(user)
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({'status': 'success', 'message': 'Authentication successful, user logged in', 'data': {
                    'Authtoken': token.key,
                    'user_email': serializer.data['email']
                }}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@csrf_exempt
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'message': 'User logged out!'})

    else:
        return JsonResponse({'message': 'forbiddden'}, status=status.HTTP_403_FORBIDDEN)





 

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_users_data(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        user = CustomUser.objects.get(email=user_email)
        serializer = CustomUserSerializer(user)
        
        return JsonResponse({'status': 'success', 'message': 'Authorization successful, users data fetched succesfully', 'data': {
           
            'userData': serializer.data,
             'totalSales': '0',
            'totalPurchases': '0',
            'taxReturns': '0',
            'inventory': '0'
        }}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

from django.contrib.auth import logout
    

from django.core.mail import send_mail
class SendMailSerializer(serializers.Serializer):
    email = serializers.EmailField()

@api_view(['POST'])
@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
       
        send_mail(
            subject='Welcome to My Service! Please Confirm Your Email',
            # message=f'Click the link below to confirm your email address:\n{link}',
            message='Click the link below to confirm your email address:\n',
            from_email='etodavid94@gmail.com',
            recipient_list=[email],
            fail_silently=True,  # Raise an exception on sending failure
        )

        return JsonResponse({'data': "successfully sent email"})
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












 
