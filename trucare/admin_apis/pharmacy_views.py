from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import serializers, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from accounts.models import AccountProfile
from accounts.views import IsAccountAdmin
from rest_framework import permissions


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
	from rest_framework import serializers
	return {
		"type": "object",
		"properties": {
			"count": {"type": "integer"},
			"next": {"type": "string", "nullable": True},
			"previous": {"type": "string", "nullable": True},
			"results": {"type": "array", "items": {}},
		},
	}


class PharmacyReadSerializer(serializers.ModelSerializer):
	"""Read-only serializer for pharmacy users."""
	pharmacy_id = serializers.IntegerField(source="id", read_only=True)
	role = serializers.CharField(source="account_profile.role", read_only=True)
	profile_created_at = serializers.DateTimeField(source="account_profile.created_at", read_only=True)
	profile_updated_at = serializers.DateTimeField(source="account_profile.updated_at", read_only=True)

	class Meta:
		model = User
		fields = [
			"pharmacy_id",
			"username",
			"email",
			"first_name",
			"last_name",
			"role",
			"profile_created_at",
			"profile_updated_at",
		]


class PharmacyCreateSerializer(serializers.Serializer):
	"""Serializer for creating new pharmacy accounts."""
	username = serializers.CharField(
		max_length=150,
		help_text="Unique login username."
	)
	email = serializers.EmailField(
		help_text="Pharmacy account email."
	)
	password = serializers.CharField(
		write_only=True,
		min_length=8,
		help_text="Minimum 8 characters."
	)
	first_name = serializers.CharField(
		max_length=150,
		required=False,
		allow_blank=True
	)
	last_name = serializers.CharField(
		max_length=150,
		required=False,
		allow_blank=True
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
		password = validated_data.pop("password")
		user = User.objects.create_user(password=password, **validated_data)
		AccountProfile.objects.create(
			user=user,
			role=AccountProfile.ROLE_PHARMACY,
		)
		return user


class PharmacyUpdateSerializer(serializers.Serializer):
	"""Serializer for updating pharmacy accounts."""
	username = serializers.CharField(
		max_length=150,
		required=False
	)
	email = serializers.EmailField(required=False)
	password = serializers.CharField(
		write_only=True,
		min_length=8,
		required=False
	)
	first_name = serializers.CharField(
		max_length=150,
		required=False,
		allow_blank=True
	)
	last_name = serializers.CharField(
		max_length=150,
		required=False,
		allow_blank=True
	)

	def validate_username(self, value):
		pharmacy = self.context.get("pharmacy")
		if User.objects.exclude(id=pharmacy.id).filter(username=value).exists():
			raise serializers.ValidationError("Username already exists.")
		return value

	def validate_email(self, value):
		pharmacy = self.context.get("pharmacy")
		if User.objects.exclude(id=pharmacy.id).filter(email=value).exists():
			raise serializers.ValidationError("Email already exists.")
		return value

	@transaction.atomic
	def update(self, pharmacy, validated_data):
		password = validated_data.pop("password", None)
		
		for field, value in validated_data.items():
			setattr(pharmacy, field, value)

		if password:
			pharmacy.set_password(password)

		pharmacy.save()

		AccountProfile.objects.update_or_create(
			user=pharmacy,
			defaults={"role": AccountProfile.ROLE_PHARMACY},
		)
		return pharmacy


class PharmacyListCreateAPIView(ListCreateAPIView):
	"""List all pharmacy accounts or create a new one."""
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = PharmacyReadSerializer

	def get_queryset(self):
		queryset = User.objects.select_related("account_profile").filter(
			account_profile__role=AccountProfile.ROLE_PHARMACY,
		).order_by("id")
		
		search = self.request.query_params.get("search")
		if search:
			search = search.strip()
			queryset = queryset.filter(
				Q(username__icontains=search)
				| Q(email__icontains=search)
				| Q(first_name__icontains=search)
				| Q(last_name__icontains=search)
			)
		return queryset

	@extend_schema(
		summary="List pharmacy accounts",
		description="Return all pharmacy user accounts. Admin-only endpoint.",
		tags=["Admin Pharmacy"],
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
		responses={200: PharmacyReadSerializer(many=True), 401: dict, 403: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Create pharmacy account",
		description="Create a new pharmacy user account. Admin-only endpoint.",
		tags=["Admin Pharmacy"],
		request=PharmacyCreateSerializer,
		responses={201: PharmacyReadSerializer, 400: dict, 401: dict, 403: dict},
		examples=[
			OpenApiExample(
				"Create pharmacy payload",
				request_only=True,
				value={
					"username": "pharmacy_main",
					"email": "pharmacy@example.com",
					"password": "StrongPass123!",
					"first_name": "Main",
					"last_name": "Pharmacy",
				},
			)
		],
	)
	def post(self, request, *args, **kwargs):
		serializer = PharmacyCreateSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		pharmacy = serializer.save()
		output = PharmacyReadSerializer(pharmacy)
		return Response(output.data, status=status.HTTP_201_CREATED)


class PharmacyDetailAPIView(RetrieveUpdateDestroyAPIView):
	"""Retrieve, update, or delete a pharmacy account."""
	permission_classes = [permissions.IsAuthenticated]

	lookup_url_kwarg = "pharmacy_id"
	serializer_class = PharmacyReadSerializer

	def get_queryset(self):
		return User.objects.select_related("account_profile").filter(
			account_profile__role=AccountProfile.ROLE_PHARMACY,
		)

	@extend_schema(
		summary="Get pharmacy account",
		description="Retrieve one pharmacy account by id. Admin-only endpoint.",
		tags=["Admin Pharmacy"],
		responses={200: PharmacyReadSerializer, 401: dict, 403: dict, 404: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Update pharmacy account",
		description="Fully update pharmacy account. Admin-only endpoint.",
		tags=["Admin Pharmacy"],
		request=PharmacyUpdateSerializer,
		responses={200: PharmacyReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
		examples=[
			OpenApiExample(
				"Update pharmacy payload",
				request_only=True,
				value={
					"first_name": "Main",
					"last_name": "Pharmacy",
					"email": "main.pharmacy@example.com",
				},
			)
		],
	)
	def put(self, request, *args, **kwargs):
		pharmacy = self.get_object()
		serializer = PharmacyUpdateSerializer(data=request.data, context={"pharmacy": pharmacy})
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(pharmacy, serializer.validated_data)
		return Response(PharmacyReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Patch pharmacy account",
		description="Partially update pharmacy account. Admin-only endpoint.",
		tags=["Admin Pharmacy"],
		request=PharmacyUpdateSerializer,
		responses={200: PharmacyReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def patch(self, request, *args, **kwargs):
		pharmacy = self.get_object()
		serializer = PharmacyUpdateSerializer(data=request.data, context={"pharmacy": pharmacy}, partial=True)
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(pharmacy, serializer.validated_data)
		return Response(PharmacyReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Delete pharmacy account",
		description="Delete a pharmacy user account. Admin-only endpoint.",
		tags=["Admin Pharmacy"],
		responses={204: None, 401: dict, 403: dict, 404: dict},
	)
	def delete(self, request, *args, **kwargs):
		pharmacy = self.get_object()
		pharmacy.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
