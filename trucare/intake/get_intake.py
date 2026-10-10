from accounts.models import DoctorLicense, DoctorProfile
from accounts.serializers import DoctorProfileSerializer

from .models import (
    PatientAnswerChoice,
    PatientIntake,
    PatientInfo,
    Insurance,
    PatientCondition,
    PatientAnswer,
    PatientFamilyHistory,
    HealthRecord,
    MedicalHistory,
)
from .payload_serializers import (
    ConditionAnswerSerializer,
    FamilyHistoryPayloadSerializer,
    HealthRecordPayloadSerializer,
    InsuranceSerializer,
    MedicalHistoryPayloadSerializer,
    PatientInfoSerializer,
    PatientIntakeSerializer,
)




class GetIntakeInfo():
    def __init__(self, intake_id):
        self.intake_id = intake_id

    def get_intake_info(self):
        try:
            self.patient_intake = PatientIntake.objects.select_related('doctor').get(id=self.intake_id)
            self.patient_info = self.patient_intake.patient
        except PatientIntake.DoesNotExist:
            return None
        insurances = Insurance.objects.filter(patient=self.patient_info)
        family_history = PatientFamilyHistory.objects.filter(patient=self.patient_info)
        health_records = HealthRecord.objects.filter(patient=self.patient_info)
        medical_history = MedicalHistory.objects.filter(patient=self.patient_info)
        requested_conditions = self.get_requested_conditions()
        condition_answers_data = self.get_condition_answers()

        intake_data = {
            "patient_info": PatientInfoSerializer(self.patient_info).data,
            "patient_intake": PatientIntakeSerializer(self.patient_intake).data,
            "insurances": InsuranceSerializer(insurances, many=True).data,
            "family_history": FamilyHistoryPayloadSerializer(family_history, many=True).data,
            "health_records": HealthRecordPayloadSerializer(health_records, many=True).data,
            "medical_history": MedicalHistoryPayloadSerializer(medical_history, many=True).data,
            "requested_conditions": requested_conditions,
            "condition_answers": condition_answers_data,
        }

        return intake_data

    def get_requested_conditions(self):
        
        requested_conditions = PatientCondition.objects.filter(patient=self.patient_intake, requested=True)
        return [
            {
                "id": item.id,
                "condition_id": item.condition_id,
                "condition_name": item.condition.name,
                "condition_code": item.condition.code,
                "requested": item.requested,
            }
            for item in requested_conditions
        ]

    def get_condition_answers(self):
        

        condition_answers = PatientAnswer.objects.filter(patient=self.patient_intake).select_related("question")
        condition_answers_data = []

        for answer in condition_answers:
            data_dict = {
                "condition_id": answer.question.condition_id,
                "condition_name": answer.question.condition.name,
                "answer_id": answer.id,
                "question_id": answer.question.id,
                "question_text": answer.question.question,
                "text_answer": answer.text_answer,
                "number_answer": str(answer.number_answer) if answer.number_answer is not None else None,
                "boolean_answer": answer.boolean_answer,
                "date_answer": answer.date_answer.isoformat() if answer.date_answer else None,
                "selected_choice_ids": [choice.id for choice in answer.selected_choices.all()] if answer.question.question_type.lower() == "multiple_choice" else [],
            }
            if answer.question.question_type == "MULTIPLE_CHOICE" or answer.question.question_type == "multiple_choice":
                answer_choices = PatientAnswerChoice.objects.filter(answer=answer).select_related('choice')
                data_dict["selected_choices"] = [
                    {
                        "id": choice.choice_id,
                        "text": choice.choice.text,
                    }
                    for choice in answer_choices
                ]
            
            condition_answers_data.append(data_dict)

        return condition_answers_data

    def get_doctor_info(self):
        doctor = self.patient_intake.doctor if hasattr(self.patient_intake, 'doctor') else None
        licenses = DoctorLicense.objects.filter(doctor=doctor) if doctor else []
        doctor_serialized = DoctorProfileSerializer(doctor).data
        state = self.patient_intake.state if hasattr(self.patient_intake, 'state') else None
        return {
            "doctor": doctor_serialized,
            "licenses": licenses,
        }
