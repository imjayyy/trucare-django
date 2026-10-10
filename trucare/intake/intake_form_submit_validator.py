
from django.db import transaction

from .models import (
    Choice,
    Condition,
    ConditionQuestion,
    HealthRecord,
    Insurance,
    MedicalHistory,
    PatientAnswer,
    PatientAnswerChoice,
    PatientCondition,
    PatientFamilyHistory,
    PatientInfo,
    PatientIntake,
)
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
    HealthRecordPayloadSerializer,
    MedicalHistoryPayloadSerializer,
    FamilyHistoryPayloadSerializer,

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
        self.medications = form_data.get("medications", [])
        self.surgeries = form_data.get("surgeries", [])
        self.allergies = form_data.get("allergies", [])
        self.medical_conditions = form_data.get("medical_conditions", [])

        # validate_non_empty_list(self.condition_requests, "Condition requests")
        validate_non_empty_list(self.condition_answers, "Condition answers")
        # validate_non_empty_list(self.family_history, "Family history")
        # validate_non_empty_list(self.HealthRecords, "Health records")
        validate_non_empty_list(self.medical_history, "Medical history")
        validate_non_empty_list(self.medications, "Medications")
        validate_non_empty_list(self.surgeries, "Surgeries")
        validate_non_empty_list(self.allergies, "Allergies")
        validate_non_empty_list(self.medical_conditions, "Medical Conditions")


    @transaction.atomic
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
        self.HealthRecords = self.medical_conditions + self.allergies + self.surgeries + self.medications
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
                        show_when_question = question.show_when
                        if show_when_question:
                            show_when_question_answer = next((item for item in self.condition_answers if item["question_id"] == show_when_question.id), None)
                            if show_when_question_answer and show_when_question_answer.get("text_answer") == "YES":
                                raise ValueError({f"condition_{condition_id}_question_{question.id}": [f"Missing answer for question: {question.id} *{question.question}* of condition {condition_id} {condition.name}"]})
                            else:
                                continue
                        else:
                            raise ValueError({f"condition_{condition_id}_question_{question.id}": [f"Missing answer for question: {question.id} *{question.question}* of condition {condition_id} {condition.name}"],
                                               
                                              })
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
    

