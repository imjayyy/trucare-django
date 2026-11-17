from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from datetime import datetime, time, timedelta
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import AccountProfile, AgencyProfile, DoctorLicense, DoctorProfile, User
from intake.models import PatientInfo, PatientIntake
from .serializers import (
	DoctorLicenseSerializer,
	DoctorProfileSerializer,
	JWTLoginSerializer,
	JWTRefreshSerializer,
	PasswordChangeSerializer,
	RegisterSerializer,
	UserSerializer,
	AgencyProfileSerializer,
	AccountProfileSerializer,
)


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
					user__id=pk
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
				user__id=pk
			).select_related("user").order_by("user__username")

			if not intake_agents_profile.exists():
				return Response(
					{"detail": "Intake agent not found."},
					status=status.HTTP_404_NOT_FOUND
				)

			intake_agent = intake_agents_profile.first().user
			# intake_agent['role'] = "INTAKE_AGENT"
			request.data['role'] = "INTAKE_AGENT"
			request.data['parent_organization_id'] = user.id
			print(request.data, intake_agent)
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
				user__id=pk
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

class UpdateProfile(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		"""Retrieve the profile of the authenticated user."""
		user = request.user
		profile = AccountProfile.objects.get(user=user)
		return Response(UserSerializer(profile.user).data, status=status.HTTP_200_OK)



	# def patch(self, request):
	# 	"""Update the profile of the authenticated user."""
	# 	user = request.user
	# 	profile = AccountProfile.objects.get(user=user)
	# 	serializer = RegisterSerializer(profile.user, data=request.data, partial=True)
	# 	serializer.is_valid(raise_exception=True)
	# 	updated_user = serializer.save()
	# 	return Response(UserSerializer(updated_user).data, status=status.HTTP_200_OK)

class PasswordChangeView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	@extend_schema(
		summary="Change password",
		description="Change the password of the authenticated user.",
		tags=["Authentication"],
		request=PasswordChangeSerializer,
		responses={200: UserSerializer, 400: dict, 401: dict},
	)
	def patch(self, request):
		"""Change the password of the authenticated user."""
		user = request.user
		serializer = PasswordChangeSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		if not user.check_password(serializer.validated_data["old_password"]):
			return Response(
				{"old_password": "The current password is incorrect."},
				status=status.HTTP_400_BAD_REQUEST,
			)

		user.set_password(serializer.validated_data["new_password"])
		user.save(update_fields=["password"])
		return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

	def put(self, request):
		account_profile = AccountProfile.objects.get(user=request.user)
		role = account_profile.role
		if role not in [AccountProfile.ROLE_ADMIN, AccountProfile.ROLE_ORGANIZATION]:
			return Response(
				{"detail": "This is an admin-only action."},
				status=status.HTTP_403_FORBIDDEN
			)
		
		
		new_password = request.data.get("new_password")
		confirm_password = request.data.get("confirm_password")
		user_id = request.data.get("user_id")

		

		if new_password != confirm_password:
			return Response(
				{"detail": "New password and confirm password do not match."},
				status=status.HTTP_400_BAD_REQUEST
			)

		try:
			if role == AccountProfile.ROLE_ORGANIZATION:
				user = AccountProfile.objects.get(id=user_id, parent_organization = request.user).user
			else:
				user = User.objects.get(id=user_id)

		except User.DoesNotExist:
			return Response(
				{"detail": "User not found."},
				status=status.HTTP_404_NOT_FOUND
			)

		user.set_password(new_password)
		user.save(update_fields=["password"])
		return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

class DashboardAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	@extend_schema(
		summary="Retrieve dashboard data",
		description="Retrieve dashboard data for the authenticated user.",
		tags=["Dashboard"],
		responses={200: dict, 401: dict, 403: dict},
	)
	def get(self, request):
		profile = getattr(request.user, "account_profile", None)
		if not profile:
			return Response({"detail": "Account profile not found."}, status=status.HTTP_403_FORBIDDEN)

		today = timezone.localdate()
		week_start = today - timedelta(days=today.weekday())
		month_start = today.replace(day=1)
		week_start_at = timezone.make_aware(datetime.combine(week_start, time.min))
		month_start_at = timezone.make_aware(datetime.combine(month_start, time.min))
		intakes = PatientIntake.objects.all()

		def status_count(status_value, start_at):
			return intakes.filter(status=status_value, updated_at__gte=start_at).count()

		if profile.role in {AccountProfile.ROLE_ADMIN, AccountProfile.ROLE_MANAGER}:
			dashboard_data = {
				"dashboard_type": "system",
				"patients_added_this_month": PatientInfo.objects.filter(
					created_at__gte=month_start_at
				).count(),
				"patients_assigned_to_doctor": intakes.filter(
					status="ASSIGNED_TO_DOCTOR"
				).count(),
				"doctor_approvals_this_week": status_count("APPROVED_BY_DOCTOR", week_start_at),
				"doctor_approvals_this_month": status_count("APPROVED_BY_DOCTOR", month_start_at),
				"provider_declines_this_month": status_count("PROVIDER_DECLINE", month_start_at),
				"patient_declines_this_month": status_count("PATIENT_DECLINE", month_start_at),
			}
		elif profile.role == AccountProfile.ROLE_ORGANIZATION:
			intakes = intakes.filter(client=request.user)
			dashboard_data = {
				"dashboard_type": "agency",
				"intake_submissions_this_week": intakes.filter(
					created_at__gte=week_start_at
				).count(),
				"intake_submissions_this_month": intakes.filter(
					created_at__gte=month_start_at
				).count(),
				"doctor_approvals_this_week": status_count("APPROVED_BY_DOCTOR", week_start_at),
				"doctor_approvals_this_month": status_count("APPROVED_BY_DOCTOR", month_start_at),
			}
		else:
			return Response(
				{"detail": "This role does not have a dashboard."},
				status=status.HTTP_403_FORBIDDEN,
			)

		return Response(dashboard_data, status=status.HTTP_200_OK)




class ProfileUpdateView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	@extend_schema(
		summary="Update user profile",
		description="Update the profile of the authenticated user.",
		tags=["Profile"],
		request=RegisterSerializer,
		responses={200: UserSerializer, 400: dict, 401: dict},
	)
	def get(self, request):
		user = request.user
		profile = AccountProfile.objects.get(user=user)
		if not profile:
			return Response({"detail": "Account profile not found."}, status=status.HTTP_404_NOT_FOUND)
		else:
			if profile.role == AccountProfile.ROLE_ORGANIZATION:
				agency_profile = AgencyProfile.objects.get(user=user)
				serializer = AgencyProfileSerializer(agency_profile)			
				serializer_data = UserSerializer(user).data
				serializer_data['agency_profile'] = serializer.data	
				return Response(serializer_data, status=status.HTTP_200_OK)

			if profile.role == AccountProfile.ROLE_DOCTOR:
				serializer = UserSerializer(user)
				doctor_profile = DoctorProfile.objects.get(user=user)
				doctor_licenses = DoctorLicense.objects.filter(doctor=doctor_profile)
				serializer_data = serializer.data
				serializer_data['doctor_profile'] = DoctorProfileSerializer(doctor_profile).data
				serializer_data['doctor_licenses'] = DoctorLicenseSerializer(doctor_licenses, many=True).data
				return Response(serializer_data, status=status.HTTP_200_OK)

			if profile.role == AccountProfile.ROLE_BILLING:
				serializer = UserSerializer(user)
				serializer_data = serializer.data
				return Response(serializer_data, status=status.HTTP_200_OK)

			if profile.role == AccountProfile.ROLE_MANAGER:
				serializer = UserSerializer(user)
				serializer_data = serializer.data
				return Response(serializer_data, status=status.HTTP_200_OK)
			if profile.role == AccountProfile.ROLE_INTAKE_AGENT:
				serializer = UserSerializer(user)
				serializer_data = serializer.data
				return Response(serializer_data, status=status.HTTP_200_OK)

			if profile.role == AccountProfile.ROLE_ADMIN:
				serializer = UserSerializer(user)
				serializer_data = serializer.data
				return Response(serializer_data, status=status.HTTP_200_OK)

	def patch(self, request):
		user = request.user
		profile = AccountProfile.objects.get(user=user)
		if not profile:
			return Response({"detail": "Account profile not found."}, status=status.HTTP_404_NOT_FOUND)
		else:
			if profile.role == AccountProfile.ROLE_ORGANIZATION:
				user_serializer = UserSerializer(user, data=request.data, partial=True)
				user_serializer.is_valid(raise_exception=True)
				user_serializer.save()
				agency_profile = AgencyProfile.objects.get(user=user)
				agency_profile_data = request.data.get('agency_profile', {})
				serializer = AgencyProfileSerializer(agency_profile, data=agency_profile_data, partial=True)
				serializer.is_valid(raise_exception=True)
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)

			if profile.role == AccountProfile.ROLE_DOCTOR:
				print(request.data)
				doctor_profile = DoctorProfile.objects.get(user=user)
				user_serializer = UserSerializer(user, data=request.data, partial=True)
				user_serializer.is_valid(raise_exception=True)
				user_serializer.save()
				serializer = DoctorProfileSerializer(doctor_profile, data=request.data.get('doctor_profile'), partial=True)
				serializer.is_valid(raise_exception=True)
				serializer.save()
				licenses_data = request.data.get('doctor_licenses', [])
				for license_data in licenses_data:
					license_id = license_data.get('id')					
					if license_id:
						try:
							license_instance = DoctorLicense.objects.get(id=license_id, doctor=doctor_profile)
							license_serializer = DoctorLicenseSerializer(license_instance, data=license_data, partial=True)
							license_serializer.is_valid(raise_exception=True)
							license_serializer.save()
						except DoctorLicense.DoesNotExist:
							return Response({"detail": f"DoctorLicense with id {license_id} not found."}, status=status.HTTP_404_NOT_FOUND)
					else:
						license_data['doctor'] = doctor_profile.id
						license_serializer = DoctorLicenseSerializer(data=license_data)
						license_serializer.is_valid(raise_exception=True)
						license_serializer.save(doctor=doctor_profile)

				return Response(serializer.data, status=status.HTTP_200_OK)

			if profile.role == AccountProfile.ROLE_BILLING:
				serializer = UserSerializer(user, data=request.data, partial=True)
				serializer.is_valid(raise_exception=True)
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)

			if profile.role == AccountProfile.ROLE_MANAGER:
				serializer = UserSerializer(user, data=request.data, partial=True)
				serializer.is_valid(raise_exception=True)
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)

			if profile.role == AccountProfile.ROLE_INTAKE_AGENT:
				serializer = UserSerializer(user, data=request.data, partial=True)
				serializer.is_valid(raise_exception=True)
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)

			if profile.role == AccountProfile.ROLE_ADMIN:
				serializer = UserSerializer(user, data=request.data, partial=True)
				serializer.is_valid(raise_exception=True)
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)
