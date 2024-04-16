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



@csrf_exempt
@api_view(['POST'])
def signup(request):
    serializer =  CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()






@csrf_exempt
@api_view(['POST'])
def login_view(request):
  if request.method == 'POST':
    email = request.data.get('email')
    
    inputpassword = request.data.get('password')
    # statuss= authenticate(request, username=email, password=inputpassword)
    # print(statuss)
    user= CustomUser.objects.get(email=	email)
    
    if inputpassword == user.password:
        serializer = CustomUserSerializer(user)
        token, _ = Token.objects.get_or_create(user=user)
        # print(check_password(password, ))
        return JsonResponse({'status': 'success', 'message': 'Authentication successful', 'data': {
            'Authtoken': token.key,
            'userdata': serializer.data

        }}, status=status.HTTP_200_OK)
    else:
        # Password incorrect
        return JsonResponse({'status': 'failed', 'error': 'Invalid login details'}, status=status.HTTP_401_UNAUTHORIZED)

  else:
      return JsonResponse({'status': 'failed', 'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

      






#in actual fact this will require a csrf token
@csrf_exempt
@api_view(['GET'])
def getUser(request):
    if request.method == 'GET':
        #This gets the email from the request body
        email = request.data.get('email')
        print(email)  # Assuming email is passed as a query parameter
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                serializer = CustomUserSerializer(user)
                return JsonResponse(serializer.data)
            except CustomUser.DoesNotExist:
                return JsonResponse({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'Email parameter is missing'}, status=status.HTTP_404_NOT_FOUND)
        




#GET reequest
#to return all the data
class CustomUserListCreate(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

#GET request
#to return individudal data
class CustomUserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer




#using default django method
class GetUserByEmail(APIView):
    def get(self, request, email):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data)


#using django rest framework
class GetUserByEmail2(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer()
    lookup_field = 'email'

    def get_queryset(self):
        email = self.kwargs['email']
        return CustomUser.objects.filter(email=email)
    


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
           
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



# @csrf_exempt
# @api_view(['POST'])
# def login_view1(request):
#     if request.method == 'POST':
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data.get('email')
#             password = serializer.validated_data.get('password')
#             print(request.headers)
#             user = authenticate(request, username=email, password=password)
#             print(user)
#             if user is not None:
#                 token, _ = Token.objects.get_or_create(user=user)
#                 return JsonResponse({'status': 'success', 'message': 'Authentication successful', 'token': token.key}, status=status.HTTP_200_OK)
#             else:
#                 return JsonResponse({'status': 'failed', 'error': 'Invalid login details'}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return JsonResponse({'status': 'failed', 'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)