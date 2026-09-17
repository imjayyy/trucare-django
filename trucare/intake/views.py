from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission, Http404, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .get_intake import GetIntakeInfo
from trucare.pagination import StandardPagination
from .intake_list_view_serializer import IntakeListViewSerializer
from .intake_form_generator import generate_intake_form_json
from .models import (
	Choice,
	ConditionQuestion,
	Insurance,
	PatientInfo,
	PatientAnswer,
	PatientAnswerChoice,
	PatientCondition,
	PatientIntake,
)

from accounts.models import AccountProfile, DoctorProfile
from .payload_serializers import (
	FamilyHistoryPayloadSerializer,
	HealthRecordPayloadSerializer,
	IntakeCreatePayloadSerializer,
	IntakeUpdatePayloadSerializer,
	IntakeWriteResponseSerializer,
	InsuranceSerializer,
	MedicalHistoryPayloadSerializer,
	PatientConditionSerializer,
	PatientInfoSerializer,
	PatientIntakeSerializer,
)


class AssignDoctorSerializer(serializers.Serializer):
	patient_id = serializers.IntegerField(required=True, help_text="The patient ID of the intake to update.")
	doctor_id = serializers.IntegerField(required=True, help_text="The doctor profile ID from the available doctors list.")


class ClaimIntakeSerializer(serializers.Serializer):
	patient_id = serializers.IntegerField(required=True, help_text="The patient ID of the intake to claim.")

class IsAuthenticatedOrOptions(BasePermission):
	"""Allow unauthenticated CORS preflight requests while protecting API methods."""

	def has_permission(self, request, view):
		if request.method == "OPTIONS":
			return True

		return bool(request.user and request.user.is_authenticated)


@extend_schema_view(
	get=extend_schema(
		summary="Get intake form schema",
		description="Returns a React-friendly JSON schema to render the intake form on the frontend.",
		tags=["Intake"],
		responses={200: serializers.JSONField()},
		examples=[
			OpenApiExample(
				"Intake form schema",
				response_only=True,
				value={
					"formKey": "patient-intake",
					"version": 1,
					"sections": [
						{"id": "patient_info", "title": "Patient Information", "fields": []},
						{"id": "insurance", "title": "Insurance", "repeatable": True, "fields": []},
					],
				},
				status_codes=["200"],
			)
		],
	),
	post=extend_schema(
		summary="Create intake submission",
		description="Creates a patient intake record with patient information, insurance entries, and condition answers.",
		tags=["Intake"],
		request=IntakeCreatePayloadSerializer,
		responses={201: IntakeWriteResponseSerializer, 400: serializers.JSONField()},
		examples=[
			OpenApiExample(
				"Create intake payload",
				request_only=True,
				value={
					"patient_info": {
						"first_name": "Jane",
						"last_name": "Doe",
						"date_of_birth": "1990-01-01",
						"email": "jane@example.com",
						"phone_number": "5551234567",
						"address": "123 Main St",
						"state": "CA",
					},
					"insurances": [
						{
							"insurance_type": "RX",
							"primary_insured": True,
							"insurance_carrier": "Acme RX",
							"group_id": "GRP-100",
							"patient_id_rx": "PAT-200",
							"bin": "123456",
							"pcn": "ABC",
						}
					],
					"condition_answers": [
						{
							"question_id": 1,
							"text_answer": "Lower back pain for 2 weeks",
						}
					],
				},
			)
		],
	),
	put=extend_schema(
		summary="Update intake submission",
		description="Updates any part of an existing intake using patient_id. Supports partial updates.",
		tags=["Intake"],
		request=IntakeUpdatePayloadSerializer,
		responses={200: IntakeWriteResponseSerializer, 400: serializers.JSONField(), 404: serializers.JSONField()},
		examples=[
			OpenApiExample(
				"Update intake payload",
				request_only=True,
				value={
					"patient_id": 1,
					"patient_info": {
						"phone_number": "5550001212",
						"address": "456 Updated Ave",
					},
					"insurances": [
						{
							"insurance_type": "PIP",
							"primary_insured": False,
							"insurance_carrier": "Acme PIP",
							"policy_number": "POL-123",
							"claim_number": "CLM-99",
							"date_of_accident": "2026-06-01",
						}
					],
				},
			)
		],
	),
)
class IntakeFormAPIView(APIView):
	permission_classes = [IsAuthenticatedOrOptions]

	def get(self, request):
		form_schema = generate_intake_form_json(include_condition_questions=True)
		return Response(form_schema, status=status.HTTP_200_OK)

	@transaction.atomic
	def post(self, request):
		intake_agent = request.user
		account_profile = AccountProfile.objects.filter(user=intake_agent).first()
		if not account_profile:
			return Response({"detail": "Account profile not found."}, status=status.HTTP_400_BAD_REQUEST)
		if account_profile.role != "ORGANIZATION" and account_profile.role != "INTAKE_AGENT":
			return Response({"detail": "You do not have permission to create an intake."}, status=status.HTTP_403_FORBIDDEN)

		if account_profile.role == "ORGANIZATION":
			client = intake_agent.id
		elif account_profile.role == "INTAKE_AGENT":
			client = account_profile.parent_organization.id
		data_ = request.data.copy()
		data_["patient_intake"]["intake_agent"] = intake_agent.id
		data_["patient_intake"]["client"] = client
		data_["patient_intake"]["status"] = "PENDING"

		from .intake_form_submit_validator import IntakeFormSubmitValidator

		try:
			validated_intake = IntakeFormSubmitValidator(form_data=data_)
			patient = validated_intake.validate()

		except ValueError as e:
			return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		
		return Response(
				{"patient_id": patient["patient_info"].id if patient.get("patient_info") else None, 
	 			"intake_id": patient["patient_intake"].id if patient.get("patient_intake") else None,
	 			"message": "Intake created successfully."},
				status=status.HTTP_201_CREATED,
			)

	@transaction.atomic
	def put(self, request):
		intake_agent = request.user
		account_profile = AccountProfile.objects.filter(user=intake_agent).first()
		
		client = account_profile.parent_organization

		if account_profile.role != "ADMIN":
			try:
				get_object_or_404(PatientInfo, id=request.data.get("patient_id"), intake_agent=intake_agent, client=client)
			except Http404:
				return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)	

		serializer = IntakeUpdatePayloadSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
        
		patient_id = serializer.validated_data["patient_id"]
		patient = get_object_or_404(PatientInfo, id=patient_id)
		patient = self._save_intake_data(serializer.validated_data, patient=patient)
		return Response(
			{"patient_id": patient.id, "message": "Intake updated successfully."},
			status=status.HTTP_200_OK,
		)

	def _save_intake_data(self, validated_data, patient=None):
		patient_info = validated_data.get("patient_info", {})
		insurances_data = validated_data.get("insurances")
		condition_answers_data = validated_data.get("condition_answers")

		if patient is None:
			patient = PatientInfo.objects.create(**patient_info)
		elif patient_info:
			for field, value in patient_info.items():
				setattr(patient, field, value)
			patient.save()

		if insurances_data is not None:
			patient.insurances.all().delete()
			for insurance_data in insurances_data:
				Insurance.objects.create(patient=patient, **insurance_data)

		if condition_answers_data is not None:
			self._upsert_condition_answers(patient, condition_answers_data)

		return patient

	def _upsert_condition_answers(self, patient, condition_answers_data):
		for item in condition_answers_data:
			question = get_object_or_404(ConditionQuestion, id=item["question_id"])
			PatientCondition.objects.update_or_create(
				patient=patient,
				condition=question.condition,
				defaults={"requested": True},
			)

			answer, _ = PatientAnswer.objects.update_or_create(
				patient=patient,
				question=question,
				defaults={
					"text_answer": item.get("text_answer"),
					"number_answer": item.get("number_answer"),
					"boolean_answer": item.get("boolean_answer"),
					"date_answer": item.get("date_answer"),
				},
			)

			if "selected_choice_ids" in item:
				selected_ids = item.get("selected_choice_ids", [])
				valid_choices = list(
					Choice.objects.filter(
						id__in=selected_ids,
						choice_set=question.choice_set,
					)
				)
				PatientAnswerChoice.objects.filter(answer=answer).delete()
				for choice in valid_choices:
					PatientAnswerChoice.objects.create(answer=answer, choice=choice)




class IntakeListItemSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	patient_id = serializers.IntegerField(source="id")
	intake_id = serializers.SerializerMethodField()
	first_name = serializers.CharField()
	last_name = serializers.CharField()
	state = serializers.CharField(allow_null=True, required=False)
	status = serializers.SerializerMethodField()
	manager = serializers.SerializerMethodField()
	agent = serializers.SerializerMethodField()
	doctor = serializers.SerializerMethodField()
	insurance_bin = serializers.SerializerMethodField()
	insurance_pcn = serializers.SerializerMethodField()
	insurance_group = serializers.SerializerMethodField()
	insurance_type = serializers.SerializerMethodField()

	def get_intake_id(self, obj):
		intake = self.context.get("intake_map", {}).get(obj.id)
		if intake:
			return intake.id
		return None

	def get_status(self, obj):
		intake = self.context.get("intake_map", {}).get(obj.id)
		return intake.status if intake else None

	def get_manager(self, obj):
		intake = self.context.get("intake_map", {}).get(obj.id)
		if intake and intake.client:
			return intake.client.get_full_name() or intake.client.username
		return None

	def get_agent(self, obj):
		intake = self.context.get("intake_map", {}).get(obj.id)
		if intake and intake.intake_agent:
			return intake.intake_agent.get_full_name() or intake.intake_agent.username
		return None

	def get_doctor(self, obj):
		intake = self.context.get("intake_map", {}).get(obj.id)
		if intake and intake.doctor and intake.doctor.user:
			return intake.doctor.user.get_full_name() or intake.doctor.user.username
		return None

	def get_insurance_bin(self, obj):
		for insurance in self.context.get("insurance_map", {}).get(obj.id, []):
			if insurance.bin:
				return insurance.bin
		return None

	def get_insurance_pcn(self, obj):
		for insurance in self.context.get("insurance_map", {}).get(obj.id, []):
			if insurance.pcn:
				return insurance.pcn
		return None

	def get_insurance_group(self, obj):
		for insurance in self.context.get("insurance_map", {}).get(obj.id, []):
			if insurance.group_id:
				return insurance.group_id
		return None

	def get_insurance_type(self, obj):
		for insurance in self.context.get("insurance_map", {}).get(obj.id, []):
			if insurance.insurance_type:
				return insurance.insurance_type
		return None


class IntakeDoctorListAPIView(APIView):
	permission_classes = [IsAuthenticatedOrOptions]

	@extend_schema(
		summary="List available doctors",
		description="Returns the list of doctors a coordinator or manager can assign to an intake.",
		tags=["Intake"],
		responses={200: serializers.JSONField(), 403: serializers.JSONField()},
		examples=[
			OpenApiExample(
				"doctor_list",
				value=[
					{"id": 1, "name": "Dr. Jane Doe", "email": "jane@example.com", "npi": "1234567890", "state": "CA"}
				],
				response_only=True,
				status_codes=["200"],
			)
		],
	)
	def get(self, request, *args, **kwargs):
		account_profile = AccountProfile.objects.filter(user=request.user).first()
		if not account_profile or account_profile.role not in {"MANAGER", "COORDINATOR"}:
			return Response({"detail": "Only coordinators or managers can view doctors."}, status=status.HTTP_403_FORBIDDEN)

		doctors = DoctorProfile.objects.select_related("user").order_by("user__first_name", "user__last_name")
		payload = []
		for doctor in doctors:
			payload.append({
				"id": doctor.id,
				"name": doctor.user.get_full_name() or doctor.user.username if doctor.user else None,
				"email": doctor.user.email if doctor.user else None,
				"npi": doctor.npi,
				"state": doctor.state,
			})
		return Response(payload, status=status.HTTP_200_OK)


