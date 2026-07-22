from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.views import IsAccountAdmin

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
    