from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from accounts.models import AccountProfile, DoctorProfile
from accounts.views import IsAccountAdmin
from financials.models import ClientCredit, DoctorConsults


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


class DoctorConsultsReadSerializer(serializers.ModelSerializer):
	doctor_id = serializers.IntegerField(source="doctor.id", read_only=True)
	username = serializers.CharField(source="doctor.user.username", read_only=True)
	first_name = serializers.CharField(source="doctor.user.first_name", read_only=True)
	last_name = serializers.CharField(source="doctor.user.last_name", read_only=True)
	email = serializers.EmailField(source="doctor.user.email", read_only=True)
	full_name = serializers.SerializerMethodField()

	class Meta:
		model = DoctorConsults
		fields = [
			"id",
			"doctor_id",
			"username",
			"first_name",
			"last_name",
			"full_name",
			"email",
			"credits",
			"consult_cost",
			"created_at",
			"updated_at",
		]

	def get_full_name(self, obj):
		return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}".strip()


class DoctorConsultsWriteSerializer(serializers.Serializer):
	doctor_id = serializers.IntegerField(help_text="DoctorProfile id.")
	credits = serializers.IntegerField(min_value=0, required=False, help_text="Exact credit balance to set.")
	credit_delta = serializers.IntegerField(required=False, help_text="Positive or negative adjustment to apply.")
	consult_cost = serializers.DecimalField(
		max_digits=10,
		decimal_places=2,
		required=False,
		min_value=0,
		help_text="Cost per consult in USD.",
	)

	def validate(self, attrs):
		if "credits" not in attrs and "credit_delta" not in attrs and "consult_cost" not in attrs:
			raise serializers.ValidationError(
				"Provide at least one of credits, credit_delta, or consult_cost."
			)
		return attrs

	def _get_doctor(self, doctor_id):
		try:
			return DoctorProfile.objects.select_related("user").get(id=doctor_id)
		except DoctorProfile.DoesNotExist as exc:
			raise serializers.ValidationError({"doctor_id": "Doctor not found."}) from exc

	@transaction.atomic
	def create(self, validated_data):
		doctor = self._get_doctor(validated_data.pop("doctor_id"))
		credits = validated_data.pop("credits", None)
		credit_delta = validated_data.pop("credit_delta", None)
		consult_cost = validated_data.pop("consult_cost", None)

		finance, _ = DoctorConsults.objects.get_or_create(doctor=doctor)
		if credits is not None:
			finance.credits = credits
		elif credit_delta is not None:
			finance.credits = max(0, finance.credits + credit_delta)
		if consult_cost is not None:
			finance.consult_cost = consult_cost
		finance.save()
		return finance

	@transaction.atomic
	def update(self, instance, validated_data):
		if "doctor_id" in validated_data:
			instance.doctor = self._get_doctor(validated_data.pop("doctor_id"))
		credits = validated_data.pop("credits", None)
		credit_delta = validated_data.pop("credit_delta", None)
		consult_cost = validated_data.pop("consult_cost", None)

		if credits is not None:
			instance.credits = credits
		elif credit_delta is not None:
			instance.credits = max(0, instance.credits + credit_delta)
		if consult_cost is not None:
			instance.consult_cost = consult_cost
		instance.save()
		return instance


class ClientCreditReadSerializer(serializers.ModelSerializer):
	client_id = serializers.IntegerField(source="client.id", read_only=True)
	username = serializers.CharField(source="client.user.username", read_only=True)
	first_name = serializers.CharField(source="client.user.first_name", read_only=True)
	last_name = serializers.CharField(source="client.user.last_name", read_only=True)
	email = serializers.EmailField(source="client.user.email", read_only=True)
	organization_type = serializers.CharField(source="client.organization_type", read_only=True)
	full_name = serializers.SerializerMethodField()

	class Meta:
		model = ClientCredit
		fields = [
			"id",
			"client_id",
			"username",
			"first_name",
			"last_name",
			"full_name",
			"email",
			"organization_type",
			"credits",
			"credit_cost",
			"created_at",
			"updated_at",
		]

	def get_full_name(self, obj):
		return f"{obj.client.user.first_name} {obj.client.user.last_name}".strip()


