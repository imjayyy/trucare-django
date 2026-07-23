
from .models import PatientAnswer, PatientAnswerChoice, PatientCondition, Patient_Info, ConditionQuestion, Choice, ChoiceSet
from .payload_serializers import (
    ConditionAnswerSerializer,
    PatientInfoPayloadSerializer,
    InsurancePayloadSerializer,
    ConditionAnswerPayloadSerializer,
    PatientInfoSerializer,
    InsuranceSerializer,

    )

from .payload_serializers import FamilyHistoryPayloadSerializer, HealthRecordPayloadSerializer, Medical_HistoryPayloadSerializer
from .models import Condition



def validate_list_of_dicts(data, required_fields):
    if not isinstance(data, list):
        raise ValueError("Data must be a list of dictionaries")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each item in the list must be a dictionary")
        for field in required_fields:
            if field not in item:
                raise ValueError(f"Missing required field: {field}")

def validate_non_empty_list(list_data, name = "Data"):
    if not isinstance(list_data, list):
        raise ValueError(f"{name} must be a list")
    if len(list_data) == 0:
        raise ValueError(f"{name} cannot be empty")

class IntakeFormSubmitValidator:
    def __init__(self, form_data: dict):
        # self.form_data = form_data
        self.patient_info = form_data.get("patient_info", {})
        self.insurance = form_data.get("insurance", {})
        self.condition_requests = form_data.get("condition_requests", [])
        self.condition_answers = form_data.get("condition_answers", [])
        self.family_history = form_data.get("family_history", [])
        self.health_records = form_data.get("health_records", [])
        self.medical_history = form_data.get("medical_history", [])

        # validate_non_empty_list(self.condition_requests, "Condition requests")
        validate_non_empty_list(self.condition_answers, "Condition answers")
        # validate_non_empty_list(self.family_history, "Family history")
        validate_non_empty_list(self.health_records, "Health records")
        validate_non_empty_list(self.medical_history, "Medical history")

    def validate(self):
        self.validate_patient_info()
        self.validate_insurance()
        self.validate_family_history()
        self.validate_health_records()
        self.validate_medical_history()
        self.validate_condition_requests()

        return self.patient_info_serializer.instance

    def validate_patient_info(self):
        self.patient_info_serializer = PatientInfoSerializer(data=self.patient_info)
        self.patient_info_serializer.is_valid(raise_exception=True)
        self.patient_info_serializer.save()
        print('Patient info validated and saved:', self.patient_info_serializer.instance)
        return

    def validate_insurance(self):
        patient_id = self.patient_info_serializer.instance.id
        self.insurance["patient"] = patient_id
        serializer = InsuranceSerializer(data=self.insurance)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        print('Insurance validated and saved:', serializer.instance)
        return

    def validate_family_history(self):
        patient_id = self.patient_info_serializer.instance.id
        self.family_history['patient'] = patient_id
        serializer = FamilyHistoryPayloadSerializer(data=self.family_history)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('Family history validated and saved:', serializer.instance)
        return

    def validate_health_records(self):
        patient_id = self.patient_info_serializer.instance.id
        for record in self.health_records:
            record['patient'] = patient_id
        serializer = HealthRecordPayloadSerializer(data=self.health_records, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('Health records validated and saved:', serializer.instance)
        return

    def validate_medical_history(self):
        patient_id = self.patient_info_serializer.instance.id
        for record in self.medical_history:
            record['patient'] = patient_id
        serializer = Medical_HistoryPayloadSerializer(data=self.medical_history, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('Medical history validated and saved:', serializer.instance)
        return

    def validate_condition_requests(self):
        patient_id = self.patient_info_serializer.instance.id
        for condition_id, response in self.condition_requests.items():
            condition = Condition.objects.filter(id=condition_id).first()

            if not condition:
                raise ValueError(f"Condition with id {condition_id} does not exist")
            if response not in ["YES", "NO"]:
                raise ValueError(f"Invalid response for condition {condition_id}: {response}")
            if response == "YES":
                PatientCondition.objects.update_or_create(
                    patient=self.patient_info_serializer.instance,
                    condition=condition,
                    defaults={"requested": True},
                )
                questions = ConditionQuestion.objects.filter(condition=condition)
                for question in questions:
                    answer_data = next((item for item in self.condition_answers if item["question_id"] == question.id), None)
                    if not answer_data:
                        raise ValueError(f"Missing answer for question: {question.id} *{question.question}* of condition {condition_id} {condition.name}")
                    answer_data["patient"] = self.patient_info_serializer.instance.id
                    answer_data["question"] = question.id
                    serializer = ConditionAnswerSerializer(data=answer_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                print(f'Condition {condition_id} and its answers validated and saved.')

                        
        return