class IntakeSearchAPIView(APIView):
	permission_classes = [IsAuthenticatedOrOptions]

	@extend_schema(
		summary="Search an intake by patient ID",
		description="Returns the current intake record for a patient so a coordinator or manager can review and act on it.",
		tags=["Intake"],
		responses={200: serializers.JSONField(), 400: serializers.JSONField(), 404: serializers.JSONField()},
		examples=[
			OpenApiExample(
				"intake_search",
				value={"patient_id": 12, "first_name": "Alice", "last_name": "Smith", "status": "Pending", "assigned_doctor_id": None},
				response_only=True,
				status_codes=["200"],
			)
		],
	)
	def get(self, request, *args, **kwargs):
		account_profile = AccountProfile.objects.filter(user=request.user).first()
		if not account_profile or account_profile.role not in {"MANAGER", "COORDINATOR"}:
			return Response({"detail": "Only coordinators or managers can search intakes."}, status=status.HTTP_403_FORBIDDEN)

		patient_id = request.query_params.get("patient_id")
		if not patient_id:
			return Response({"detail": "patient_id is required."}, status=status.HTTP_400_BAD_REQUEST)

		# patient = get_object_or_404(PatientInfo, id=patient_id)
		intake = PatientIntake.objects.filter(id=patient_id).select_related("patient").first()
		if not intake:
			return Response({"detail": "Intake not found."}, status=status.HTTP_404_NOT_FOUND)

		return Response([{
			"patient_id": intake.patient.id,
			"first_name": intake.patient.first_name,
			"last_name": intake.patient.last_name,
			"status": intake.status,
			"assigned_doctor_id": intake.doctor_id,
		}], status=status.HTTP_200_OK)


class IntakeClaimedListAPIView(APIView):
	permission_classes = [IsAuthenticatedOrOptions]

	@extend_schema(
		summary="List claimed intakes",
		description="Returns a list of intakes that have been claimed by coordinators or managers.",
		tags=["Intake"],
		responses={200: serializers.JSONField(), 403: serializers.JSONField()},
		examples=[
			OpenApiExample(
				"claimed_intakes",
				value=[
					{"patient_id": 12, "first_name": "Alice", "last_name": "Smith", "status": "Claimed", "assigned_doctor_id": None}
				],
				response_only=True,
				status_codes=["200"],
			)
		],
	)
	def get(self, request, *args, **kwargs):
		account_profile = AccountProfile.objects.filter(user=request.user).first()
		if not account_profile or account_profile.role not in {"MANAGER", "COORDINATOR"}:
			return Response({"detail": "Only coordinators or managers can view claimed intakes."}, status=status.HTTP_403_FORBIDDEN)

		intakes = PatientIntake.objects.filter(status="CLAIMED").select_related("patient")
		payload = []
		for intake in intakes:
			payload.append({
				"patient_id": intake.patient.id,
				"first_name": intake.patient.first_name,
				"last_name": intake.patient.last_name,
				"status": intake.status,
				"assigned_doctor_id": intake.doctor_id,
			})
		return Response(payload, status=status.HTTP_200_OK)


class IntakeClaimAPIView(APIView):
	permission_classes = [IsAuthenticatedOrOptions]

	@extend_schema(
		summary="Claim an intake",
		description="Moves a pending intake into the claimed state so it can be assigned to a doctor.",
		tags=["Intake"],
		request=ClaimIntakeSerializer,
		responses={200: serializers.JSONField(), 400: serializers.JSONField(), 404: serializers.JSONField()},
		examples=[
			OpenApiExample(
				"claim_intake",
				request_only=True,
				value={"patient_id": 12},
				status_codes=["200"],
			),
			OpenApiExample(
				"claim_intake_response",
				value={"patient_id": 12, "status": "CLAIMED"},
				response_only=True,
				status_codes=["200"],
			),
		],
	)
	def post(self, request, *args, **kwargs):
		account_profile = AccountProfile.objects.filter(user=request.user).first()
		if not account_profile or account_profile.role not in {"MANAGER", "COORDINATOR"}:

			return Response({"detail": "Only coordinators or managers can claim intakes."}, status=status.HTTP_403_FORBIDDEN)

		patient_id = request.data.get("patient_id")
		if not patient_id:
			return Response({"detail": "patient_id is required."}, status=status.HTTP_400_BAD_REQUEST)

		patient = get_object_or_404(PatientInfo, id=patient_id)
		intake = PatientIntake.objects.filter(patient=patient).first()
		if not intake:
			return Response({"detail": "Intake not found."}, status=status.HTTP_404_NOT_FOUND)
		if intake.status not in {None, "PENDING"}:
			return Response({"detail": "Intake is not pending."}, status=status.HTTP_400_BAD_REQUEST)

		intake.cordinator = request.user
		intake.status = "CLAIMED"
		intake.save(update_fields=["cordinator", "status", "updated_at"])
		return Response({"patient_id": patient.id, "status": intake.status}, status=status.HTTP_200_OK)


