from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import transaction
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import AccountProfile, DoctorLicense, DoctorProfile, AgencyProfile
from accounts.views import IsAccountAdmin
import json

User = get_user_model()


PAGINATION_PARAMETERS = [
	OpenApiParameter(
		name="page",
		type=OpenApiTypes.INT,
		location=OpenApiParameter.QUERY,
		required=False,
		description="Page number for paginated list responses.",
	),
	OpenApiParameter(
		name="page_size",
		type=OpenApiTypes.INT,
		location=OpenApiParameter.QUERY,
		required=False,
		description="Number of items per page (max 100).",
	),
]


def paginated_response_serializer(name, item_serializer):
	return inline_serializer(
		name=name,
		fields={
			"count": serializers.IntegerField(),
			"next": serializers.CharField(allow_null=True, required=False),
			"previous": serializers.CharField(allow_null=True, required=False),
			"results": item_serializer(many=True),
		},
	)

def _build_user_fields(validated_data, field_names):
	user_data = {}
	for field_name in field_names:
		if field_name in validated_data:
			user_data[field_name] = validated_data.pop(field_name)
	return user_data


class DoctorLicenseWriteSerializer(serializers.Serializer):
	license_number = serializers.CharField(max_length=50, help_text="Medical license number.")
	license_state = serializers.CharField(max_length=50, help_text="2-letter state code.")
	expiration_date = serializers.DateField(help_text="License expiration date in YYYY-MM-DD format.")


class DoctorLicenseReadSerializer(serializers.ModelSerializer):
	class Meta:
		model = DoctorLicense
		fields = ["id", "license_number", "license_state", "expiration_date"]


class DoctorCreateSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=150, help_text="Unique login username.")
	email = serializers.EmailField(help_text="Doctor account email.")
	password = serializers.CharField(write_only=True, min_length=8, help_text="Minimum 8 characters.")
	first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
	last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
	phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
	address = serializers.CharField(required=False, allow_blank=True)
	state = serializers.CharField(max_length=50, required=False, allow_blank=True)
	postal_code = serializers.CharField(max_length=20, required=False, allow_blank=True)
	signature = serializers.ImageField(
		required=False,
		allow_null=True,
		validators=[FileExtensionValidator(allowed_extensions=['png'])],
	)
	npi = serializers.CharField(max_length=100, required=False, allow_blank=True)
	licenses = DoctorLicenseWriteSerializer(many=True, required=False, allow_empty=True)

	def validate_username(self, value):
		if User.objects.filter(username=value).exists():
			raise serializers.ValidationError("Username already exists.")
		return value

	def validate_email(self, value):
		if User.objects.filter(email=value).exists():
			raise serializers.ValidationError("Email already exists.")
		return value

	@transaction.atomic
	def create(self, validated_data):
		licenses_data = validated_data.pop("licenses", [])
		password = validated_data.pop("password")
		user_data = _build_user_fields(validated_data, ["username", "email", "first_name", "last_name"])
		profile_data = _build_user_fields(
			validated_data,
			["phone_number", "address", "state", "postal_code", "signature", "npi"],
		)

		user = User.objects.create_user(password=password, **user_data)
		AccountProfile.objects.update_or_create(
			user=user,
			defaults={"role": AccountProfile.ROLE_DOCTOR},
		)

		doctor = DoctorProfile.objects.create(
			user=user,
			phone_number=profile_data.get("phone_number", ""),
			email=user_data.get("email", ""),
			address=profile_data.get("address", ""),
			state=profile_data.get("state", ""),
			postal_code=profile_data.get("postal_code", ""),
			signature=profile_data.get("signature"),
			npi=profile_data.get("npi", ""),
		)

		for license_row in licenses_data:
			DoctorLicense.objects.create(doctor=doctor, **license_row)

		return doctor


class DoctorUpdateSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=150, required=False)
	email = serializers.EmailField(required=False)
	password = serializers.CharField(write_only=True, min_length=8, required=False)
	first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
	last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
	phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
	address = serializers.CharField(required=False, allow_blank=True)
	state = serializers.CharField(max_length=50, required=False, allow_blank=True)
	postal_code = serializers.CharField(max_length=20, required=False, allow_blank=True)
	signature = serializers.ImageField(
		required=False,
		allow_null=True,
		validators=[FileExtensionValidator(allowed_extensions=['png'])],
	)
	npi = serializers.CharField(max_length=100, required=False, allow_blank=True)
	licenses = DoctorLicenseWriteSerializer(many=True, required=False, allow_empty=True)

	def validate_username(self, value):
		doctor = self.context.get("doctor")
		if User.objects.exclude(id=doctor.user_id).filter(username=value).exists():
			raise serializers.ValidationError("Username already exists.")
		return value

	def validate_email(self, value):
		doctor = self.context.get("doctor")
		if User.objects.exclude(id=doctor.user_id).filter(email=value).exists():
			raise serializers.ValidationError("Email already exists.")
		return value

	@transaction.atomic
	def update(self, doctor, validated_data):
		licenses_data = validated_data.pop("licenses", None)
		user_data = _build_user_fields(validated_data, ["username", "email", "first_name", "last_name"])
		profile_data = _build_user_fields(validated_data, ["phone_number", "address", "state", "postal_code", "signature", "npi"])

		user = doctor.user
		for field, value in user_data.items():
			setattr(user, field, value)

		password = validated_data.pop("password", None)
		if password:
			user.set_password(password)

		user.save()

		for field, value in profile_data.items():
			setattr(doctor, field, value)

		doctor.save()

		AccountProfile.objects.update_or_create(
			user=user,
			defaults={"role": AccountProfile.ROLE_DOCTOR},
		)

		if licenses_data is not None:
			doctor.licenses.all().delete()
			for license_row in licenses_data:
				DoctorLicense.objects.create(doctor=doctor, **license_row)

		return doctor


class OrganizationReadSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField(source="id", read_only=True)
	role = serializers.CharField(source="account_profile.role", read_only=True)
	organization_type = serializers.CharField(source="account_profile.organization_type", read_only=True)
	profile_created_at = serializers.DateTimeField(source="account_profile.created_at", read_only=True)
	profile_updated_at = serializers.DateTimeField(source="account_profile.updated_at", read_only=True)
	organization_id = serializers.IntegerField(
			source="account_profile.id",
			read_only=True,
		)
	
	class Meta:
		model = User
		fields = [
			"user_id",
			"username",
			"email",
			"first_name",
			"last_name",
			"role",
			"organization_type",
			"profile_created_at",
			"profile_updated_at",
			"organization_id"
		]


class OrganizationWriteSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=150, help_text="Unique login username.")
	email = serializers.EmailField(help_text="Organization account email.")
	password = serializers.CharField(write_only=True, min_length=8, help_text="Minimum 8 characters.")
	first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
	last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
	organization_type = serializers.ChoiceField(
		choices=[choice[0] for choice in AccountProfile.ORGANIZATION_TYPE_CHOICES],
		help_text="Organization type: AGENCY or CLIENT.",
	)

	def validate_username(self, value):
		if User.objects.filter(username=value).exists():
			raise serializers.ValidationError("Username already exists.")
		return value

	def validate_email(self, value):
		if User.objects.filter(email=value).exists():
			raise serializers.ValidationError("Email already exists.")
		return value

	@transaction.atomic
	def create(self, validated_data):
		organization_type = validated_data.pop("organization_type")
		password = validated_data.pop("password")
		user_data = _build_user_fields(validated_data, ["username", "email", "first_name", "last_name"])

		user = User.objects.create_user(password=password, **user_data)
		
		AccountProfile.objects.create(
			user=user,
			role=AccountProfile.ROLE_ORGANIZATION,
			organization_type=organization_type,
		)
		
		if organization_type == AccountProfile.ORG_AGENCY:
			AgencyProfile.objects.create(user=user)

		return user


class OrganizationUpdateSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=150, required=False)
	email = serializers.EmailField(required=False)
	password = serializers.CharField(write_only=True, min_length=8, required=False)
	first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
	last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
	organization_type = serializers.ChoiceField(
		choices=[choice[0] for choice in AccountProfile.ORGANIZATION_TYPE_CHOICES],
		required=False,
	)

	def validate_username(self, value):
		organization = self.context.get("organization")
		if User.objects.exclude(id=organization.id).filter(username=value).exists():
			raise serializers.ValidationError("Username already exists.")
		return value

	def validate_email(self, value):
		organization = self.context.get("organization")
		if User.objects.exclude(id=organization.id).filter(email=value).exists():
			raise serializers.ValidationError("Email already exists.")
		return value

	@transaction.atomic
	def update(self, organization, validated_data):
		user_data = _build_user_fields(validated_data, ["username", "email", "first_name", "last_name"])
		password = validated_data.pop("password", None)
		organization_type = validated_data.pop("organization_type", None)

		for field, value in user_data.items():
			setattr(organization, field, value)

		if password:
			organization.set_password(password)

		organization.save()

		profile = organization.account_profile
		profile.role = AccountProfile.ROLE_ORGANIZATION
		if organization_type is not None:
			profile.organization_type = organization_type
		profile.save()
		return organization


class DoctorReadSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField(source="user.id", read_only=True)
	username = serializers.CharField(source="user.username", read_only=True)
	first_name = serializers.CharField(source="user.first_name", read_only=True)
	last_name = serializers.CharField(source="user.last_name", read_only=True)
	account_email = serializers.EmailField(source="user.email", read_only=True)
	licenses = DoctorLicenseReadSerializer(many=True, read_only=True)

	class Meta:
		model = DoctorProfile
		fields = [
			"id",
			"user_id",
			"username",
			"first_name",
			"last_name",
			"account_email",
			"phone_number",
			"email",
			"address",
			"state",
			"postal_code",
			"signature",
			"npi",
			"licenses",
			"created_at",
			"updated_at",
		]


