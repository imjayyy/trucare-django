
from django.db import transaction

from accounts.models import DoctorLicense, DoctorProfile
from scriptbuilder.models import PrescribeAbleItem

from .models import Prescription, PrescriptionItem, PrimaryDrug, SecondaryDrug, Soap_notes
from intake.models import PatientCondition
from intake.models import PatientIntake, PatientCondition 
from .serializers import PrimaryDrugSerializer, SecondaryDrugSerializer, PrescribeAbleItemSerializer, PrescriptionItemSerializer

from intake.payload_serializers import PatientConditionSerializer, PatientIntakeSerializer
from intake.get_intake import GetIntakeInfo
from accounts.serializers import DoctorLicenseSerializer, DoctorProfileSerializer




def get_patient_conditions(intake_id):
    """
    Retrieve all patient conditions from the database.
    """
    return PatientCondition.objects.filter(patient__id=intake_id)


data = [
    {
        "condition":  { "condition_id" : 1},
        "denied" : False,
        "denied_reason" : "",
        "primary_drug" : { "drug_id" : 1},
        "secondary_drugs" : [ { "drug_id" : 2}, { "drug_id" : 3} ]
    },
    {
        "condition":  { "condition_id" : 1},
        "denied" : True,
        "denied_reason" : "Patient is allergic to this medication",
        "primary_drug" : { "drug_id" : 1},
        "secondary_drugs" : [ { "drug_id" : 2}, { "drug_id" : 3} ]
    }
        
]

class ValidatePrescription():
    def __init__(self, prescription_data, Prescription, intake_id):
        self.prescription_data = prescription_data
        self.errors = []
        self.Prescription = Prescription
        self.intake_id = intake_id
        print("prescription_data:", prescription_data)

    @transaction.atomic
    def validate_and_save(self):

        try:
            for item in self.prescription_data:
                condition = item.get("category_id")
                denied = item.get("isDenied")
                denied_reason = item.get("denialReason")
                primary_drug = item.get("primaryDrug")
                secondary_drugs = item.get("secondaryDrugs")


                if denied: 
                    PatientCondition.objects.filter(condition__id=condition, patient__id = self.intake_id).update(denied_by_doctor=True, denied_reason=denied_reason)
                else:
                    print(condition, item.get("category_name"), denied, "denied", denied_reason, "denied reason")

                    primary_drug['prescription'] = self.Prescription.id
                    if "category" not in primary_drug:
                        primary_drug["category"] = condition

                    if 'usual_sig' not in primary_drug:
                        primary_drug['usual_sig'] = primary_drug.get('sig', '')
                        
                    prescription_item = PrescriptionItemSerializer(data=primary_drug)
                    prescription_item.is_valid(raise_exception=True)
                    prescription_item.save()
                    prescription_item_instance = prescription_item.instance
                    pd = PrimaryDrug.objects.create(prescription=self.Prescription, drug=prescription_item_instance)
                    # pd_serializer = PrimaryDrugSerializer(data={"prescription": prescription_item_instance.prescription.id, "drug": prescription_item_instance.id})
                    # pd_serializer.is_valid(raise_exception=True)
                    # pd_serializer.save()
                    sd_querry = PrescribeAbleItem.objects.filter(id__in=[int(id_) for id_ in secondary_drugs])
                    sd_data = PrescribeAbleItemSerializer(sd_querry, many=True).data

                    for sd in sd_data:
                        sd['prescription'] = self.Prescription.id
                        sd['drug'] = sd

                    serializer = PrescriptionItemSerializer(data=sd_data, many=True)
                    serializer.is_valid(raise_exception=True)
                    drugs = serializer.save()
                    drug_ids = [drug.id for drug in drugs]
                    sd_data = []
                    for ids in drug_ids:
                        SecondaryDrug.objects.create(prescription=self.Prescription, drug_id=ids)
                        
                    # sd_serializer = SecondaryDrugSerializer(data=sd_data, many=True)
                    # sd_serializer.is_valid(raise_exception=True)
                    # sd_serializer.save()
            return True, self.errors
        except Exception as e:
            self.errors.append(str(e))
            transaction.set_rollback(True)  
            print("Error occurred during prescription validation and saving:", str(e))

        return len(self.errors) == 0, self.errors








class PrescriptionPDFData:
    def __init__(self, intake_id):
        self.intake_id = intake_id

    def get_pdf_data(self):
        pdf_data = {
            "intake_info": self.get_intake_info(),
            "doctor": self.get_doctor_info(),
            "prescription_items": self.get_prescription_items(),            
            }

        return pdf_data

    def get_intake_info(self):
        try:
            self.intake_info = GetIntakeInfo(self.intake_id).get_intake_info()
            return self.intake_info
        except Exception as e:
            return {"error": str(e)}
    
    def get_doctor_info(self):
        state = self.intake_info.get('patient_info').get('state')
        doctor_id = self.intake_info.get('patient_intake').get('doctor')
        doctor = DoctorProfile.objects.filter(id=doctor_id).first()
        license = DoctorLicense.objects.filter(doctor=doctor, license_state=state).first()
        doctor_profile = DoctorProfileSerializer(doctor).data if doctor else None

        return {
            "doctor": doctor_profile,
            "license": {
                "license_number": license.license_number if license else None,
                "state": license.license_state if license else None
            } 
        }

    def get_prescription_items(self):
        prescription = Prescription.objects.filter(patient_id=self.intake_id).first()
        categories = self.intake_info.get("requested_conditions", [])
        prescription_items = []
        for category in categories:
            category_id = category.get("condition_id")
            patient_conditions = PatientCondition.objects.filter(condition__id=category_id, patient__id=self.intake_id, denied_by_doctor=False)
            print(patient_conditions.count(), "patient_conditions", category_id)
            if patient_conditions.exists():
                primary_drug = PrimaryDrug.objects.filter(prescription=prescription, drug__category__id=category_id).first()
                secondary_drugs = SecondaryDrug.objects.filter(prescription=prescription, drug__category__id=category_id)
                print(secondary_drugs.count(), "secondary_drugs", category_id)
                prescription_items.append({
                    "condition": category,
                    "primary_drug": PrimaryDrugSerializer(primary_drug).data,
                    "secondary_drugs": SecondaryDrugSerializer(secondary_drugs, many=True).data,
                })
            
        return prescription_items