class IntakeAssignDoctorAPIView(APIView):
	permission_classes = [IsAuthenticatedOrOptions]

	@extend_schema(
		summary="Assign a doctor to an intake",
		description="Allows a coordinator or manager to assign a doctor to an existing intake and move it into the assigned workflow state.",
		tags=["Intake"],
		request=AssignDoctorSerializer,
		responses={200: serializers.JSONField(), 400: serializers.JSONField(), 404: serializers.JSONField()},
		examples=[
			OpenApiExample(
				"assign_doctor_request",
				request_only=True,
				value={"patient_id": 12, "doctor_id": 3},
				status_codes=["200"],
			),
			OpenApiExample(
				"assign_doctor_response",
				value={"patient_id": 12, "doctor_id": 3, "status": "ASSIGNED"},
				response_only=True,
				status_codes=["200"],
			),
		],
	)
	def post(self, request, *args, **kwargs):
		account_profile = AccountProfile.objects.filter(user=request.user).first()
		if not account_profile or account_profile.role not in {"MANAGER", "COORDINATOR"}:
			return Response({"detail": "Only coordinators or managers can assign a doctor."}, status=status.HTTP_403_FORBIDDEN)

		serializer = AssignDoctorSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		patient_id = serializer.validated_data["patient_id"]
		doctor_id = serializer.validated_data["doctor_id"]

		patient = get_object_or_404(PatientInfo, id=patient_id)
		intake = PatientIntake.objects.filter(patient=patient).first()
		if not intake:
			return Response({"detail": "Intake not found."}, status=status.HTTP_404_NOT_FOUND)
		if intake.status != "CLAIMED":
			return Response({"detail": "Intake must be claimed before a doctor can be assigned."}, status=status.HTTP_400_BAD_REQUEST)

		doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)
		if not doctor_profile.user:
			return Response({"detail": "Selected user is not a doctor."}, status=status.HTTP_400_BAD_REQUEST)

		intake.doctor = doctor_profile
		intake.status = "ASSIGNED_TO_DOCTOR"
		intake.save(update_fields=["doctor", "status", "updated_at"])
		return Response({"patient_id": patient.id, "doctor_id": doctor_profile.id, "status": intake.status}, status=status.HTTP_200_OK)


class IntakeDetailConditionAnswerSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	question_id = serializers.IntegerField(source="question.id")
	text_answer = serializers.CharField(allow_blank=True, allow_null=True, required=False)
	number_answer = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True, required=False)
	boolean_answer = serializers.BooleanField(allow_null=True, required=False)
	date_answer = serializers.DateField(allow_null=True, required=False)
	selected_choice_ids = serializers.SerializerMethodField(help_text="IDs for the selected choices when this is a choice question.")
	selected_choices = serializers.SerializerMethodField(help_text="Human-readable selected choice labels when this is a choice question.")

	def get_selected_choice_ids(self, obj):
		return list(obj.selected_choices.values_list("choice_id", flat=True))

	def get_selected_choices(self, obj):
		return list(obj.selected_choices.values_list("choice__text", flat=True))


class IntakeDetailResponseSerializer(serializers.Serializer):
	patient_info = PatientInfoSerializer(help_text="Patient demographic and contact information.")
	patient_intake = PatientIntakeSerializer(allow_null=True, help_text="Intake assignment and workflow metadata.")
	insurances = InsuranceSerializer(many=True, help_text="Insurance entries attached to the patient.")
	condition_answers = IntakeDetailConditionAnswerSerializer(many=True, help_text="Condition question answers with selected choice details.")
	family_history = FamilyHistoryPayloadSerializer(many=True, help_text="Patient family history entries.")
	health_records = HealthRecordPayloadSerializer(many=True, help_text="Patient health record entries.")
	medical_history = MedicalHistoryPayloadSerializer(many=True, help_text="Patient medical history entries.")

class IntakeDetailAPIView(APIView):
	permission_classes = [IsAuthenticated]

	@extend_schema(
		summary="Get intake detail by patient ID",
		description="Returns a full intake payload for a single patient, including demographics, assignment metadata, insurance, condition answers, family history, health records, and medical history.",
		tags=["Intake"],
		parameters=[
			OpenApiParameter(
				name="patient_id",
				type=int,
				location=OpenApiParameter.QUERY,
				required=True,
				description="Patient ID for the intake detail lookup.",
			)
		],
		responses={
			200: IntakeDetailResponseSerializer,
			400: serializers.JSONField(),
			403: serializers.JSONField(),
			404: serializers.JSONField(),
		},
		examples=[
			OpenApiExample(
				"intake_detail_success",
				response_only=True,
				status_codes=["200"],
				value={
					"patient_info": {
						"id": 12,
						"first_name": "Alice",
						"last_name": "Smith",
						"email": "alice@example.com",
					},
					"patient_intake": {
						"id": 20,
						"patient": 12,
						"status": "CLAIMED",
					},
					"insurances": [],
					"condition_answers": [
						{
							"id": 77,
							"question_id": 1,
							"text_answer": "Back pain for 2 weeks",
							"number_answer": None,
							"boolean_answer": None,
							"date_answer": None,
							"selected_choice_ids": [],
							"selected_choices": [],
						}
					],
					"family_history": [],
					"health_records": [],
					"medical_history": [],
				},
			),
		],
	)
	def get(self, request, *args, **kwargs):
		intake_id = request.query_params.get("intake_id")
		if not intake_id:
			return Response({"detail": "intake_id is required."}, status=status.HTTP_400_BAD_REQUEST)

		# patient_id = PatientIntake.objects.filter(id=intake_id).select_related("patient").first()
		# print("patient_id object:", patient_id)
		# patient_id = patient_id.patient.id if patient_id else None
		get_intake = GetIntakeInfo(intake_id=intake_id)
		intake_data = get_intake.get_intake_info()
		if not intake_data:
			return Response({"detail": "Intake not found."}, status=status.HTTP_404_NOT_FOUND)

		patient_intake = intake_data.get("patient_intake")
		if not patient_intake:
			return Response({"detail": "Intake not found."}, status=status.HTTP_404_NOT_FOUND)

		doctor_profile_id = patient_intake.get("doctor")
		doctor_user_id = None
		if doctor_profile_id:
			doctor_user_id = DoctorProfile.objects.filter(id=doctor_profile_id).values_list("user_id", flat=True).first()

		account_profile = AccountProfile.objects.filter(user=request.user).first()
		if not account_profile:
			return Response({"detail": "Account profile not found."}, status=status.HTTP_403_FORBIDDEN)

		# if account_profile.role in {"MANAGER", "COORDINATOR"} and patient_intake.get("cordinator") != request.user.id:
		# 	return Response({"detail": "You do not have permission to view this intake."}, status=status.HTTP_403_FORBIDDEN)
		# if account_profile.role == "DOCTOR" and doctor_user_id != request.user.id:
		# 	return Response({"detail": "You do not have permission to view this intake."}, status=status.HTTP_403_FORBIDDEN)
		# if account_profile.role == "ORGANIZATION" and patient_intake.get("client") != request.user.id:
		# 	return Response({"detail": "You do not have permission to view this intake."}, status=status.HTTP_403_FORBIDDEN)
		# if account_profile.role == "INTAKE_AGENT" and patient_intake.get("intake_agent") != request.user.id:
		# 	return Response({"detail": "You do not have permission to view this intake."}, status=status.HTTP_403_FORBIDDEN)
		# if account_profile.role not in {"MANAGER", "COORDINATOR", "DOCTOR", "ORGANIZATION", "INTAKE_AGENT", "ADMIN"}:
		# 	return Response({"detail": "You do not have permission to view this intake."}, status=status.HTTP_403_FORBIDDEN)

		return Response(intake_data, status=status.HTTP_200_OK)