class ClientCreditWriteSerializer(serializers.Serializer):
	client_id = serializers.IntegerField(help_text="AccountProfile id for the client organization.")
	credits = serializers.IntegerField(min_value=0, required=False, help_text="Exact credit balance to set.")
	credit_delta = serializers.IntegerField(required=False, help_text="Positive or negative adjustment to apply.")
	credit_cost = serializers.DecimalField(
		max_digits=10,
		decimal_places=2,
		required=False,
		min_value=0,
		help_text="Cost per credit in USD.",
	)

	def validate(self, attrs):
		if "credits" not in attrs and "credit_delta" not in attrs and "credit_cost" not in attrs:
			raise serializers.ValidationError(
				"Provide at least one of credits, credit_delta, or credit_cost."
			)
		return attrs

	def _get_client(self, client_id):
		try:
			client = AccountProfile.objects.select_related("user").get(id=client_id)
		except AccountProfile.DoesNotExist as exc:
			raise serializers.ValidationError({"client_id": "Client not found."}) from exc

		if client.role != AccountProfile.ROLE_ORGANIZATION or client.organization_type != AccountProfile.ORG_CLIENT:
			raise serializers.ValidationError({"client_id": "Client must be an organization account with CLIENT type."})
		return client

	@transaction.atomic
	def create(self, validated_data):
		client = self._get_client(validated_data.pop("client_id"))
		credits = validated_data.pop("credits", None)
		credit_delta = validated_data.pop("credit_delta", None)
		credit_cost = validated_data.pop("credit_cost", None)

		finance, _ = ClientCredit.objects.get_or_create(client=client)
		if credits is not None:
			finance.credits = credits
		elif credit_delta is not None:
			finance.credits = max(0, finance.credits + credit_delta)
		if credit_cost is not None:
			finance.credit_cost = credit_cost
		finance.save()
		return finance

	@transaction.atomic
	def update(self, instance, validated_data):
		if "client_id" in validated_data:
			instance.client = self._get_client(validated_data.pop("client_id"))
		credits = validated_data.pop("credits", None)
		credit_delta = validated_data.pop("credit_delta", None)
		credit_cost = validated_data.pop("credit_cost", None)

		if credits is not None:
			instance.credits = credits
		elif credit_delta is not None:
			instance.credits = max(0, instance.credits + credit_delta)
		if credit_cost is not None:
			instance.credit_cost = credit_cost
		instance.save()
		return instance