class DoctorListCreateAPIView(ListCreateAPIView):
	permission_classes = [IsAccountAdmin]
	serializer_class = DoctorReadSerializer

	def get_queryset(self):
		queryset = DoctorProfile.objects.select_related("user").prefetch_related("licenses").order_by("id")
		search = self.request.query_params.get("search")
		if search:
			search = search.strip()
			queryset = queryset.filter(
				Q(user__username__icontains=search)
				| Q(user__email__icontains=search)
				| Q(user__first_name__icontains=search)
				| Q(user__last_name__icontains=search)
				| Q(npi__icontains=search)
			)
		return queryset

	@extend_schema(
		summary="List doctors",
		description="Return all doctor profiles. Admin-only endpoint.",
		tags=["Admin Doctors"],
		parameters=[
			*PAGINATION_PARAMETERS,
			OpenApiParameter(
				name="search",
				type=OpenApiTypes.STR,
				location=OpenApiParameter.QUERY,
				required=False,
				description="Search by username, email, first name, last name, or NPI.",
			),
		],
		responses={200: paginated_response_serializer("PaginatedDoctorRead", DoctorReadSerializer), 401: dict, 403: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Create doctor",
		description="Create a doctor user account, doctor profile, and optional licenses. Admin-only endpoint.",
		tags=["Admin Doctors"],
		request=DoctorCreateSerializer,
		responses={201: DoctorReadSerializer, 400: dict, 401: dict, 403: dict},
		examples=[
			OpenApiExample(
				"Create doctor payload",
				request_only=True,
				value={
					"username": "doctor_alex",
					"email": "alex@example.com",
					"password": "StrongPass123!",
					"first_name": "Alex",
					"last_name": "Rivera",
					"phone_number": "5551234567",
					"address": "100 Main St",
					"state": "CA",
					"postal_code": "94105",
					"npi": "1234567890",
					"licenses": [
						{
							"license_number": "A12345",
							"license_state": "CA",
							"expiration_date": "2028-12-31",
						}
					],
				},
			)
		],
	)
	def post(self, request, *args, **kwargs):
		data = request.POST.dict()
		signature = request.FILES.get('signature')
		data['signature'] = signature
		licenses = data.get("licenses")
		data["licenses"] = json.loads(licenses)	
		
		serializer = DoctorCreateSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		doctor = serializer.save()
		output = DoctorReadSerializer(doctor)
		return Response(output.data, status=status.HTTP_201_CREATED)


class DoctorDetailAPIView(RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAccountAdmin]
	lookup_url_kwarg = "doctor_id"
	serializer_class = DoctorReadSerializer

	def get_queryset(self):
		return DoctorProfile.objects.select_related("user").prefetch_related("licenses")

	@extend_schema(
		summary="Get doctor",
		description="Retrieve one doctor profile by id. Admin-only endpoint.",
		tags=["Admin Doctors"],
		responses={200: DoctorReadSerializer, 401: dict, 403: dict, 404: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Update doctor",
		description="Partially or fully update doctor account, profile, and licenses. Admin-only endpoint.",
		tags=["Admin Doctors"],
		request=DoctorUpdateSerializer,
		responses={200: DoctorReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
		examples=[
			OpenApiExample(
				"Update doctor payload",
				request_only=True,
				value={
					"first_name": "Alex",
					"last_name": "Rivera",
					"npi": "9999999999",
					"licenses": [
						{
							"license_number": "B88888",
							"license_state": "NY",
							"expiration_date": "2029-06-30",
						}
					],
				},
			)
		],
	)
	def put(self, request, *args, **kwargs):
		doctor = self.get_object()
		serializer = DoctorUpdateSerializer(data=request.data, context={"doctor": doctor})
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(doctor, serializer.validated_data)
		return Response(DoctorReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Patch doctor",
		description="Partially update doctor account, profile, and licenses. Admin-only endpoint.",
		tags=["Admin Doctors"],
		request=DoctorUpdateSerializer,
		responses={200: DoctorReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def patch(self, request, *args, **kwargs):
		print("REQEUST DATA", request.POST.dict())
		data = request.POST.dict()
		signature = request.FILES.get('signature')
		data['signature'] = signature
		licenses = data.get("licenses")
		data["licenses"] = json.loads(licenses)	
		doctor = self.get_object()
		serializer = DoctorUpdateSerializer(data=data, context={"doctor": doctor}, partial=True)
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(doctor, serializer.validated_data)
		return Response(DoctorReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Delete doctor",
		description="Delete doctor profile and linked user account. Admin-only endpoint.",
		tags=["Admin Doctors"],
		responses={204: None, 401: dict, 403: dict, 404: dict},
	)
	def delete(self, request, *args, **kwargs):
		doctor = self.get_object()
		user = doctor.user
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizationListCreateAPIView(ListCreateAPIView):
	permission_classes = [IsAccountAdmin]
	serializer_class = OrganizationReadSerializer

	def get_queryset(self):
		queryset = User.objects.select_related("account_profile").filter(
			account_profile__role=AccountProfile.ROLE_ORGANIZATION,
		)
		organization_type = self.request.query_params.get("organization_type")
		search = self.request.query_params.get("search")
		if organization_type:
			queryset = queryset.filter(account_profile__organization_type=organization_type)
		if search:
			search = search.strip()
			queryset = queryset.filter(
				Q(username__icontains=search)
				| Q(email__icontains=search)
				| Q(first_name__icontains=search)
				| Q(last_name__icontains=search)
				| Q(account_profile__organization_type__icontains=search)
			)
		return queryset.order_by("id")

	@extend_schema(
		summary="List organizations",
		description="Return all client and agency accounts. Admin-only endpoint.",
		tags=["Admin Organizations"],
		parameters=[
			*PAGINATION_PARAMETERS,
			OpenApiParameter(
				name="search",
				type=OpenApiTypes.STR,
				location=OpenApiParameter.QUERY,
				required=False,
				description="Search by username, email, first name, last name, or organization type.",
			),
			OpenApiParameter(
				name="organization_type",
				type=OpenApiTypes.STR,
				location=OpenApiParameter.QUERY,
				required=False,
				description="Filter by organization type: AGENCY or CLIENT.",
			),
		],
		responses={200: paginated_response_serializer("PaginatedOrganizationRead", OrganizationReadSerializer), 401: dict, 403: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Create organization",
		description="Create a client or agency account and its profile. Admin-only endpoint.",
		tags=["Admin Organizations"],
		request=OrganizationWriteSerializer,
		responses={201: OrganizationReadSerializer, 400: dict, 401: dict, 403: dict},
		examples=[
			OpenApiExample(
				"Create agency payload",
				request_only=True,
				value={
					"username": "agency_acme",
					"email": "agency@example.com",
					"password": "StrongPass123!",
					"first_name": "Acme",
					"last_name": "Agency",
					"organization_type": "AGENCY",
				},
			),
		],
	)
	def post(self, request, *args, **kwargs):
		serializer = OrganizationWriteSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		organization = serializer.save()
		return Response(OrganizationReadSerializer(organization).data, status=status.HTTP_201_CREATED)


class OrganizationDetailAPIView(RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAccountAdmin]
	lookup_url_kwarg = "organization_id"
	serializer_class = OrganizationReadSerializer

	def get_queryset(self):
		return User.objects.select_related("account_profile").filter(
			account_profile__role=AccountProfile.ROLE_ORGANIZATION,
		)

	@extend_schema(
		summary="Get organization",
		description="Retrieve one client or agency account by id. Admin-only endpoint.",
		tags=["Admin Organizations"],
		responses={200: OrganizationReadSerializer, 401: dict, 403: dict, 404: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Update organization",
		description="Partially or fully update a client or agency account. Admin-only endpoint.",
		tags=["Admin Organizations"],
		request=OrganizationUpdateSerializer,
		responses={200: OrganizationReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def put(self, request, *args, **kwargs):
		organization = self.get_object()
		serializer = OrganizationUpdateSerializer(data=request.data, context={"organization": organization})
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(organization, serializer.validated_data)
		return Response(OrganizationReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Patch organization",
		description="Partially update a client or agency account. Admin-only endpoint.",
		tags=["Admin Organizations"],
		request=OrganizationUpdateSerializer,
		responses={200: OrganizationReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def patch(self, request, *args, **kwargs):
		organization = self.get_object()
		serializer = OrganizationUpdateSerializer(data=request.data, context={"organization": organization}, partial=True)
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(organization, serializer.validated_data)
		return Response(OrganizationReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Delete organization",
		description="Delete a client or agency account and its profile. Admin-only endpoint.",
		tags=["Admin Organizations"],
		responses={204: None, 401: dict, 403: dict, 404: dict},
	)
	def delete(self, request, *args, **kwargs):
		organization = self.get_object()
		organization.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class AgencyProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = AgencyProfile
		fields = [
			"phone_number",
			"email",
			"address",
			"state",
			"postal_code",
			"website",
			"fax_number",
		]

class UpdateAgencyProfileAPIView(APIView):
	permission_classes = [IsAuthenticated]

	@extend_schema(
		summary="Update organization info",
		description="Update the organization profile information. Admin-only endpoint.",
		tags=["Admin Organizations"],
		request=AgencyProfileSerializer,
		responses={200: AgencyProfile, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def get(self, request):
		user = request.user
		account_profile = AccountProfile.objects.filter(user=user).first()
		if not account_profile:
			return Response({"detail": "Account profile not found."}, status=status.HTTP_404_NOT_FOUND)
		role = account_profile.role
		if role != AccountProfile.ROLE_ADMIN:
			profile = AgencyProfile.objects.filter(user_id=user.id).first()
			if not profile:
				return Response({"detail": "Agency profile not found."}, status=status.HTTP_404_NOT_FOUND)
			serializer = AgencyProfileSerializer(profile)
			return Response(serializer.data, status=status.HTTP_200_OK)

		if role == AccountProfile.ROLE_ADMIN:
			user_id = request.query_params.get("user_id")
			if not user_id:
				return Response({"detail": "user_id query parameter is required for admin users."}, status=status.HTTP_400_BAD_REQUEST)
			profile = AgencyProfile.objects.filter(user_id=user_id).first()
			if not profile:
				return Response({"detail": "Agency profile not found."}, status=status.HTTP_404_NOT_FOUND)
			serializer = AgencyProfileSerializer(profile)
			return Response(serializer.data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Post/Update organization info",
		description="Update the organization profile information.",
		tags=["Admin Organizations"],
		request=AgencyProfileSerializer,
		responses={200: AgencyProfile, 400: dict, 401: dict, 403: dict, 404: dict},
		parameters=[
			OpenApiParameter(
				name="user_id",
				type=OpenApiTypes.INT,
				location=OpenApiParameter.QUERY,
				required=False,
				description="User ID of the organization profile to update. Required for admin users.",
			),
		],
	)

	def post(self, request):
		user = request.user
		account_profile = AccountProfile.objects.filter(user=user).first()
		if not account_profile:
			return Response({"detail": "Account profile not found."}, status=status.HTTP_404_NOT_FOUND)
		role = account_profile.role
		if role != AccountProfile.ROLE_ADMIN:
			profile = AgencyProfile.objects.filter(user_id=user.id).first()
			if not profile:
				return Response({"detail": "Agency profile not found."}, status=status.HTTP_404_NOT_FOUND)
			serializer = AgencyProfileSerializer(profile, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		if role == AccountProfile.ROLE_ADMIN:
			user_id = request.query_params.get("user_id")
			if not user_id:
				return Response({"detail": "user_id query parameter is required for admin users."}, status=status.HTTP_400_BAD_REQUEST)
			profile = AgencyProfile.objects.filter(user_id=user_id).first()
			if not profile:
				profile = AgencyProfile.objects.create(user_id=user_id)				
			serializer = AgencyProfileSerializer(profile, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request):
		return self.post(request)
	

class RoleAccountReadSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField(source="id", read_only=True)
	role = serializers.CharField(source="account_profile.role", read_only=True)
	profile_created_at = serializers.DateTimeField(source="account_profile.created_at", read_only=True)
	profile_updated_at = serializers.DateTimeField(source="account_profile.updated_at", read_only=True)

	class Meta:
		model = User
		fields = [
			"user_id",
			"username",
			"email",
			"first_name",
			"last_name",
			"role",
			"profile_created_at",
			"profile_updated_at",
		]


class RoleAccountWriteSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=150, help_text="Unique login username.")
	email = serializers.EmailField(help_text="Account email.")
	password = serializers.CharField(write_only=True, min_length=8, help_text="Minimum 8 characters.")
	first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
	last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

	role_value = None
	role_label = "Account"

	def validate_username(self, value):
		if User.objects.filter(username=value).exists():
			raise serializers.ValidationError("Username already exists.")
		return value

	def validate_email(self, value):
		if User.objects.filter(email=value).exists():
			raise serializers.ValidationError("Email already exists.")
		return value

	@transaction.atomic
	def create(self, validated_data):
		password = validated_data.pop("password")
		user_data = _build_user_fields(validated_data, ["username", "email", "first_name", "last_name"])

		user = User.objects.create_user(password=password, **user_data)
		AccountProfile.objects.create(
			user=user,
			role=self.role_value,
		)
		return user


class RoleAccountUpdateSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=150, required=False)
	email = serializers.EmailField(required=False)
	password = serializers.CharField(write_only=True, min_length=8, required=False)
	first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
	last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

	role_value = None
	role_label = "Account"

	def validate_username(self, value):
		account = self.context.get("account")
		if User.objects.exclude(id=account.id).filter(username=value).exists():
			raise serializers.ValidationError("Username already exists.")
		return value

	def validate_email(self, value):
		account = self.context.get("account")
		if User.objects.exclude(id=account.id).filter(email=value).exists():
			raise serializers.ValidationError("Email already exists.")
		return value

	@transaction.atomic
	def update(self, account, validated_data):
		user_data = _build_user_fields(validated_data, ["username", "email", "first_name", "last_name"])
		password = validated_data.pop("password", None)

		for field, value in user_data.items():
			setattr(account, field, value)

		if password:
			account.set_password(password)

		account.save()

		profile = account.account_profile
		profile.role = self.role_value
		profile.save()
		return account


class ManagerWriteSerializer(RoleAccountWriteSerializer):
	role_value = AccountProfile.ROLE_MANAGER
	role_label = "Manager"


class ManagerUpdateSerializer(RoleAccountUpdateSerializer):
	role_value = AccountProfile.ROLE_MANAGER
	role_label = "Manager"


class BillingWriteSerializer(RoleAccountWriteSerializer):
	role_value = AccountProfile.ROLE_BILLING
	role_label = "Billing"


class BillingUpdateSerializer(RoleAccountUpdateSerializer):
	role_value = AccountProfile.ROLE_BILLING
	role_label = "Billing"


class ManagerListCreateAPIView(ListCreateAPIView):
	permission_classes = [IsAccountAdmin]
	serializer_class = RoleAccountReadSerializer

	def get_queryset(self):
		queryset = User.objects.select_related("account_profile").filter(
			account_profile__role=AccountProfile.ROLE_MANAGER,
		)
		search = self.request.query_params.get("search")
		if search:
			search = search.strip()
			queryset = queryset.filter(
				Q(username__icontains=search)
				| Q(email__icontains=search)
				| Q(first_name__icontains=search)
				| Q(last_name__icontains=search)
			)
		return queryset.order_by("id")

	@extend_schema(
		summary="List managers",
		description="Return all manager accounts. Admin-only endpoint.",
		tags=["Admin Staff"],
		parameters=[
			*PAGINATION_PARAMETERS,
			OpenApiParameter(
				name="search",
				type=OpenApiTypes.STR,
				location=OpenApiParameter.QUERY,
				required=False,
				description="Search by username, email, first name, or last name.",
			),
		],
		responses={200: paginated_response_serializer("PaginatedRoleAccountReadManagers", RoleAccountReadSerializer), 401: dict, 403: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Create manager",
		description="Create a manager account and profile. Admin-only endpoint.",
		tags=["Admin Staff"],
		request=ManagerWriteSerializer,
		responses={201: RoleAccountReadSerializer, 400: dict, 401: dict, 403: dict},
		examples=[
			OpenApiExample(
				"Create manager payload",
				request_only=True,
				value={
					"username": "manager_one",
					"email": "manager@example.com",
					"password": "StrongPass123!",
					"first_name": "Casey",
					"last_name": "Morgan",
				},
			),
		],
	)
	def post(self, request, *args, **kwargs):
		serializer = ManagerWriteSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		account = serializer.save()
		return Response(RoleAccountReadSerializer(account).data, status=status.HTTP_201_CREATED)


class ManagerDetailAPIView(RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAccountAdmin]
	lookup_url_kwarg = "manager_id"
	serializer_class = RoleAccountReadSerializer

	def get_queryset(self):
		return User.objects.select_related("account_profile").filter(
			account_profile__role=AccountProfile.ROLE_MANAGER,
		)

	@extend_schema(
		summary="Get manager",
		description="Retrieve one manager account by id. Admin-only endpoint.",
		tags=["Admin Staff"],
		responses={200: RoleAccountReadSerializer, 401: dict, 403: dict, 404: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Update manager",
		description="Partially or fully update a manager account. Admin-only endpoint.",
		tags=["Admin Staff"],
		request=ManagerUpdateSerializer,
		responses={200: RoleAccountReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def put(self, request, *args, **kwargs):
		account = self.get_object()
		serializer = ManagerUpdateSerializer(data=request.data, context={"account": account})
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(account, serializer.validated_data)
		return Response(RoleAccountReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Patch manager",
		description="Partially update a manager account. Admin-only endpoint.",
		tags=["Admin Staff"],
		request=ManagerUpdateSerializer,
		responses={200: RoleAccountReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def patch(self, request, *args, **kwargs):
		account = self.get_object()
		serializer = ManagerUpdateSerializer(data=request.data, context={"account": account}, partial=True)
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(account, serializer.validated_data)
		return Response(RoleAccountReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Delete manager",
		description="Delete a manager account and profile. Admin-only endpoint.",
		tags=["Admin Staff"],
		responses={204: None, 401: dict, 403: dict, 404: dict},
	)
	def delete(self, request, *args, **kwargs):
		account = self.get_object()
		account.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class BillingListCreateAPIView(ListCreateAPIView):
	permission_classes = [IsAccountAdmin]
	serializer_class = RoleAccountReadSerializer

	def get_queryset(self):
		queryset = User.objects.select_related("account_profile").filter(
			account_profile__role=AccountProfile.ROLE_BILLING,
		)
		search = self.request.query_params.get("search")
		if search:
			search = search.strip()
			queryset = queryset.filter(
				Q(username__icontains=search)
				| Q(email__icontains=search)
				| Q(first_name__icontains=search)
				| Q(last_name__icontains=search)
			)
		return queryset.order_by("id")

	@extend_schema(
		summary="List billers",
		description="Return all billing accounts. Admin-only endpoint.",
		tags=["Admin Staff"],
		parameters=[
			*PAGINATION_PARAMETERS,
			OpenApiParameter(
				name="search",
				type=OpenApiTypes.STR,
				location=OpenApiParameter.QUERY,
				required=False,
				description="Search by username, email, first name, or last name.",
			),
		],
		responses={200: paginated_response_serializer("PaginatedRoleAccountReadBillers", RoleAccountReadSerializer), 401: dict, 403: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Create biller",
		description="Create a billing account and profile. Admin-only endpoint.",
		tags=["Admin Staff"],
		request=BillingWriteSerializer,
		responses={201: RoleAccountReadSerializer, 400: dict, 401: dict, 403: dict},
		examples=[
			OpenApiExample(
				"Create biller payload",
				request_only=True,
				value={
					"username": "billing_one",
					"email": "billing@example.com",
					"password": "StrongPass123!",
					"first_name": "Jordan",
					"last_name": "Lee",
				},
			),
		],
	)
	def post(self, request, *args, **kwargs):
		serializer = BillingWriteSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		account = serializer.save()
		return Response(RoleAccountReadSerializer(account).data, status=status.HTTP_201_CREATED)


class BillingDetailAPIView(RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAccountAdmin]
	lookup_url_kwarg = "biller_id"
	serializer_class = RoleAccountReadSerializer

	def get_queryset(self):
		return User.objects.select_related("account_profile").filter(
			account_profile__role=AccountProfile.ROLE_BILLING,
		)

	@extend_schema(
		summary="Get biller",
		description="Retrieve one billing account by id. Admin-only endpoint.",
		tags=["Admin Staff"],
		responses={200: RoleAccountReadSerializer, 401: dict, 403: dict, 404: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Update biller",
		description="Partially or fully update a billing account. Admin-only endpoint.",
		tags=["Admin Staff"],
		request=BillingUpdateSerializer,
		responses={200: RoleAccountReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def put(self, request, *args, **kwargs):
		account = self.get_object()
		serializer = BillingUpdateSerializer(data=request.data, context={"account": account})
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(account, serializer.validated_data)
		return Response(RoleAccountReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Patch biller",
		description="Partially update a billing account. Admin-only endpoint.",
		tags=["Admin Staff"],
		request=BillingUpdateSerializer,
		responses={200: RoleAccountReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def patch(self, request, *args, **kwargs):
		account = self.get_object()
		serializer = BillingUpdateSerializer(data=request.data, context={"account": account}, partial=True)
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(account, serializer.validated_data)
		return Response(RoleAccountReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Delete biller",
		description="Delete a billing account and profile. Admin-only endpoint.",
		tags=["Admin Staff"],
		responses={204: None, 401: dict, 403: dict, 404: dict},
	)
	def delete(self, request, *args, **kwargs):
		account = self.get_object()
		account.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


