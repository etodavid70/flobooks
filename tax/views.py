from django.shortcuts import render

from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics
from .models import VAT
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# views.py
from rest_framework import generics
from .models import VAT
from .serializers import VATSerializer, UserStateSerializer
from rest_framework.response import Response
from datetime import timedelta


from django.http import JsonResponse
from django.views import View

from .state_urls import STATE_URLS

class VATRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = VAT.objects.all()
    serializer_class = VATSerializer

    # Assuming you only have one VAT record to track the total VAT
    def get_object(self):
        return VAT.objects.first()






class VATStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        vat_record = VAT.objects.first()  # Assuming single VAT record
        if vat_record:
            vat_due = vat_record.is_vat_due()  # Check if VAT is due
            next_due_date = vat_record.commencement_date + timedelta(days=30)
            return Response({
                "total_vat": vat_record.total_vat,
                "commencement_date": vat_record.commencement_date,
                "Filling Deadline": next_due_date,
                "vat_due": vat_due,
                "compliant status": "Due" if vat_due else "Compliant"
            })
        return Response({"error": "No VAT records found."}, status=404)



class SetCommencementDateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = VAT.objects.all()

    def post(self, request, *args, **kwargs):
        vat_record, created = VAT.objects.get_or_create(id=1)  # Assume single VAT record
        # commencement_date = request.data.get('commencement_date')

        # Use current date as default if not provided
        # if not commencement_date:
        commencement_date = timezone.now()

        try:
            # Make sure to import datetime module
            vat_record.commencement_date = commencement_date
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        vat_record.save()

        user = request.user
        user.start_tax = True
        user.save()

        return Response({"message": "Commencement date set successfully and tax is now being calculated"})



class VATMarkAsPaidView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        vat_record = VAT.objects.first()
        if vat_record and vat_record.vat_due:
            # Mark the VAT as paid and reset for the next cycle
            vat_record.total_vat = Decimal('0.00')
            vat_record.vat_due = False
            vat_record.commencement_date = datetime.now()  # Reset commencement date
            vat_record.save()
            return Response({"message": "VAT marked as paid."})
        return Response({"error": "No VAT due or record not found."}, status=400)





class UserStateView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get(self, request, *args, **kwargs):
        user = request.user  # Get the currently authenticated user
        serializer = UserStateSerializer(user)  # Serialize the user data
        return Response(serializer.data)  # Return th

# Create your views here.



  # Import the dictionary of states

class StateURLView(View):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the state from query parameters
        state = request.GET.get('state', '').lower()

        # Return the corresponding URL if the state exists
        if state in STATE_URLS:
            return JsonResponse({'state': state, 'e_payment_link': STATE_URLS[state]})
        else:
            return JsonResponse({'error': f'State not found {STATE_URLS}'}, status=404)