class DoctorFinanceListCreateAPIView(ListCreateAPIView):
	permission_classes = [IsAccountAdmin]

	def get_queryset(self):
		queryset = DoctorConsults.objects.select_related("doctor__user").order_by("id")
		search = self.request.query_params.get("search")
		if search:
			queryset = queryset.filter(
				Q(doctor__user__username__icontains=search)
				| Q(doctor__user__email__icontains=search)
				| Q(doctor__user__first_name__icontains=search)
				| Q(doctor__user__last_name__icontains=search)
				| Q(doctor__npi__icontains=search)
			)
		return queryset

	@extend_schema(
		summary="List doctor finances",
		description="Return doctor credit balances and consult cost settings. Admin-only endpoint.",
		tags=["Admin Finance"],
		parameters=[
			*PAGINATION_PARAMETERS,
			OpenApiParameter(
				name="search",
				type=OpenApiTypes.STR,
				location=OpenApiParameter.QUERY,
				required=False,
				description="Search by username, email, name, or NPI.",
			),
		],
		responses={200: paginated_response_serializer("PaginatedDoctorConsultsRead", DoctorConsultsReadSerializer), 401: dict, 403: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Create or set doctor credits",
		description="Create doctor finance settings if missing, or set/adjust credits and consult cost.",
		tags=["Admin Finance"],
		request=DoctorConsultsWriteSerializer,
		responses={201: DoctorConsultsReadSerializer, 400: dict, 401: dict, 403: dict},
		examples=[
			OpenApiExample(
				"Set doctor credits",
				request_only=True,
				value={"doctor_id": 1, "credits": 25, "consult_cost": "45.00"},
			),
			OpenApiExample(
				"Add doctor credits",
				request_only=True,
				value={"doctor_id": 1, "credit_delta": 10},
			),
		],
	)
	def post(self, request, *args, **kwargs):
		serializer = DoctorConsultsWriteSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		finance = serializer.save()
		return Response(DoctorConsultsReadSerializer(finance).data, status=status.HTTP_201_CREATED)


class DoctorFinanceDetailAPIView(RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAccountAdmin]
	lookup_url_kwarg = "finance_id"
	queryset = DoctorConsults.objects.select_related("doctor__user")
	serializer_class = DoctorConsultsReadSerializer

	@extend_schema(
		summary="Get doctor finance record",
		description="Retrieve one doctor finance record by id. Admin-only endpoint.",
		tags=["Admin Finance"],
		responses={200: DoctorConsultsReadSerializer, 401: dict, 403: dict, 404: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Update doctor credits",
		description="Set exact credits, adjust credits, or change consult cost for a doctor.",
		tags=["Admin Finance"],
		request=DoctorConsultsWriteSerializer,
		responses={200: DoctorConsultsReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def put(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = DoctorConsultsWriteSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(instance, serializer.validated_data)
		return Response(DoctorConsultsReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Patch doctor credits",
		description="Partially update a doctor finance record.",
		tags=["Admin Finance"],
		request=DoctorConsultsWriteSerializer,
		responses={200: DoctorConsultsReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def patch(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = DoctorConsultsWriteSerializer(data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(instance, serializer.validated_data)
		return Response(DoctorConsultsReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Delete doctor finance record",
		description="Remove the stored doctor finance record.",
		tags=["Admin Finance"],
		responses={204: None, 401: dict, 403: dict, 404: dict},
	)
	def delete(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class ClientFinanceReadSerializer(serializers.ModelSerializer):
	client_id = serializers.IntegerField(source="client.id", read_only=True)
	username = serializers.CharField(source="client.user.username", read_only=True)
	first_name = serializers.CharField(source="client.user.first_name", read_only=True)
	last_name = serializers.CharField(source="client.user.last_name", read_only=True)
	email = serializers.EmailField(source="client.user.email", read_only=True)
	full_name = serializers.SerializerMethodField()

	class Meta:
		model = ClientCredit
		fields = [
			"id",
			"client_id",
			"username",
			"first_name",
			"last_name",
			"full_name",
			"email",
			"credits",
			"credit_cost",
			"created_at",
			"updated_at",
		]

	def get_full_name(self, obj):
		return f"{obj.client.user.first_name} {obj.client.user.last_name}".strip()


class ClientFinanceWriteSerializer(serializers.Serializer):
	client_id = serializers.IntegerField(help_text="AccountProfile id for a client organization.")
	credits = serializers.IntegerField(min_value=0, required=False, help_text="Exact credit balance to set.")
	credit_delta = serializers.IntegerField(required=False, help_text="Positive or negative adjustment to apply.")
	credit_cost = serializers.DecimalField(
		max_digits=10,
		decimal_places=2,
		required=False,
		min_value=0,
		help_text="Cost per credit in USD.",
	)

	def validate(self, attrs):
		if "credits" not in attrs and "credit_delta" not in attrs and "credit_cost" not in attrs:
			raise serializers.ValidationError(
				"Provide at least one of credits, credit_delta, or credit_cost."
			)
		return attrs

	def _get_client(self, client_id):
		try:
			client = AccountProfile.objects.select_related("user").get(id=client_id)
		except AccountProfile.DoesNotExist as exc:
			raise serializers.ValidationError({"client_id": "Client not found."}) from exc

		if client.role != AccountProfile.ROLE_ORGANIZATION or client.organization_type != AccountProfile.ORG_CLIENT:
			raise serializers.ValidationError({"client_id": "Client must be an organization account with CLIENT type."})
		return client

	@transaction.atomic
	def create(self, validated_data):
		client = self._get_client(validated_data.pop("client_id"))
		credits = validated_data.pop("credits", None)
		credit_delta = validated_data.pop("credit_delta", None)
		credit_cost = validated_data.pop("credit_cost", None)

		finance, _ = ClientCredit.objects.get_or_create(client=client)
		if credits is not None:
			finance.credits = credits
		elif credit_delta is not None:
			finance.credits = max(0, finance.credits + credit_delta)
		if credit_cost is not None:
			finance.credit_cost = credit_cost
		finance.save()
		return finance

	@transaction.atomic
	def update(self, instance, validated_data):
		if "client_id" in validated_data:
			instance.client = self._get_client(validated_data.pop("client_id"))
		credits = validated_data.pop("credits", None)
		credit_delta = validated_data.pop("credit_delta", None)
		credit_cost = validated_data.pop("credit_cost", None)

		if credits is not None:
			instance.credits = credits
		elif credit_delta is not None:
			instance.credits = max(0, instance.credits + credit_delta)
		if credit_cost is not None:
			instance.credit_cost = credit_cost
		instance.save()
		return instance


class ClientFinanceListCreateAPIView(ListCreateAPIView):
	permission_classes = [IsAccountAdmin]

	def get_queryset(self):
		queryset = ClientCredit.objects.select_related("client__user").order_by("id")
		search = self.request.query_params.get("search")
		if search:
			queryset = queryset.filter(
				Q(client__user__username__icontains=search)
				| Q(client__user__email__icontains=search)
				| Q(client__user__first_name__icontains=search)
				| Q(client__user__last_name__icontains=search)
				| Q(client__organization_type__icontains=search)
			)
		organization_type = self.request.query_params.get("organization_type")
		if organization_type:
			queryset = queryset.filter(client__organization_type=organization_type)
		return queryset

	@extend_schema(
		summary="List client finances",
		description="Return client credit balances and configured credit cost. Admin-only endpoint.",
		tags=["Admin Finance"],
		parameters=[
			*PAGINATION_PARAMETERS,
			OpenApiParameter(
				name="search",
				type=OpenApiTypes.STR,
				location=OpenApiParameter.QUERY,
				required=False,
				description="Search by username, email, name, or organization type.",
			),
			OpenApiParameter(
				name="organization_type",
				type=OpenApiTypes.STR,
				location=OpenApiParameter.QUERY,
				required=False,
				description="Filter by organization type, typically CLIENT.",
			),
		],
		responses={200: paginated_response_serializer("PaginatedClientFinanceRead", ClientFinanceReadSerializer), 401: dict, 403: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Create or set client credits",
		description="Create client finance settings if missing, or set/adjust credits and credit cost.",
		tags=["Admin Finance"],
		request=ClientFinanceWriteSerializer,
		responses={201: ClientFinanceReadSerializer, 400: dict, 401: dict, 403: dict},
		examples=[
			OpenApiExample(
				"Set client credits",
				request_only=True,
				value={"client_id": 1, "credits": 100, "credit_cost": "2.50"},
			),
			OpenApiExample(
				"Add client credits",
				request_only=True,
				value={"client_id": 1, "credit_delta": 25},
			),
		],
	)
	def post(self, request, *args, **kwargs):
		serializer = ClientFinanceWriteSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		finance = serializer.save()
		return Response(ClientFinanceReadSerializer(finance).data, status=status.HTTP_201_CREATED)


class ClientFinanceDetailAPIView(RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAccountAdmin]
	lookup_url_kwarg = "finance_id"
	queryset = ClientCredit.objects.select_related("client__user")
	serializer_class = ClientFinanceReadSerializer

	@extend_schema(
		summary="Get client finance record",
		description="Retrieve one client finance record by id. Admin-only endpoint.",
		tags=["Admin Finance"],
		responses={200: ClientFinanceReadSerializer, 401: dict, 403: dict, 404: dict},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)

	@extend_schema(
		summary="Update client credits",
		description="Set exact credits, adjust credits, or change client credit cost.",
		tags=["Admin Finance"],
		request=ClientFinanceWriteSerializer,
		responses={200: ClientFinanceReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def put(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = ClientFinanceWriteSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(instance, serializer.validated_data)
		return Response(ClientFinanceReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Patch client credits",
		description="Partially update a client finance record.",
		tags=["Admin Finance"],
		request=ClientFinanceWriteSerializer,
		responses={200: ClientFinanceReadSerializer, 400: dict, 401: dict, 403: dict, 404: dict},
	)
	def patch(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = ClientFinanceWriteSerializer(data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		updated = serializer.update(instance, serializer.validated_data)
		return Response(ClientFinanceReadSerializer(updated).data, status=status.HTTP_200_OK)

	@extend_schema(
		summary="Delete client finance record",
		description="Remove the stored client finance record.",
		tags=["Admin Finance"],
		responses={204: None, 401: dict, 403: dict, 404: dict},
	)
	def delete(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