data = [
    {
        "scriptTitle": "Pain condition request?",
        "mode": "select",
        "isDenied": True,
        "denialReason": "no reason",
        "primaryDrug": None,
        "secondaryDrugs": [
            {
                "id": "169",
                "name": "CLEMASTINE FUMARATE syrup (.67mg/5mL)",
                "drug": {
                    "id": 169,
                    "category": 13,
                    "category_name": "Acne condition request?",
                    "item_type": "medication",
                    "name": "CLEMASTINE FUMARATE syrup (.67mg/5mL)",
                    "ndc": "45678-9012",
                    "generic_name": "Omeprazole",
                    "strength": "12",
                    "dosage_form": "ml",
                    "usual_sig": "Take 10-20ml by mouth twice daily",
                    "quantity": "1200",
                    "refills": 3,
                    "duration": "30 days",
                    "description": "NDC: 000 | Unit: ml | Source ID: 6285326109cbfe84d20641e0",
                    "active": True  
                },
                "checked": True
            },
            {
                "id": "101",
                "name": "Omeprazole 20mg",
                "drug": {
                    "id": 101,
                    "category": 13,
                    "category_name": "Acne condition request?",
                    "item_type": "medication",
                    "name": "Omeprazole 20mg",
                    "ndc": "12345-0000",
                    "generic_name": "Omeprazole",
                    "strength": "12",
                    "dosage_form": "Caps",
                    "usual_sig": "Take 1-2 capsules daily",
                    "quantity": "60",
                    "refills": 2,
                    "duration": "30 days",
                    "description": "NDC: 000 | Unit: Caps | Source ID: 61fc34de02f39a272f413d1f",
                    "active": True
                },
                "checked": True
            },
        ],
        "secondaryDrugsChecked": {}
    },
    {
        "scriptTitle": "Muscle relaxer condition request?",
        "mode": "custom",
        "isDenied": False,
        "denialReason": "",
        "primaryDrug": {
            "category": "14",
            "ndc": "121212-1212-121",
            "drugName": "Panadol",
            "quantity": "2",
            "sig": "asdasd",
            "units": "2",
            "daysSupply": "12"
        },
        "secondaryDrugs": [
            {
                "id": "169",
                "name": "CLEMASTINE FUMARATE syrup (.67mg/5mL)",
                "drug": {
                    "id": 169,
                    "category": 13,
                    "category_name": "Acne condition request?",
                    "item_type": "medication",
                    "name": "CLEMASTINE FUMARATE syrup (.67mg/5mL)",
                    "ndc": "45678-9012",
                    "generic_name": "Omeprazole",
                    "strength": "12",
                    "dosage_form": "ml",
                    "usual_sig": "Take 10-20ml by mouth twice daily",
                    "quantity": "1200",
                    "refills": 3,
                    "duration": "30 days",
                    "description": "NDC: 000 | Unit: ml | Source ID: 6285326109cbfe84d20641e0",
                    "active": True
                },
                "checked": True
            },
        ],
        "secondaryDrugsChecked": {}
    },
    {
        "scriptTitle": "Dermatitis/Eczema/Psoriasis condition request?",
        "mode": "select",
        "isDenied": False,
        "denialReason": "",
        "primaryDrug": {
            "medicationId": "163",
            "drugName": "Clemastine Fumarate Syrup",
            "sig": "asdasd",
            "refill": "12",
            "unprescribeDrugs": "ASDASDASD"
        },
        "secondaryDrugs": [
            {
                "id": "169",
                "name": "CLEMASTINE FUMARATE syrup (.67mg/5mL)",
                "drug": {
                    "id": 169,
                    "category": 13,
                    "category_name": "Acne condition request?",
                    "item_type": "medication",
                    "name": "CLEMASTINE FUMARATE syrup (.67mg/5mL)",
                    "ndc": "45678-9012",
                    "generic_name": "Omeprazole",
                    "strength": "12",
                    "dosage_form": "ml",
                    "usual_sig": "Take 10-20ml by mouth twice daily",
                    "quantity": "1200",
                    "refills": 3,
                    "duration": "30 days",
                    "description": "NDC: 000 | Unit: ml | Source ID: 6285326109cbfe84d20641e0",
                    "active": True
                },
                "checked": True
            },
            {
                "id": "101",
                "name": "Omeprazole 20mg",
                "drug": {
                    "id": 101,
                    "category": 13,
                    "category_name": "Acne condition request?",
                    "item_type": "medication",
                    "name": "Omeprazole 20mg",
                    "ndc": "12345-0000",
                    "generic_name": "Omeprazole",
                    "strength": "12",
                    "dosage_form": "Caps",
                    "usual_sig": "Take 1-2 capsules daily",
                    "quantity": "60",
                    "refills": 2,
                    "duration": "30 days",
                    "description": "NDC: 000 | Unit: Caps | Source ID: 61fc34de02f39a272f413d1f",
                    "active": True
                },
                "checked": True
            },
 
        ],
        "secondaryDrugsChecked": {}
    }
]