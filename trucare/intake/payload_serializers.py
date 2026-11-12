
from rest_framework import serializers
from .models import HealthRecord, MedicalHistory, PatientInfo, Insurance, ConditionQuestion, Choice, ChoiceSet, PatientAnswer, PatientAnswerChoice, PatientCondition, PatientFamilyHistory, PatientIntake
from .models import Surgery, Medication, Allergy

class PatientInfoPayloadSerializer(serializers.Serializer):
	first_name = serializers.CharField(max_length=30, required=False)
	last_name = serializers.CharField(max_length=30, required=False)
	date_of_birth = serializers.DateField(required=False)
	email = serializers.EmailField(required=False)
	phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
	address = serializers.CharField(required=False, allow_blank=True)
	state = serializers.CharField(max_length=20, required=False, allow_blank=True)



class InsurancePayloadSerializer(serializers.Serializer):
	insurance_type = serializers.ChoiceField(choices=[choice[0] for choice in Insurance.INSURANCE_TYPES])
	primary_insured = serializers.BooleanField(required=False, default=False)
	insurance_carrier = serializers.CharField(max_length=100, required=False, allow_blank=True)
	carrier_phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
	group_id = serializers.CharField(max_length=50, required=False, allow_blank=True)
	patient_id_rx = serializers.CharField(max_length=50, required=False, allow_blank=True)
	bin = serializers.CharField(max_length=20, required=False, allow_blank=True)
	pcn = serializers.CharField(max_length=20, required=False, allow_blank=True)
	adjuster_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
	adjuster_phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
	policy_number = serializers.CharField(max_length=50, required=False, allow_blank=True)
	claim_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
	date_of_accident = serializers.DateField(required=False, allow_null=True)
	payer_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
	date_of_injury = serializers.DateField(required=False, allow_null=True)
	employer_name = serializers.CharField(max_length=100, required=False, allow_blank=True)


class ConditionAnswerPayloadSerializer(serializers.Serializer):
	question_id = serializers.IntegerField()
	text_answer = serializers.CharField(required=False, allow_blank=True, allow_null=True)
	number_answer = serializers.DecimalField(
		max_digits=10,
		decimal_places=2,
		required=False,
		allow_null=True,
	)
	boolean_answer = serializers.BooleanField(required=False, allow_null=True)
	date_answer = serializers.DateField(required=False, allow_null=True)
	selected_choice_ids = serializers.ListField(
		child=serializers.IntegerField(),
		required=False,
		allow_empty=True,
	)


class IntakeCreatePayloadSerializer(serializers.Serializer):
	patient_info = PatientInfoPayloadSerializer(required=True)
	insurances = InsurancePayloadSerializer(many=True, required=False)
	condition_answers = ConditionAnswerPayloadSerializer(many=True, required=False)

	def validate(self, attrs):
		patient_info = attrs.get("patient_info", {})
		required_fields = ["first_name", "last_name", "date_of_birth", "email"]
		missing = [field for field in required_fields if not patient_info.get(field)]
		if missing:
			raise serializers.ValidationError(
				{"patient_info": f"Missing required fields for create: {', '.join(missing)}"}
			)
		return attrs


class IntakeUpdatePayloadSerializer(serializers.Serializer):
	patient_id = serializers.IntegerField(required=True)
	intake_id = serializers.IntegerField(required=True)
	patient_info = PatientInfoPayloadSerializer(required=False)
	patient_intake = serializers.DictField(required=False)
	insurances = InsurancePayloadSerializer(many=True, required=False)
	condition_answers = ConditionAnswerPayloadSerializer(many=True, required=False)
	family_history = serializers.JSONField(required=False)
	health_records = serializers.ListField(child=serializers.JSONField(), required=False)
	medical_history = serializers.ListField(child=serializers.JSONField(), required=False)
	condition_requests = serializers.JSONField(required=False)


class IntakeWriteResponseSerializer(serializers.Serializer):
	patient_id = serializers.IntegerField()
	message = serializers.CharField()


class FamilyHistoryPayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientFamilyHistory
        fields = "__all__"

class HealthRecordPayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = "__all__"


class MedicalHistoryPayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = "__all__"

class SurgeryPayloadSerializer(serializers.ModelSerializer):
	class Meta:
		model = Surgery
		fields = "__all__"

class MedicationPayloadSerializer(serializers.ModelSerializer):
	class Meta:
		model = Medication
		fields = "__all__"

class AllergyPayloadSerializer(serializers.ModelSerializer):
	class Meta:
		model = Allergy
		fields = "__all__"

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = "__all__"

class ConditionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientAnswer
        fields = "__all__"
class PatientInfoSerializer(serializers.ModelSerializer):
	# patient_intake = serializers.SerializerMethodField()

	# def get_patient_intake(self, obj):
	# 	intake = PatientIntake.objects.filter(patient=obj).first()
	# 	return PatientIntakeSerializer(intake).data
	
	class Meta:
		model = PatientInfo
		fields = "__all__"
			
class PatientIntakeSerializer(serializers.ModelSerializer):
	# patient_info = PatientInfoSerializer(required=True)

	class Meta:
		model = PatientIntake
		fields = "__all__"


class PatientConditionSerializer(serializers.ModelSerializer):
	condition_name = serializers.CharField(source="condition.name", read_only=True)
	
	class Meta:
		model = PatientCondition
		fields = "__all__"

class PatientAnswerChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = PatientAnswerChoice
		fields = "__all__"