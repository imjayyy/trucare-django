from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view
from rest_framework import serializers, status
from rest_framework.permissions import BasePermission, Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from .intake_form_generator import generate_intake_form_json
from .models import (
	Choice,
	ConditionQuestion,
	Insurance,
	Patient_Info,
	PatientAnswer,
	PatientAnswerChoice,
	PatientCondition,
)

from accounts.models import AccountProfile
from .payload_serializers import (
	IntakeCreatePayloadSerializer,
	IntakeUpdatePayloadSerializer,
	IntakeWriteResponseSerializer,
)

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
		client = account_profile.parent_organization
		data_ = request.data.copy()
		data_["patient_info"]["intake_agent"] = intake_agent.id
		data_["patient_info"]["client"] = client


		from .intake_form_submit_validator import IntakeFormSubmitValidator
		try:
			validated_intake = IntakeFormSubmitValidator(form_data=data_)
			patient = validated_intake.validate()
		except ValueError as e:
			return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		
		return Response(
				{"patient_id": patient.id, "message": "Intake created successfully."},
				status=status.HTTP_201_CREATED,
			)

	@transaction.atomic
	def put(self, request):
		intake_agent = request.user
		account_profile = AccountProfile.objects.filter(user=intake_agent).first()
		
		client = account_profile.parent_organization

		if account_profile.role != "Admin":
			try:
				get_object_or_404(Patient_Info, id=request.data.get("patient_id"), intake_agent=intake_agent, client=client)
			except Http404:
				return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)	

		serializer = IntakeUpdatePayloadSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
        
		patient_id = serializer.validated_data["patient_id"]
		patient = get_object_or_404(Patient_Info, id=patient_id)
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
			patient = Patient_Info.objects.create(**patient_info)
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



