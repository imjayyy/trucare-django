from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import AccountProfile
from .serializers import JWTLoginSerializer, JWTRefreshSerializer, RegisterSerializer, UserSerializer


class IsAccountAdmin(permissions.BasePermission):
	message = "Only admins can register accounts."

	def has_permission(self, request, view):
		if not request.user or not request.user.is_authenticated:
			return False

		profile = getattr(request.user, "account_profile", None)
		return bool(profile and profile.role == AccountProfile.ROLE_ADMIN)


class JWTLoginView(TokenObtainPairView):
	serializer_class = JWTLoginSerializer

	@extend_schema(
		summary="Login with JWT",
		description="Authenticate user and return JWT access and refresh tokens.",
		tags=["Authentication"],
		request=JWTLoginSerializer,
		responses={200: dict, 401: dict},
		examples=[
			OpenApiExample(
				"JWT login request",
				request_only=True,
				value={"username": "manager01", "password": "StrongPassword123!"},
			)
		],
	)
	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)


class JWTRefreshView(TokenRefreshView):
	serializer_class = JWTRefreshSerializer

	@extend_schema(
		summary="Refresh JWT token",
		description="Return a new access token using refresh token.",
		tags=["Authentication"],
		responses={200: dict, 401: dict},
		examples=[
			OpenApiExample(
				"JWT refresh request",
				request_only=True,
				value={"refresh": "<refresh_token>"},
			)
		],
	)
	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)


class RegisterAPIView(APIView):
	permission_classes = [IsAccountAdmin]

	@extend_schema(
		summary="Register account",
		description=(
			"Create a new account-level user with role support for "
			"Admin, Manager, Organization (Agency/Client), Intake Agent, Billing, and Doctor."
			" Only authenticated admins can access this endpoint."
		),
		tags=["Authentication"],
		request=RegisterSerializer,
		responses={201: UserSerializer, 400: dict, 401: dict, 403: dict},
		examples=[
			OpenApiExample(
				"Register organization user",
				request_only=True,
				value={
					"username": "agency_acme",
					"email": "agency@acme.com",
					"password": "StrongPassword123!",
					"first_name": "Acme",
					"last_name": "Agency",
					"role": "ORGANIZATION",
					"organization_type": "AGENCY",
				},
			),
			OpenApiExample(
				"Register intake agent",
				request_only=True,
				value={
					"username": "agent_jane",
					"email": "agent.jane@acme.com",
					"password": "StrongPassword123!",
					"role": "INTAKE_AGENT",
					"parent_organization_id": 5,
				},
			),
		],
	)
	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class MeAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	@extend_schema(
		summary="Get current user",
		description="Return the currently authenticated user and account profile details.",
		tags=["Authentication"],
		responses={200: UserSerializer, 401: dict},
	)
	def get(self, request):
		return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
