from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from models import DoctorConsults, DoctorConsultCost, ClientCredit, ClientCreditRecord

# Create your views here.


class DoctorConsultsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DoctorConsults.objects.all()

    def post(self, request, *args, **kwargs):
        pass