class IntakeFormUpdateValidator:
    def __init__(self, form_data: dict, patient_id, intake_id):
        self.patient_id = patient_id
        self.intake_id = intake_id
        self.patient_info = form_data.get("patient_info")
        self.patient_intake = form_data.get("patient_intake")
        self.insurance = form_data.get("insurance", form_data.get("insurances"))
        self.condition_requests = form_data.get("condition_requests")
        self.condition_answers = form_data.get("condition_answers")
        self.family_history = form_data.get("family_history")
        self.HealthRecords = form_data.get("HealthRecords", form_data.get("health_records"))
        self.medical_history = form_data.get("medical_history")
        self.medications = form_data.get("medications", [])
        self.surgeries = form_data.get("surgeries", [])
        self.allergies = form_data.get("allergies", [])
        self.medical_conditions = form_data.get("medical_conditions", [])

    @transaction.atomic
    def validate(self):
        self.patient = PatientInfo.objects.filter(pk=self.patient_id).first()
        self.intake = PatientIntake.objects.filter(pk=self.intake_id, patient=self.patient).first()
        if not self.patient or not self.intake:
            raise ValueError("Patient or intake was not found.")

        self.validate_patient_info()
        self.validate_patient_intake()
        self.validate_insurance()
        self.validate_family_history()
        self.validate_HealthRecords()
        self.validate_medical_history()
        self.validate_condition_requests()

        return {"patient_intake": self.intake, "patient_info": self.patient}

    @staticmethod
    def _save(serializer_class, instance, data, many=False):
        serializer = serializer_class(instance, data=data, partial=instance is not None, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    def validate_patient_info(self):
        if not self.patient_info:
            return
        data = {k: v for k, v in self.patient_info.items() if k not in {"id", "created_at", "updated_at"}}
        self._save(PatientInfoSerializer, self.patient, data)

    def validate_patient_intake(self):
        if not self.patient_intake:
            return
        protected = {
            "id", "patient", "client", "intake_agent", "cordinator",
            "doctor", "allocated_pharmacy", "created_at", "updated_at",
        }
        data = {k: v for k, v in self.patient_intake.items() if k not in protected}
        self._save(PatientIntakeSerializer, self.intake, data)

    def validate_insurance(self):
        if not self.insurance:
            return
        items = [self.insurance] if isinstance(self.insurance, dict) else self.insurance
        for item in items:
            data = {k: v for k, v in item.items() if v not in ("", None) and k not in {"id", "patient"}}
            record = None
            if item.get("id"):
                record = Insurance.objects.filter(pk=item["id"], patient=self.patient).first()
            elif data.get("insurance_type"):
                record = Insurance.objects.filter(patient=self.patient, insurance_type=data["insurance_type"]).first()
            data["patient"] = self.patient.id
            self._save(InsuranceSerializer, record, data)

    def validate_family_history(self):
        if not self.family_history:
            return
        data = {k: v for k, v in self.family_history.items() if k not in {"id", "patient"}}
        data["patient"] = self.patient.id
        record = PatientFamilyHistory.objects.filter(patient=self.patient).first()
        self._save(FamilyHistoryPayloadSerializer, record, data)

    def validate_HealthRecords(self):
        records = self.HealthRecords or (
            self.medical_conditions + self.allergies + self.surgeries + self.medications
        )
        if not records:
            return
        HealthRecord.objects.filter(patient=self.patient).delete()
        for record in records:
            record.pop("id", None)
            record["patient"] = self.patient.id
        self._save(HealthRecordPayloadSerializer, None, records, many=True)

    def validate_medical_history(self):
        if not self.medical_history:
            return
        MedicalHistory.objects.filter(patient=self.patient).delete()
        for record in self.medical_history:
            record.pop("id", None)
            record["patient"] = self.patient.id
        self._save(MedicalHistoryPayloadSerializer, None, self.medical_history, many=True)

    def validate_condition_requests(self):
        for condition_id, response in (self.condition_requests or {}).items():
            if not Condition.objects.filter(id=condition_id).exists():
                raise ValueError(f"Condition with id {condition_id} does not exist")
            if response not in ["YES", "NO"]:
                raise ValueError(f"Invalid response for condition {condition_id}: {response}")
            if response == "YES":
                PatientCondition.objects.update_or_create(
                    patient=self.intake, condition_id=condition_id, defaults={"requested": True},
                )
            elif response == "NO":
                patient_condition = PatientCondition.objects.filter(patient=self.intake, condition_id=condition_id).first()
                if patient_condition:
                    patient_condition.delete()
                questions_ = ConditionQuestion.objects.filter(condition_id=condition_id)
                answers = PatientAnswer.objects.filter(question__in=questions_, patient=self.intake)
                answer_choices = PatientAnswerChoice.objects.filter(answer__in=answers)
                answer_choices.delete()
                answers.delete()
            else:
                PatientCondition.objects.filter(patient=self.intake, condition_id=condition_id).delete()
        self.validate_condition_answers()

    def validate_condition_answers(self):
        for answer_data in self.condition_answers or []:
            question = ConditionQuestion.objects.filter(id=answer_data.get("question_id")).first()
            if not question:
                raise ValueError(f"Question {answer_data.get('question_id')} was not found.")
            data = {k: v for k, v in answer_data.items() if k not in {"id", "selected_choice_ids"}}
            data["patient"] = self.intake.id
            data["question"] = question.id
            existing = PatientAnswer.objects.filter(patient=self.intake, question=question).first()
            answer = self._save(ConditionAnswerSerializer, existing, data).instance

            if "selected_choice_ids" in answer_data:
                selected_ids = answer_data["selected_choice_ids"]
                valid_choices = list(Choice.objects.filter(id__in=selected_ids, choice_set=question.choice_set))
                if len(valid_choices) != len(set(selected_ids)):
                    raise ValueError(f"Invalid choice IDs for question: {question.id} *{question.question}*")
                PatientAnswerChoice.objects.filter(answer=answer).delete()
                PatientAnswerChoice.objects.bulk_create(
                    [PatientAnswerChoice(answer=answer, choice=choice) for choice in valid_choices]
                )


class RefillIntakeFunction():
    def __init__(self, intake_id):
        self.intake_id = intake_id

    def create(self):
        if not self.intake_id:
            raise ValueError("Intake ID is required.")
        intake = PatientIntake.objects.filter(id=self.intake_id).first()
        # patient = intake.patient
        if not intake:
            raise ValueError("Intake not found.")

        intake_original_id = intake.id
        intake.id = None
        intake.pk = None
        intake.cordinator = None
        intake.doctor = None
        intake.allocated_pharmacy = None
        intake.status = "Pending"
        intake.billing_status = None
        intake.billing_notes = None
        intake.cordinator_disposition = None
        intake.internal_notes = None
        intake.audio_file = None
        intake.save()
        print(f'Refilled intake created with new ID: {intake.id}, original ID: {intake_original_id}')
        patient_conditions = PatientCondition.objects.filter(patient=intake_original_id)

        for condition in patient_conditions:
            condition.id = None
            condition.pk = None            
            condition.patient = intake
            condition.denied_reason = None
            condition.denied_by_doctor = False
            condition.save()

        patient_answers = PatientAnswer.objects.filter(patient=intake_original_id)

        for answer in patient_answers:
            patient_answer_choices = PatientAnswerChoice.objects.filter(answer=answer)
            answer.id = None
            answer.pk = None
            answer.patient = intake
            answer.save()
            for answer_choice in patient_answer_choices:
                print(f"answer_choice.answer: {answer_choice.answer}")
                answer_choice.id = None
                answer_choice.pk = None
                answer_choice.answer = answer
                answer_choice.save()
        
        return intake