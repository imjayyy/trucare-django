from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
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


class IntakeAgentPagination(PageNumberPagination):
	"""Custom pagination for intake agent list with configurable page size."""
	page_size = 10
	page_size_query_param = "page_size"
	max_page_size = 100




class RegisterIntakeAgentAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	pagination_class = IntakeAgentPagination

	@extend_schema(
		summary="List intake agents for organization",
		description="Retrieve a paginated list of intake agents belonging to the authenticated organization. Only accessible by organization accounts.",
		tags=["Authentication"],
		parameters=[
			OpenApiParameter(
				name="page",
				description="Page number for pagination (default: 1)",
				required=False,
				type=int,
			),
			OpenApiParameter(
				name="page_size",
				description="Number of results per page (default: 10, max: 100)",
				required=False,
				type=int,
			),
		],
		responses={
			200: OpenApiExample(
				"Paginated intake agents list",
				value={
					"count": 25,
					"next": "http://api.example.com/intake-agents/?page=2",
					"previous": None,
					"results": [
						{
							"id": 1,
							"username": "agent_jane",
							"email": "agent.jane@acme.com",
							"first_name": "Jane",
							"last_name": "Doe",
						}
					],
				},
				response_only=True,
				status_codes=[200],
			),
			401: {"description": "Authentication credentials were not provided or are invalid."},
			403: {"description": "Only organization accounts can access this endpoint."},
		},
	)
	def get(self, request, pk=None):
		"""Retrieve paginated list of intake agents for the authenticated organization."""
		user = request.user
		

		try:
			account_profile = AccountProfile.objects.get(user=user)
			if account_profile.role != "ORGANIZATION":
				return Response(
					{"detail": "This is not an ORGANIZATION account."},
					status=status.HTTP_403_FORBIDDEN
				)
			if pk is not None:
				intake_agents_profile = AccountProfile.objects.filter(
					parent_organization=user,
					id=pk
				).select_related("user").order_by("user__username")

				if not intake_agents_profile.exists():
					return Response(
						{"detail": "Intake agent not found."},
						status=status.HTTP_404_NOT_FOUND
					)
				return Response(
					UserSerializer(
						intake_agents_profile.first().user
					).data,
					status=status.HTTP_200_OK
				)

			intake_agents_profile = AccountProfile.objects.filter(
				parent_organization=user
			).select_related("user").order_by("user__username")

			# Apply pagination
			paginator = self.pagination_class()
			paginated_profiles = paginator.paginate_queryset(intake_agents_profile, request)
			intake_agents_data = UserSerializer(
				[profile.user for profile in paginated_profiles],
				many=True
			).data

			return paginator.get_paginated_response(intake_agents_data)
		except AccountProfile.DoesNotExist:
			return Response(
				{"detail": "Account profile not found."},
				status=status.HTTP_403_FORBIDDEN
			)

	@extend_schema(
		summary="Create new intake agent",
		description="Register a new intake agent under the authenticated organization. Only accessible by organization accounts.",
		tags=["Authentication"],
		request=RegisterSerializer,
		responses={
			201: OpenApiExample(
				"Intake agent created successfully",
				value={
					"id": 1,
					"username": "agent_jane",
					"email": "agent.jane@acme.com",
					"first_name": "Jane",
					"last_name": "Doe",
				},
				response_only=True,
				status_codes=[201],
			),
			400: {"description": "Invalid input data or missing required fields."},
			401: {"description": "Authentication credentials were not provided or are invalid."},
			403: {"description": "Only organization accounts can create intake agents."},
		},
		examples=[
			OpenApiExample(
				"Create intake agent",
				request_only=True,
				value={
					"username": "agent_jane",
					"email": "agent.jane@acme.com",
					"password": "StrongPassword123!",
					"first_name": "Jane",
					"last_name": "Doe",
				},
			)
		],
	)
	def post(self, request):
		"""Create a new intake agent for the authenticated organization."""
		user = request.user
		try:
			account_profile = AccountProfile.objects.get(user=user)
			if account_profile.role != "ORGANIZATION":
				return Response(
					{"detail": "This is not an ORGANIZATION account."},
					status=status.HTTP_403_FORBIDDEN
				)

			intake_agent_data = {
				'username': request.data.get('username'),
				'email': request.data.get('email'),
				'password': request.data.get('password'),
				'first_name': request.data.get('first_name'),
				'last_name': request.data.get('last_name'),
				'role': "INTAKE_AGENT",
				'parent_organization_id': user.id,
			}
			serializer = RegisterSerializer(data=intake_agent_data)
			serializer.is_valid(raise_exception=True)
			agent_user = serializer.save()
			return Response(UserSerializer(agent_user).data, status=status.HTTP_201_CREATED)
		except AccountProfile.DoesNotExist:
			return Response(
				{"detail": "Account profile not found."},
				status=status.HTTP_403_FORBIDDEN
			)

	@extend_schema(
		summary="Update intake agent",
		description="Update an existing intake agent under the authenticated organization. Only accessible by organization accounts.",
		tags=["Authentication"],
		request=RegisterSerializer,
		responses={
			200: OpenApiExample(
				"Intake agent updated successfully",
				value={
					"id": 1,
					"username": "agent_jane",
					"email": "agent.jane@acme.com",
					"first_name": "Jane",
					"last_name": "Doe",
					"password" : "StrongPassword123!",
				},
				response_only=True,
				status_codes=[200],
			),
			400: {"description": "Invalid input data or missing required fields."},
			401: {"description": "Authentication credentials were not provided or are invalid."},
			403: {"description": "Only organization accounts can update intake agents."},
			404: {"description": "Intake agent not found."},
		},
	)
	def patch(self, request, pk):
		"""Update an existing intake agent for the authenticated organization."""
		user = request.user
		try:
			account_profile = AccountProfile.objects.get(user=user)
			if account_profile.role != "ORGANIZATION":
				return Response(
					{"detail": "This is not an ORGANIZATION account."},
					status=status.HTTP_403_FORBIDDEN
				)

			intake_agents_profile = AccountProfile.objects.filter(
				parent_organization=user,
				id=pk
			).select_related("user").order_by("user__username")

			if not intake_agents_profile.exists():
				return Response(
					{"detail": "Intake agent not found."},
					status=status.HTTP_404_NOT_FOUND
				)

			intake_agent = intake_agents_profile.first().user
			serializer = RegisterSerializer(intake_agent, data=request.data, partial=True)
			serializer.is_valid(raise_exception=True)
			updated_agent = serializer.save()
			return Response(UserSerializer(updated_agent).data, status=status.HTTP_200_OK)
		except AccountProfile.DoesNotExist:
			return Response(
				{"detail": "Account profile not found."},
				status=status.HTTP_403_FORBIDDEN
			)

	def delete(self, request, pk):
		"""Delete an existing intake agent for the authenticated organization."""
		user = request.user
		try:
			account_profile = AccountProfile.objects.get(user=user)
			if account_profile.role != "ORGANIZATION":
				return Response(
					{"detail": "This is not an ORGANIZATION account."},
					status=status.HTTP_403_FORBIDDEN
				)

			intake_agents_profile = AccountProfile.objects.filter(
				parent_organization=user,
				id=pk
			).select_related("user").order_by("user__username")

			if not intake_agents_profile.exists():
				return Response(
					{"detail": "Intake agent not found."},
					status=status.HTTP_404_NOT_FOUND
				)

			intake_agent = intake_agents_profile.first().user
			intake_agent.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)
		except AccountProfile.DoesNotExist:
			return Response(
				{"detail": "Account profile not found."},
				status=status.HTTP_403_FORBIDDEN
			)