class IntakeListView(GenericAPIView):
	permission_classes = [IsAuthenticatedOrOptions]
	pagination_class = StandardPagination
	serializer_class = IntakeListItemSerializer

	@extend_schema(
		summary="List intake submissions",
		description="Retrieve a paginated list of intakes that can be searched and filtered by patient details, insurance, doctor, agent, manager, state, and status.",
		tags=["Intake"],
		parameters=[
			OpenApiParameter("first_name", str, OpenApiParameter.QUERY, description="Filter by patient first name."),
			OpenApiParameter("last_name", str, OpenApiParameter.QUERY, description="Filter by patient last name."),
			OpenApiParameter("manager", str, OpenApiParameter.QUERY, description="Filter by manager name or username."),
			OpenApiParameter("select_manager", str, OpenApiParameter.QUERY, description="Alias for manager filter."),
			OpenApiParameter("doctor", str, OpenApiParameter.QUERY, description="Filter by doctor name or username."),
			OpenApiParameter("search_by_doctor", str, OpenApiParameter.QUERY, description="Alias for doctor filter."),
			OpenApiParameter("select_doctor", str, OpenApiParameter.QUERY, description="Alias for doctor filter."),
			OpenApiParameter("agent", str, OpenApiParameter.QUERY, description="Filter by agent name or username."),
			OpenApiParameter("select_agent", str, OpenApiParameter.QUERY, description="Alias for agent filter."),
			OpenApiParameter("insurance_bin", str, OpenApiParameter.QUERY, description="Filter by insurance BIN."),
			OpenApiParameter("insurance_pcn", str, OpenApiParameter.QUERY, description="Filter by insurance PCN."),
			OpenApiParameter("insurance_group", str, OpenApiParameter.QUERY, description="Filter by insurance group."),
			OpenApiParameter("state", str, OpenApiParameter.QUERY, description="Filter by patient state."),
			OpenApiParameter("patient_status", str, OpenApiParameter.QUERY, description="Filter by patient status."),
			OpenApiParameter("select_status", str, OpenApiParameter.QUERY, description="Alias for patient status filter."),
			OpenApiParameter("patient_type", str, OpenApiParameter.QUERY, description="Filter by patient type when available."),
			OpenApiParameter("search", str, OpenApiParameter.QUERY, description="General search across patient names and email."),
		],
		responses={200: IntakeListItemSerializer(many=True), 404: serializers.JSONField()},
	)
	def get(self, request, *args, **kwargs):
		patient_id = request.query_params.get("patient_id")
		if patient_id:
			get_intake = GetIntakeInfo(patient_id=patient_id)
			intake_data = get_intake.get_intake_info()
			if not intake_data:
				return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
			return Response(intake_data, status=status.HTTP_200_OK)

		queryset = self._build_queryset(request)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True, context=self._build_context(page))
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True, context=self._build_context(queryset))
		return Response(serializer.data, status=status.HTTP_200_OK)

	def _build_context(self, queryset):
		
		intake_map = {
			intake.patient_id: intake
			for intake in PatientIntake.objects.filter(patient__in=queryset).select_related("client", "intake_agent", "doctor__user")
		}
		insurance_map = {}
		for insurance in Insurance.objects.filter(patient__in=queryset):
			insurance_map.setdefault(insurance.patient_id, []).append(insurance)
		return {"intake_map": intake_map, "insurance_map": insurance_map}

	def _build_queryset(self, request):
		queryset = PatientInfo.objects.all().order_by("-created_at")
		allocate_rx = request.query_params.get("allocate_rx", False)
		show_claimed_only = request.query_params.get("show_claimed_only", False)
		completed_consults = request.query_params.get("completed_consults", False)
		doctors_queue = request.query_params.get("doctors_queue", False)
		billed_consults = request.query_params.get("billed_consults", False)
		user = self.request.user
		account_profile = AccountProfile.objects.filter(user=user).first()
		if account_profile and (account_profile.role == "MANAGER" or account_profile.role == "COORDINATOR"):
			queryset = queryset.filter(intake__cordinator=user)
			if show_claimed_only:
				queryset = queryset.filter(intake__status="CLAIMED")
		if account_profile and account_profile.role == "DOCTOR":
			queryset = queryset.filter(intake__doctor__user=user)
			if completed_consults:
				queryset = queryset.filter(intake__status__in=["DELIVERED", "APPROVED_BY_DOCTOR", ])
			if doctors_queue:
				queryset = queryset.filter(intake__status="ASSIGNED_TO_DOCTOR")
		if account_profile and account_profile.role == "ORGANIZATION":
			queryset = queryset.filter(intake__client=account_profile.user)
			if allocate_rx:
				queryset = queryset.filter(intake__status="APPROVED_BY_DOCTOR")
		if account_profile and account_profile.role == "BILLING":
			queryset = queryset.filter( intake__status__in=["DELIVERED"])
			if billed_consults:
				queryset = queryset.filter(intake__billing_status="BILLED")
			if request.query_params.get("unbillable_consults", False):
				queryset = queryset.filter(intake__billing_status="UNBILLABLE")
			if request.query_params.get("paper_billed_consults", False):
				queryset = queryset.filter(intake__billing_status="PAPER_BILLED")

		if account_profile and account_profile.role == "PHARMACY":
			queryset = queryset.filter(intake__allocated_pharmacy=request.user.id)
			if request.query_params.get("pending_prescriptions", False):
				queryset = queryset.filter(intake__status="ALLOCATED_TO_PHARMACY")




		search = request.query_params.get("search")
		if search:
			queryset = queryset.filter(
				Q(first_name__icontains=search)
				| Q(last_name__icontains=search)
				| Q(email__icontains=search)
			)

		first_name = request.query_params.get("first_name")
		if first_name:
			queryset = queryset.filter(first_name__icontains=first_name)

		last_name = request.query_params.get("last_name")
		if last_name:
			queryset = queryset.filter(last_name__icontains=last_name)

		manager = request.query_params.get("manager") or request.query_params.get("select_manager")
		if manager:
			queryset = queryset.filter(
				Q(intake__client__username__icontains=manager)
				| Q(intake__client__first_name__icontains=manager)
				| Q(intake__client__last_name__icontains=manager)
			)

		doctor = request.query_params.get("doctor") or request.query_params.get("search_by_doctor") or request.query_params.get("select_doctor")
		if doctor:
			queryset = queryset.filter(
				Q(intake__doctor__user__username__icontains=doctor)
				| Q(intake__doctor__user__first_name__icontains=doctor)
				| Q(intake__doctor__user__last_name__icontains=doctor)
			)

		agent = request.query_params.get("agent") or request.query_params.get("select_agent")
		if agent:
			queryset = queryset.filter(
				Q(intake__intake_agent__username__icontains=agent)
				| Q(intake__intake_agent__first_name__icontains=agent)
				| Q(intake__intake_agent__last_name__icontains=agent)
			)

		insurance_bin = request.query_params.get("insurance_bin")
		if insurance_bin:
			queryset = queryset.filter(insurances__bin__icontains=insurance_bin)

		insurance_pcn = request.query_params.get("insurance_pcn")
		if insurance_pcn:
			queryset = queryset.filter(insurances__pcn__icontains=insurance_pcn)

		insurance_group = request.query_params.get("insurance_group")
		if insurance_group:
			queryset = queryset.filter(insurances__group_id__icontains=insurance_group)

		state = request.query_params.get("state")
		if state:
			queryset = queryset.filter(state__icontains=state)

		patient_status = request.query_params.get("patient_status") or request.query_params.get("select_status")
		if patient_status:
			queryset = queryset.filter(intake__status__icontains=patient_status)

		patient_type = request.query_params.get("patient_type")
		if patient_type:
			queryset = queryset.filter(insurances__insurance_type__icontains=patient_type)

		return queryset.distinct().order_by("-created_at")


