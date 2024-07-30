from django.shortcuts import render
from rest_framework import status
# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt,  csrf_protect, ensure_csrf_cookie
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import generics
from .models import CustomUser, UserPhoto
from .serializers import CustomUserSerializer, PhotoSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password


from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken




@csrf_exempt
def getToken(request):
    csrf_token = get_token(request)
    # print("CSRF Token:", csrf_token)
    return JsonResponse({"csrf token": csrf_token})


@api_view(['POST'])
def signup(request):
    serializer =  CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        user=serializer.save()
        user.set_password(password)
        user.save()

        return JsonResponse({'email': serializer.data['email'], "message":"user created successfully "}, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):

    # @method_decorator(csrf_protect)

    def post(self, request):
        # user= request.user
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            # print(email, password, user)

            if user is not None:
                login(request, user)
                serializer = CustomUserSerializer(user)


                photo_serializers=PhotoSerializer(user)

                jwToken = RefreshToken.for_user(user)

                return Response({'status': 'success', 'message': 'Authentication successful, user logged in', 'data': {
                    'jwAccessToken': str(jwToken.access_token),
                    "jwRefreshToken":  str(jwToken),

                    'user_email': serializer.data['email'],
                 "photo": photo_serializers.data['business_logo'],

                }},  status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_protect
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def logout_view(request):

    logout(request)
    return JsonResponse({'message': 'User logged out!'}, status= status.HTTP_200_OK)








@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_users_data(request):

    #this is repetition the isAuthenticated decorator handles this already
    if request.user.is_authenticated:
        #get the email
        user = request.user

        #serialize the queried data
        serializer = CustomUserSerializer(user)

        #return the json of this data

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













# @csrf_exempt
# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def upload_logo(request):
#     if request.method =='POST':
#         user= request.user.email
#         serializer= PhotoSerializer(user, data=request.data)
#         if serializer.is_valid():

#             serializer.save()
#             return JsonResponse({'message':'sucessfully uploaded'}, status=status.HTTP_201_CREATED)

#         else:
#             return JsonResponse({'message': "invalid file"}, status=status.HTTP_400_BAD_REQUEST)

#     else:
#          return JsonResponse({'message': "bad request"}, status=status.HTTP_400_BAD_REQUEST)



from django.db import IntegrityError

class BusinessLogoView(APIView):

    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # print(request.user.email)
        try:
            serializer = PhotoSerializer( data=request.data)
            if serializer.is_valid():
                serializer.validated_data['user'] = request.user
                serializer.save()
                return JsonResponse({"data": serializer.data, "user": request.user.email}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

        except IntegrityError:
            return JsonResponse({"error": serializer.errors, "message": "This user has already uploaded a photo", "user": request.user.email}, status= status.HTTP_409_CONFLICT)

    def get(self, request):
        try:
              #get the email
            email =request.user.email
            # query the database with this id
            user= CustomUser.objects.get(email)
            photo= user.photo.all

            if photo is not None:
                serializers= PhotoSerializerSerializer(photo)
                return JsonResponse({"message":"user photo successfully fetched", "photo": serializers.data}, status= status.HTTP_200_OK)
            else:
                return JsonResponse({'error': "invalid user details"}, status= status.HTTP_400_BAD_REQUEST)



        except ObjectDoesNotExist:
            return JsonResponse({"error": serializers.errors, "message": "the user has not uploaded a photo"})


