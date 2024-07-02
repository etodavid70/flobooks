from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status
# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import generics
from manageaccounts.models import  Subuser
from onboarding.models import CustomUser
from .serializers import  SubuserSerializer
from rest_framework.views import APIView
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password


from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
    
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers


# from django.middleware.csrf import get_token

class ManageAccounts (APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(csrf_protect)
    def post(self, request):
    

        
        subuser_name = request.data.get('subuser_name')
        subuser_email= request.data.get('subuser_email')
        subuser_password = request.data.get('subuser_password')

        # Hash the subuser_password using make_password
        hashed_password = make_password(subuser_password)
        # print(check_password(subuser_password, hashed_password))

        # Create a new dictionary with the hashed password
        data = {
            'subuser_name': subuser_name,
            "subuser_email":  subuser_email,
            'subuser_password': subuser_password
        }

    # Create an instance of the UserSerializer with the data
        serializer =SubuserSerializer(data=data)
        if serializer.is_valid():
        #parse the associated user
            serializer.validated_data["base_user"]= request.user
            serializer.save()
            return JsonResponse({"message":"subuser created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED, safe=False)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


        #if its valid
        

    def get (self, request):

        try:

            base_user_email= request.user.email
            base_user =CustomUser.objects.get(email=base_user_email)
            subusers=base_user.sub_users.all()

            serializer = SubuserSerializer(subusers, many=True)
            # return JsonResponse({"message": "successfully fetched all users","all users": all_subusers}, status=status.HTTP_200_OK)
            return JsonResponse({"message": "successfully fetched all sub users","all sub users": serializer.data}, status=status.HTTP_200_OK)
        
        except Subuser.DoesNotExist:
            return JsonResponse({"message": "no sub users registered on this account"}, status=status.HTTP_404_NOT_FOUND, safe=False)

        

    # def delete (self, request, email):
    @method_decorator(csrf_protect)
    def delete (self, request):
        subUserEmail= request.data["email"]
        baseUserEmail=request.data["base_user"]
        
        try:

            # base_user_email= request.user.email
            #get the base user
            base_user =CustomUser.objects.get(email=baseUserEmail)
           #get the sub user
            sub_user=base_user.sub_users.get(subuser_email=subUserEmail)
           
           #delete the sub user
               
            sub_user.delete()
            return JsonResponse({"message": "sub user successfully removed"},status=status.HTTP_204_NO_CONTENT, safe=False)
            # else:
            #     return JsonResponse({"message": "user does not exist"},status=status.HTTP_404_NOT_FOUND)

        except Subuser.DoesNotExist:
            return JsonResponse({"message": "sub user does not exist"}, status=status.HTTP_404_NOT_FOUND, safe=False)


    @method_decorator(csrf_protect)
    def put ( self, request):
        email = request.data.get('subuser_email')
        try:
            subuser = Subuser.objects.get(subuser_email= email)

            serializer= SubuserSerializer(subuser, data = request.data)
            if serializer.is_valid():
                serializer.save()
                    
                return JsonResponse({"message": "successfully updated", "data": serializer.data}, status=status.HTTP_200_OK)
            
                
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

        except Subuser.DoesNotExist:
            return JsonResponse({"message": "sub user does not exist"}, status=status.HTTP_404_NOT_FOUND, safe=False)

        
        


# Create your views here.