class IntakeStatusUpdateRequestSerializer(serializers.Serializer):
	function = serializers.ChoiceField(
		choices=[
			"add_notes",
			"update_status",
			"update_cordinator_disposition",
			"allocate_pharmacy",
		],
		help_text="Which intake workflow action to execute.",
	)
	pk = serializers.IntegerField(help_text="Primary key of the intake record to update.")
	notes = serializers.CharField(
		required=False,
		allow_blank=True,
		allow_null=True,
		help_text="Required when function is add_notes; stores the note text.",
	)
	status = serializers.CharField(
		required=False,
		allow_blank=True,
		allow_null=True,
		help_text="Required when function is update_status; sets the new intake status.",
	)
	cordinator_disposition = serializers.CharField(
		required=False,
		allow_blank=True,
		allow_null=True,
		help_text="Required when function is update_cordinator_disposition; stores disposition text.",
	)
	pharmacy = serializers.CharField(
		required=False,
		allow_blank=True,
		allow_null=True,
		help_text="Required when function is allocate_pharmacy; names the assigned pharmacy.",
	)


class IntakeStatusUpdateResponseSerializer(serializers.Serializer):
	message = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="Success message returned for valid actions.")
	error = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="Error message returned when validation or authorization fails.")
	pk = serializers.IntegerField(required=False, allow_null=True, help_text="Intake primary key if relevant to the submitted action.")
	patient_id = serializers.IntegerField(required=False, allow_null=True, help_text="Patient ID associated with the intake.")
	status = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="Updated intake status value when applicable.")
	pharmacy = serializers.CharField(required=False, allow_blank=True, allow_null=True, help_text="Assigned pharmacy when applicable.")


