from django.db.models.aggregates import Count
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.views import IsAccountAdmin
from accounts.models import DoctorProfile
from intake.models import PatientIntake
from prescription.models import Prescription
from collections import defaultdict

from financials.models import DoctorConsults

# Create your views here.


class AdminAPIView(APIView):
    permission_classes = [IsAccountAdmin]


class GetDoctorsAPIView(AdminAPIView):

    def get(self, request):
        from accounts.models import User
        from accounts.serializers import UserSerializer

        users = User.objects.filter(account_profile__role="doctor")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        from accounts.models import User
        from accounts.serializers import UserSerializer

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)

    




class DoctorsConsultationsAPIView(AdminAPIView):
    permission_classes = [IsAccountAdmin]

    def get(self, request):
        rows = (
            DoctorConsults.objects
            .select_related("doctor__user", "patient")
            .values(
                "doctor__user__first_name",
                "doctor__user__last_name",
                "patient__status",
            )
            .annotate(count=Count("id"))
            .order_by(
                "doctor__user__first_name",
                "doctor__user__last_name",
            )
        )

        result = defaultdict(dict)

        for row in rows:
            doctor_name = (
                f"{row['doctor__user__first_name']} "
                f"{row['doctor__user__last_name']}"
            )

            result[doctor_name][row["patient__status"]] = row["count"]

        response_data = [
            {
                "doctor": doctor_name,
                "statuses": statuses,
            }
            for doctor_name, statuses in result.items()
        ]

        return Response(response_data)


