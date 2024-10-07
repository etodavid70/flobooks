from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import AddEntry
from .serializers import AddEntrySerializer

class AddEntryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddEntrySerializer(data=request.data)
        if serializer.is_valid():
            # Assign the logged-in user to the entry
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class AddEntryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter entries by the logged-in user
        user_entries = AddEntry.objects.filter(user=request.user)

        # Serialize the entries
        serializer = AddEntrySerializer(user_entries, many=True)

        # Optionally, you can include additional information in the response
        additional_info = {
            'total_entries': user_entries.count(),  # Example: Include count of entries
            # Add other relevant info as needed
        }
        sales_revenue={
            "debit": 0,
            "credit":0
            }
        account_recievables={
            "debit": 0,
            "credit":0
            }
        purchases={
            "debit": 0,
            "credit":0
            }

        account_payable={
            "debit": 0,
            "credit":0
            }
        loans_payable={
            "debit": 0,
            "credit":0
            }
        inventory={
            "debit": 0,
            "credit":0
        }

        expenses_account={
            "debit": 0,
            "credit":0
            }
        cash_account={
            "debit": 0,
            "credit":0
            }
        bank_account={
            "debit": 0,
            "credit":0
            }

        response_data = {
            'entries': serializer.data,
            'sales_revenue': sales_revenue,
            "account_recievables": account_recievables,
            "purchases": purchases,
            "account_payable": account_payable,
            "loans_payable": loans_payable,
            "inventory": inventory,
            "expenses_account": expenses_account,
            "cash_account": cash_account,
            "bank_account":bank_account

        }
        return Response(response_data, status=status.HTTP_200_OK)