class IntakeStatusUpdateView(APIView):

	permission_classes = [IsAuthenticated]


	def add_notes(self, pk, payload_data):
		"""
		Add notes to the patient intake record.
		"""
		notes = payload_data.get("notes", None)
		if not notes:
			return Response({"error": "Notes are required."}, status=status.HTTP_400_BAD_REQUEST)

		accounts_profile = AccountProfile.objects.get(user=self.user)
		if accounts_profile.role == "MANAGER":
			patient_intake = PatientIntake.objects.get(cordinator=self.user, pk=pk)
			patient_intake.billing_notes = notes
			patient_intake.save()
			return Response({"message": "Billing notes added successfully."}, status=status.HTTP_200_OK)
		return Response({"error": "You do not have permission to add billing notes."}, status=status.HTTP_403_FORBIDDEN)


	def update_status(self, pk, payload_data):
		"""
		Update the status of the patient intake record.
		"""
		accounts_profile = AccountProfile.objects.get(user=self.user)
		role = accounts_profile.role
		target_status = payload_data.get("status")
		if not target_status:
			return Response({"error": "status is required."}, status=status.HTTP_400_BAD_REQUEST)

		if role == "MANAGER":
			patient_intake = PatientIntake.objects.get(cordinator=self.user, pk=pk)
			patient_intake.status = target_status
			patient_intake.save()
			return Response({"message": "Patient intake status updated successfully."}, status=status.HTTP_200_OK)

		if role == "DOCTOR":
			patient_intake = PatientIntake.objects.get(doctor=self.user, pk=pk)
			patient_intake.status = target_status
			patient_intake.save()
			return Response({"message": "Patient intake status updated successfully."}, status=status.HTTP_200_OK)

		if role == "ORGANIZATION":
			patient_intake = PatientIntake.objects.get(client=self.user, pk=pk)
			patient_intake.status = target_status
			patient_intake.save()
			return Response({"message": "Patient intake status updated successfully."}, status=status.HTTP_200_OK)

		if role == "ADMIN":
			patient_intake = PatientIntake.objects.get(pk=pk)
			patient_intake.status = target_status
			patient_intake.save()
			return Response({"message": "Patient intake status updated successfully."}, status=status.HTTP_200_OK)

		if role == "BILLING":
			patient_intake = PatientIntake.objects.get(biller=self.user, pk=pk)
			patient_intake.billing_status = target_status
			patient_intake.save()
			return Response({"message": "Patient intake status updated successfully."}, status=status.HTTP_200_OK)

		if role == "PHARMACY":
			patient_intake = PatientIntake.objects.get(allocated_pharmacy=self.user.id, pk=pk)
			patient_intake.status = target_status
			patient_intake.save()
			return Response({"message": "Patient intake status updated successfully."}, status=status.HTTP_200_OK)

		return Response({"error": "You do not have permission to update the status."}, status=status.HTTP_403_FORBIDDEN)


	def update_cordinator_disposition(self, pk, payload_data):
		"""
		Update the cordinator disposition of the patient intake record.
		"""
		accounts_profile = AccountProfile.objects.get(user=self.user)
		role = accounts_profile.role

		if role == "MANAGER":
			patient_intake = PatientIntake.objects.get(cordinator=self.user, pk=pk)
			patient_intake.cordinator_disposition = payload_data.get("cordinator_disposition")
			patient_intake.save()
			return Response({"message": "Cordinator disposition updated successfully."}, status=status.HTTP_200_OK)

		return Response({"error": "You do not have permission to update the cordinator disposition."}, status=status.HTTP_403_FORBIDDEN)



	def allocate_pharmacy(self, pk, payload_data):
		"""
		Allocate a pharmacy to the patient intake record.
		"""
		accounts_profile = AccountProfile.objects.get(user=self.user)
		role = accounts_profile.role
		pharmacy = payload_data.get("pharmacy")

		if not pharmacy:
			return Response({"error": "Pharmacy is required."}, status=status.HTTP_400_BAD_REQUEST)
		
		if role == "ORGANIZATION":
			patient_intake = PatientIntake.objects.get(client=self.user, pk=pk)
			pharmacy_account_profile = AccountProfile.objects.get(user__id=pharmacy)
			if pharmacy_account_profile.role != "PHARMACY":
				return Response({"error": "Selected user is not a pharmacy."}, status=status.HTTP_400_BAD_REQUEST)
			patient_intake.pharmacy = pharmacy
			if patient_intake.status == "APPROVED_BY_DOCTOR":
				patient_intake.status = "ALLOCATED_TO_PHARMACY"
				patient_intake.save()
			else:
				return Response({"error": "Patient not prescribed yet."}, status=status.HTTP_400_BAD_REQUEST)
			return Response({"message": "Pharmacy allocated successfully."}, status=status.HTTP_200_OK)

		return Response({"error": "You do not have permission to allocate a pharmacy."}, status=status.HTTP_403_FORBIDDEN)


	def update_billing_status(self, pk, payload_data):
	
		accounts_profile = AccountProfile.objects.get(user=self.user)
		role = accounts_profile.role
		if role != "BILLING":
			return Response({"error": "You do not have permission to update the billing status."}, status=status.HTTP_403_FORBIDDEN)
		
		billing_status = payload_data.get("billing_status")
		if not billing_status:
			return Response({"error": "Billing status is required."}, status=status.HTTP_400_BAD_REQUEST)

		intake = get_object_or_404(PatientIntake, pk=pk)
		intake.billing_status = billing_status
		intake.save()

		return Response({"message": "Patient intake billing status updated successfully."}, status=status.HTTP_200_OK)

	def add_billing_notes(self, pk, payload_data):
		accounts_profile = AccountProfile.objects.get(user=self.user)
		role = accounts_profile.role
		if role != "BILLING":
			return Response({"error": "You do not have permission to add billing notes."}, status=status.HTTP_403_FORBIDDEN)

		billing_notes = payload_data.get("billing_notes")
		if not billing_notes:
			return Response({"error": "Billing notes are required."}, status=status.HTTP_400_BAD_REQUEST)

		intake = get_object_or_404(PatientIntake, pk=pk)
		intake.billing_notes = billing_notes
		intake.save()

		return Response({"message": "Patient intake billing notes added successfully."}, status=status.HTTP_200_OK)
	
	@extend_schema(
		summary="Update an intake using a dispatch action",
		description=(
			"This endpoint handles a single intake workflow action selected by the `function` field. "
			"Allowed actions are `add_notes` (manager), `update_status` (all roles), `update_cordinator_disposition` (manager), and `allocate_pharmacy` (agency). "
			"The API validates the active user role and performs the action only when the request is permitted."
		),
		tags=["Intake"],
		request=IntakeStatusUpdateRequestSerializer,
		responses={
			200: IntakeStatusUpdateResponseSerializer,
			400: serializers.JSONField(),
			403: serializers.JSONField(),
		},
		examples=[
			OpenApiExample(
				"Add notes",
				request_only=True,
				value={
					"function": "add_notes",
					"pk": 12,
					"notes": "Patient requested follow-up after intake review.",
				},
				status_codes=["200"],
			),
			OpenApiExample(
				"Update status",
				request_only=True,
				value={
					"function": "update_status",
					"pk": 12,
					"status": "Assigned",
				},
				status_codes=["200"],
			),
			OpenApiExample(
				"Update coordinator disposition",
				request_only=True,
				value={
					"function": "update_cordinator_disposition",
					"pk": 12,
					"cordinator_disposition": "Needs physician review",
				},
				status_codes=["200"],
			),
			OpenApiExample(
				"Allocate pharmacy",
				request_only=True,
				value={
					"function": "allocate_pharmacy",
					"pk": 12,
					"pharmacy": 12,
				},
				status_codes=["200"],
			),
			OpenApiExample(
				"Success response",
				response_only=True,
				value={"message": "Patient intake status updated successfully."},
				status_codes=["200"],
			),
			OpenApiExample(
				"Update billing status",
				request_only=True,
				value={
					"function": "update_billing_status",
					"pk": 12,
					"billing_status": "BILLED",
				},
				status_codes=["200"],
			),
			OpenApiExample(
				"Add billing notes",
				request_only=True,
				value={
					"function": "add_billing_notes",
					"pk": 12,
					"billing_notes": "Patient requested follow-up on billing.",
				},
				status_codes=["200"],
			)
		],
	)

	def post(self, request):
		payload_data = request.data
		self.user = request.user

		function = payload_data.get("function")

		functions = {
			"add_notes": self.add_notes,
			"update_status": self.update_status,
			"update_cordinator_disposition": self.update_cordinator_disposition,
			"allocate_pharmacy": self.allocate_pharmacy,
			"update_billing_status": self.update_billing_status,
			"add_billing_notes": self.add_billing_notes
		}

		return functions.get(
			function,
			lambda *args, **kwargs: Response({"error": "Invalid function."}, status=status.HTTP_400_BAD_REQUEST),
		)(pk=payload_data.get("pk"), payload_data=payload_data)
		

