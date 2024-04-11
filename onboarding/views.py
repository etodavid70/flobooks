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




@csrf_exempt
@api_view(['POST'])
def signup(request):
    serializer =  CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({'message': 'Email parameter is missing'}, status=status.HTTP_404_NOT_FOUND)
        


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