
from .models import PatientAnswer, PatientAnswerChoice, PatientCondition, PatientInfo, ConditionQuestion, Choice, ChoiceSet
from .payload_serializers import (
    ConditionAnswerSerializer,
    PatientAnswerChoiceSerializer,
    PatientConditionSerializer,
    PatientInfoPayloadSerializer,
    InsurancePayloadSerializer,
    ConditionAnswerPayloadSerializer,
    PatientInfoSerializer,
    InsuranceSerializer,
    PatientIntakeSerializer,

    )

from .payload_serializers import FamilyHistoryPayloadSerializer, HealthRecordPayloadSerializer, MedicalHistoryPayloadSerializer
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
        self.patient_intake = form_data.get("patient_intake", {})
        self.insurance = form_data.get("insurance", {})
        self.condition_requests = form_data.get("condition_requests", [])
        self.condition_answers = form_data.get("condition_answers", [])
        self.family_history = form_data.get("family_history", [])
        self.HealthRecords = form_data.get("HealthRecords", [])
        self.medical_history = form_data.get("medical_history", [])

        # validate_non_empty_list(self.condition_requests, "Condition requests")
        validate_non_empty_list(self.condition_answers, "Condition answers")
        # validate_non_empty_list(self.family_history, "Family history")
        validate_non_empty_list(self.HealthRecords, "Health records")
        validate_non_empty_list(self.medical_history, "Medical history")

    def validate(self):
        self.validate_patient_info()
        self.validate_patient_intake()
        self.validate_insurance()
        self.validate_family_history()
        self.validate_HealthRecords()
        self.validate_medical_history()
        self.validate_condition_requests()
        
        return {"patient_intake": self.patient_intake_serializer.instance,
                "patient_info": self.patient_info_serializer.instance,
                }

    def validate_patient_info(self):
        self.patient_info_serializer = PatientInfoSerializer(data=self.patient_info)
        self.patient_info_serializer.is_valid(raise_exception=True)
        self.patient_info_serializer.save()
        print('Patient info validated and saved:', self.patient_info_serializer.instance)
        return


    def validate_patient_intake(self):
        patient_id = self.patient_info_serializer.instance.id   
        print("testing patient_id",patient_id)
        self.patient_intake['patient'] = patient_id
        self.patient_intake_serializer = PatientIntakeSerializer(data=self.patient_intake)
        self.patient_intake_serializer.is_valid(raise_exception=True)
        self.patient_intake_serializer.save()
        print('Patient intake validated and saved:', self.patient_intake_serializer.instance)
        return


    def validate_insurance(self):
        patient_id = self.patient_info_serializer.instance.id
        self.insurance["patient"] = patient_id
        for key in self.insurance:
            if self.insurance[key] == "":
                self.insurance[key] = None
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

    def validate_HealthRecords(self):
        patient_id = self.patient_info_serializer.instance.id
        for record in self.HealthRecords:
            record['patient'] = patient_id
        serializer = HealthRecordPayloadSerializer(data=self.HealthRecords, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('Health records validated and saved:', serializer.instance)
        return

    def validate_medical_history(self):
        patient_id = self.patient_info_serializer.instance.id
        for record in self.medical_history:
            record['patient'] = patient_id
        serializer = MedicalHistoryPayloadSerializer(data=self.medical_history, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('Medical history validated and saved:', serializer.instance)
        return

    def validate_condition_requests(self):
        patient_id = self.patient_intake_serializer.instance.id
        print("Validating condition requests for patient_id:", self.patient_intake_serializer)

        for condition_id, response in self.condition_requests.items():
            condition = Condition.objects.filter(id=condition_id).first()

            if not condition:
                raise ValueError(f"Condition with id {condition_id} does not exist")
            if response not in ["YES", "NO"]:
                raise ValueError(f"Invalid response for condition {condition_id}: {response}")
            if response == "YES":
                patient_condition_serializer = PatientConditionSerializer(data={"patient": patient_id, "condition": condition_id, "requested": True})
                patient_condition_serializer.is_valid(raise_exception=True)
                patient_condition_serializer.save()

                questions = ConditionQuestion.objects.filter(condition=condition)
                for question in questions:
                    answer_data = next((item for item in self.condition_answers if item["question_id"] == question.id), None)
                    if not answer_data:
                        raise ValueError(f"Missing answer for question: {question.id} *{question.question}* of condition {condition_id} {condition.name}")
                    answer_data["patient"] = patient_id
                    answer_data["question"] = question.id
                    answer_serializer = ConditionAnswerSerializer(data=answer_data)
                    answer_serializer.is_valid(raise_exception=True)
                    answer_serializer.save()
                    if question.question_type == "MULTIPLE_CHOICE" or question.question_type == "multiple_choice":
                        if answer_data and "selected_choice_ids" in answer_data:
                            selected_ids = answer_data["selected_choice_ids"]
                            valid_choices = list(
                            Choice.objects.filter(
                                id__in=selected_ids,
                                choice_set=question.choice_set,
                            )
                        )
                        if len(valid_choices) != len(selected_ids):
                            raise ValueError(f"Invalid choice IDs for question: {question.id} *{question.question}* of condition {condition_id} {condition.name}")
                        answer_data["selected_choice_ids"] = [choice.id for choice in valid_choices]
                        answer_choice_data = []
                        for choice in valid_choices:
                            answer_choice_data.append({
                                "answer": answer_serializer.instance.id,
                                "choice": choice.id
                            })
                        answer_choice_serializer = PatientAnswerChoiceSerializer(data=answer_choice_data, many=True)
                        answer_choice_serializer.is_valid(raise_exception=True)
                        answer_choice_serializer.save()
                    
                
                print(f'Condition {condition_id} and its answers validated and saved.')

                        
        return