class IntakeGetStatusView(APIView):
	@extend_schema(
		summary="Get the status of an intake",
		description="This endpoint retrieves the current status of a specific intake.",
		tags=["Intake"],
		request=serializers.JSONField(),
		responses={
			200: serializers.JSONField(),
			400: serializers.JSONField(),
			403: serializers.JSONField(),
		},
		examples=[
			OpenApiExample(
				"Get status request",
				request_only=True,
				value={
					"pk": 12,
				},
				status_codes=["200"],
			),
			OpenApiExample(
				"Success response",
				response_only=True,
				value={"status": "Assigned"},
				status_codes=["200"],
			),
		],
	)
	def get(self, request):
		user = request.user
		account_profile = AccountProfile.objects.get(user=user)
		role = account_profile.role

		status_ = {
			"MANAGER": [("Claimed", "CLAIMED"),
						("Assigned to Doctor", "ASSIGNED_TO_DOCTOR"),
						("Provider Decline", "PROVIDER_DECLINE"),
						("Patient Decline", "PATIENT_DECLINE"),
						("Cant Connect", "CANT_CONNECT"),
						("Transfer Unsuccessful", "TRANSFER_UNSUCCESSFUL"),
						("Patient Not Interested", "PATIENT_NOT_INTERESTED"),
						("Invalid Insurance", "INVALID_INSURANCE"),

			   ],
			"ADMIN": [  ("No Status Assigned (N/A)", "N/A"),
						# ("Claimed", "CLAIMED"),
						# ("Assigned to Doctor", "ASSIGNED_TO_DOCTOR"),
						# ("Charting in Progress", "CHARTING_IN_PROGRESS"),
						# ("Approved by Doctor", "APPROVED_BY_DOCTOR"),
						# ("Allocated to Pharmacy", "ALLOCATED_TO_PHARMACY"),
						# ("Delivered", "DELIVERED"),
						("Provider Decline", "PROVIDER_DECLINE"),
						("Patient Decline", "PATIENT_DECLINE"),
						("Cant Connect", "CANT_CONNECT"),
						("Transfer Unsuccessful", "TRANSFER_UNSUCCESSFUL"),
						("Patient Not Interested", "PATIENT_NOT_INTERESTED"),
						("Invalid Insurance", "INVALID_INSURANCE"),
						],

			"PHARMACY": [("Delivered", "DELIVERED"),
						("Cant Connect", "CANT_CONNECT"),

				],
			"ORGANIZATION": [("Pending", "PENDING"),
					   ("Allocated to Pharmacy", "ALLOCATED_TO_PHARMACY"),
			  ],
			"BILLING": [("Pending", "PENDING"),
						('Billed', 'BILLED'),
						('Unbillable', 'UNBILLABLE'),
						('Paper Billed', 'PAPER_BILLED')
			],
		}

		return Response({"status": status_.get(role, [])}, status=status.HTTP_200_OK)
	


class IntakeConditionsView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):

		user = request.user
		intake_id = request.query_params.get("intake_id")
		intake = get_object_or_404(PatientIntake, id=intake_id)
		conditions = PatientCondition.objects.filter(patient=intake)
		serializer = PatientConditionSerializer(conditions, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)