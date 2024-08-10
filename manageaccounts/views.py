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
from manageaccounts.models import  Subuser,CustomToken
from onboarding.models import CustomUser
from .serializers import  SubuserSerializer,  PackageUpdateSerializer
from rest_framework.views import APIView
# from rest_framework.viewsets import ModelViewSet

from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password


from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
import json


# from django.middleware.csrf import get_token



class PackageUpdateView(APIView):
    permission_classes = [IsAuthenticated ]

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = PackageUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ManageAccounts (APIView):
    permission_classes = [IsAuthenticated]

    PACKAGE_SUBUSER_LIMITS = {
        'bronze': 2,
        'gold': 3,
        'platinum': 4,
        'diamond': 5
    }

    # @method_decorator(csrf_protect)
    def post(self, request):



        subuser_name = request.data.get('subuser_name')
        subuser_email= request.data.get('subuser_email')
        subuser_password = request.data.get('subuser_password')

        user_package = request.user.present_package
        # Adjust according to your actual field name

        # Determine the subuser limit based on the package
        subuser_limit = self.PACKAGE_SUBUSER_LIMITS.get(user_package, 0)

        # Check the number of subusers already created by the user
        current_subuser_count = Subuser.objects.filter(base_user=request.user).count()
        if current_subuser_count >= subuser_limit:
            return JsonResponse(
                {"error": f"You can only create up to {subuser_limit} subusers with the {user_package} package."},
                status=status.HTTP_400_BAD_REQUEST,
                safe=False
            )

        # Hash the subuser_password using make_password
        hashed_password = make_password(subuser_password)


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
            return JsonResponse({"message":f"subuser created successfully! you have {subuser_limit-current_subuser_count-1} slots left",
            "data": serializer.data},)

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
    # @method_decorator(csrf_protect)
    def delete (self, request):

        try:
            subUserEmail= request.data["email"]
            baseUserEmail=request.data["base_user"]

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

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)


    # @method_decorator(csrf_protect)
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

from django.contrib.auth.hashers import check_password
from .serializers import SubuserLoginSerializer
# from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken



@api_view(['POST'])
def subuser_login(request):
    serializer = SubuserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['subuser_email']
        password = serializer.validated_data['subuser_password']

        try:
            subuser = Subuser.objects.get(subuser_email=email)
            if check_password(password, subuser.subuser_password):
                base_user = subuser.base_user  # Get the associated CustomUser instance

                jwToken = RefreshToken.for_user(base_user)

                return Response({
                    "message": "Login successful",
                    'jwAccessToken': str(jwToken.access_token),
                    "jwRefreshToken": str(jwToken),
                    "data": {
                        "email": email,
                        "name": subuser.subuser_name,
                        "baseuserBusinessName": base_user.businessName,
                         "baseuserBusinessAddress": base_user.businessAddress,

                          "recentActivities": {


                        }

                        }



                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
        except Subuser.DoesNotExist:
            return Response({"error": "Invalid email"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status

@api_view(['POST'])
def subuser_logout(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
    except KeyError:
        return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
    except TokenError:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

