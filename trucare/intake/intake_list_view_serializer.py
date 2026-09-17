from .models import (PatientIntake, PatientInfo, Insurance, PatientCondition, PatientAnswer, PatientFamilyHistory, HealthRecord, MedicalHistory)


from rest_framework import serializers
from .payload_serializers import (
    PatientInfoSerializer,
    PatientIntakeSerializer,
    InsuranceSerializer,
    ConditionAnswerSerializer,
    FamilyHistoryPayloadSerializer,
    HealthRecordPayloadSerializer,
    MedicalHistoryPayloadSerializer,
)

class IntakeListViewSerializer(serializers.Serializer):
    patient_info = PatientInfoSerializer()
    patient_intake = PatientIntakeSerializer()
    insurances = InsuranceSerializer(many=True)
    condition_answers = ConditionAnswerSerializer(many=True)


