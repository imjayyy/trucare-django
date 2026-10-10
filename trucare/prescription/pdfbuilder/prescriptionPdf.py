from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import HRFlowable, SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from ..prescription_functions import PrescriptionPDFData
from datetime import datetime
from xml.sax.saxutils import escape
import os

from prescription.models import Prescription, Soap_notes

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.core.files.base import ContentFile
from scriptbuilder.models import LetterOfMedicalNecessity
from trucare import settings

data__ ={
    "intake_info": {
        "patient_info": {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "email": "test@example.com",
            "phone_number": "1234567890",
            "address": "Test Entry",
            "state": "AL",
            "created_at": "2026-08-26T22:45:47.229944Z",
            "updated_at": "2026-08-26T22:45:47.230041Z"
        },
        "patient_intake": {
            "id": 1,
            "height": "1.00",
            "weight": "1.00",
            "status": "Assigned",
            "created_at": "2026-08-26T22:45:47.386322Z",
            "updated_at": "2026-08-26T22:48:23.303829Z",
            "patient": 1,
            "client": 4,
            "intake_agent": 7,
            "cordinator": 5,
            "doctor": 1
        },
        "insurances": [
            {
                "id": 1,
                "insurance_type": "RX",
                "primary_insured": True,
                "insurance_carrier": "Test Entry",
                "carrier_phone": "1234567890",
                "group_id": "123456789",
                "patient_id_rx": "123456789",
                "bin": "123456789",
                "pcn": "123456789",
                "adjuster_name": None,
                "adjuster_phone": None,
                "policy_number": None,
                "claim_number": None,
                "date_of_accident": None,
                "payer_name": None,
                "date_of_injury": None,
                "employer_name": None,
                "created_at": "2026-08-26T22:45:47.409559Z",
                "updated_at": "2026-08-26T22:45:47.409600Z",
                "patient": 1
            }
        ],
        "family_history": [
            {
                "id": 1,
                "asthama": "Yes",
                "bleeding_tendency": "Yes",
                "cancer": "Yes",
                "colitis": "Yes",
                "depression": "Yes",
                "diabetes": "Yes",
                "epilepsy": "Yes",
                "heart_attack": "Yes",
                "high_blood_pressure": "Yes",
                "kidney_disease": "Yes",
                "leukemia": "Yes",
                "migraine": "Yes",
                "schizophrenia": "Yes",
                "stomach_ulcers": "Yes",
                "stroke": "Yes",
                "suicide": "Yes",
                "tuberculosis": "Yes",
                "patient": 1
            }
        ],
        "health_records": [
            {
                "id": 1,
                "record_type": "Medical Conditions",
                "record_date": "1990-01-01",
                "description": "Test Entry",
                "created_at": "2026-08-26T22:45:47.422759Z",
                "updated_at": "2026-08-26T22:45:47.422796Z",
                "patient": 1
            }
        ],
        "medical_history": [
            {
                "id": 1,
                "condition": "Test Entry",
                "diagnosis_date": "1990-01-01",
                "notes": "Test Entry",
                "created_at": "2026-08-26T22:45:47.430334Z",
                "updated_at": "2026-08-26T22:45:47.430369Z",
                "patient": 1
            }
        ],
        "requested_conditions": [
            {
                "id": 1,
                "condition_id": 1,
                "condition_name": "Pain condition request?",
                "condition_code": "pain_request",
                "requested": True
            },
            {
                "id": 2,
                "condition_id": 2,
                "condition_name": "Muscle relaxer condition request?",
                "condition_code": "muscle_relaxer",
                "requested": True
            },
            {
                "id": 3,
                "condition_id": 3,
                "condition_name": "Dermatitis/Eczema/Psoriasis condition request?",
                "condition_code": "dermatitis_eczema_psoriasis",
                "requested": True
            },
            {
                "id": 4,
                "condition_id": 4,
                "condition_name": "Scar/wound/actinic keratosis condition request?",
                "condition_code": "scar_wound_actinic",
                "requested": True
            },
            {
                "id": 5,
                "condition_id": 5,
                "condition_name": "Acid reflux condition request?",
                "condition_code": "acid_reflux",
                "requested": True
            },
            {
                "id": 6,
                "condition_id": 7,
                "condition_name": "Cough condition request?",
                "condition_code": "cough",
                "requested": True
            },
            {
                "id": 7,
                "condition_id": 8,
                "condition_name": "Allergy condition request?",
                "condition_code": "allergy",
                "requested": True
            },
            {
                "id": 8,
                "condition_id": 9,
                "condition_name": "Oral NSAIDs condition request?",
                "condition_code": "oral_nsaids",
                "requested": True
            },
            {
                "id": 9,
                "condition_id": 10,
                "condition_name": "Topical anti-fungal condition request?",
                "condition_code": "topical_antifungal",
                "requested": True
            },
            {
                "id": 10,
                "condition_id": 11,
                "condition_name": "Migraine and Headache condition request?",
                "condition_code": "migraine_headache",
                "requested": True
            },
            {
                "id": 11,
                "condition_id": 12,
                "condition_name": "Acne condition request?",
                "condition_code": "acne",
                "requested": True
            },
            {
                "id": 12,
                "condition_id": 13,
                "condition_name": "Foot bath condition request?",
                "condition_code": "foot_bath",
                "requested": True
            },
            {
                "id": 13,
                "condition_id": 14,
                "condition_name": "Cold sores condition request?",
                "condition_code": "cold_sores",
                "requested": True
            },
            {
                "id": 14,
                "condition_id": 15,
                "condition_name": "Diabetes condition request?",
                "condition_code": "diabetes",
                "requested": True
            },
            {
                "id": 15,
                "condition_id": 16,
                "condition_name": "Laser Therapy Pain treatment request?",
                "condition_code": "laser_therapy_pain",
                "requested": True
            },
            {
                "id": 16,
                "condition_id": 17,
                "condition_name": "Cold Compression Therapy request?",
                "condition_code": "cold_compression",
                "requested": True
            }
        ],
        "condition_answers": [
            {
                "answer_id": 1,
                "question_id": 1,
                "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 2,
                "question_id": 2,
                "question_text": "Diagnosis",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 3,
                "question_id": 3,
                "question_text": "Have you tried other medications for this condition?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 4,
                "question_id": 4,
                "question_text": "Medications",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 5,
                "question_id": 5,
                "question_text": "Have you ever used Lidocaine for pain?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 6,
                "question_id": 6,
                "question_text": "For what pain",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 7,
                "question_id": 7,
                "question_text": "What type of pain are you experiencing?",
                "text_answer": "Aching",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 8,
                "question_id": 8,
                "question_text": "On a scale of 1 to 10, rate severity of your pain",
                "text_answer": "1",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 9,
                "question_id": 9,
                "question_text": "Where is the pain located?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                    24,
                    25,
                    26,
                    27,
                    28,
                    29,
                    30,
                    31
                ],
                "selected_choices": [
                    {
                        "id": 1,
                        "text": "Face"
                    },
                    {
                        "id": 2,
                        "text": "Head"
                    },
                    {
                        "id": 3,
                        "text": "Neck"
                    },
                    {
                        "id": 4,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 5,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 6,
                        "text": "Right Arm"
                    },
                    {
                        "id": 7,
                        "text": "Left Arm"
                    },
                    {
                        "id": 8,
                        "text": "Right elbow"
                    },
                    {
                        "id": 9,
                        "text": "Left elbow"
                    },
                    {
                        "id": 10,
                        "text": "Right wrist"
                    },
                    {
                        "id": 11,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 12,
                        "text": "Right hand"
                    },
                    {
                        "id": 13,
                        "text": "Left hand"
                    },
                    {
                        "id": 14,
                        "text": "Right fingers"
                    },
                    {
                        "id": 15,
                        "text": "Left fingers"
                    },
                    {
                        "id": 16,
                        "text": "Upper back"
                    },
                    {
                        "id": 17,
                        "text": "Lower Back"
                    },
                    {
                        "id": 18,
                        "text": "Chest"
                    },
                    {
                        "id": 19,
                        "text": "Stomach"
                    },
                    {
                        "id": 20,
                        "text": "Right hip"
                    },
                    {
                        "id": 21,
                        "text": "Left Hip"
                    },
                    {
                        "id": 22,
                        "text": "Right thigh"
                    },
                    {
                        "id": 23,
                        "text": "Left thigh"
                    },
                    {
                        "id": 24,
                        "text": "Right knee"
                    },
                    {
                        "id": 25,
                        "text": "Left knee"
                    },
                    {
                        "id": 26,
                        "text": "Right Leg"
                    },
                    {
                        "id": 27,
                        "text": "Left Leg"
                    },
                    {
                        "id": 28,
                        "text": "Right foot & ankle"
                    },
                    {
                        "id": 29,
                        "text": "Left foot & ankle"
                    },
                    {
                        "id": 30,
                        "text": "Right toes"
                    },
                    {
                        "id": 31,
                        "text": "Left toes"
                    }
                ]
            },
            {
                "answer_id": 10,
                "question_id": 10,
                "question_text": "How long have you had this problem (days, weeks, months etc.)?",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 11,
                "question_id": 11,
                "question_text": "How often do you experience the symptoms?",
                "text_answer": "Constantly",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 12,
                "question_id": 12,
                "question_text": "How are your symptoms changing with time?",
                "text_answer": "Getting worse",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 13,
                "question_id": 13,
                "question_text": "How do you think your problem began?",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 14,
                "question_id": 14,
                "question_text": "What activities make the pain worse?",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 15,
                "question_id": 15,
                "question_text": "What activities reduce the pain?",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 16,
                "question_id": 16,
                "question_text": "What prior therapeutic interventions have you tried?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    32,
                    33,
                    34,
                    35,
                    36,
                    37,
                    38,
                    39,
                    40,
                    41,
                    42,
                    43,
                    44,
                    45
                ],
                "selected_choices": [
                    {
                        "id": 60,
                        "text": "Rest"
                    },
                    {
                        "id": 61,
                        "text": "Exercise"
                    },
                    {
                        "id": 62,
                        "text": "PT"
                    },
                    {
                        "id": 63,
                        "text": "injections"
                    },
                    {
                        "id": 64,
                        "text": "anti-inflammatories"
                    },
                    {
                        "id": 65,
                        "text": "corticosteroids"
                    },
                    {
                        "id": 66,
                        "text": "NSAIDs"
                    },
                    {
                        "id": 67,
                        "text": "steroids"
                    },
                    {
                        "id": 68,
                        "text": "opioids"
                    },
                    {
                        "id": 69,
                        "text": "oxycodone"
                    },
                    {
                        "id": 70,
                        "text": "non-prescription medications"
                    },
                    {
                        "id": 71,
                        "text": "prescription medications"
                    },
                    {
                        "id": 72,
                        "text": "muscle relaxants"
                    },
                    {
                        "id": 73,
                        "text": "Other"
                    }
                ]
            },
            {
                "answer_id": 17,
                "question_id": 17,
                "question_text": "Other prior therapeutic intervention",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 18,
                "question_id": 18,
                "question_text": "Which therapeutic interventions afforded improvement of symptoms?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    46,
                    47,
                    48,
                    49,
                    50,
                    51,
                    52,
                    53,
                    54,
                    55,
                    56,
                    57,
                    58,
                    59
                ],
                "selected_choices": [
                    {
                        "id": 60,
                        "text": "Rest"
                    },
                    {
                        "id": 61,
                        "text": "Exercise"
                    },
                    {
                        "id": 62,
                        "text": "PT"
                    },
                    {
                        "id": 63,
                        "text": "injections"
                    },
                    {
                        "id": 64,
                        "text": "anti-inflammatories"
                    },
                    {
                        "id": 65,
                        "text": "corticosteroids"
                    },
                    {
                        "id": 66,
                        "text": "NSAIDs"
                    },
                    {
                        "id": 67,
                        "text": "steroids"
                    },
                    {
                        "id": 68,
                        "text": "opioids"
                    },
                    {
                        "id": 69,
                        "text": "oxycodone"
                    },
                    {
                        "id": 70,
                        "text": "non-prescription medications"
                    },
                    {
                        "id": 71,
                        "text": "prescription medications"
                    },
                    {
                        "id": 72,
                        "text": "muscle relaxants"
                    },
                    {
                        "id": 73,
                        "text": "Other"
                    }
                ]
            },
            {
                "answer_id": 19,
                "question_id": 19,
                "question_text": "Other intervention that afforded improvement",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 20,
                "question_id": 20,
                "question_text": "Do you have a history of seizures, heart arrhythmias, or pacemaker use?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 21,
                "question_id": 21,
                "question_text": "Do you have muscle spasms?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 22,
                "question_id": 22,
                "question_text": "Location of muscle spasms",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    60,
                    61,
                    62,
                    63,
                    64,
                    65,
                    66,
                    67,
                    68,
                    69,
                    70,
                    71,
                    72,
                    73,
                    74,
                    75,
                    76,
                    77,
                    78,
                    79,
                    80,
                    81,
                    82,
                    83,
                    84,
                    85,
                    86,
                    87,
                    88,
                    89,
                    90
                ],
                "selected_choices": [
                    {
                        "id": 1,
                        "text": "Face"
                    },
                    {
                        "id": 2,
                        "text": "Head"
                    },
                    {
                        "id": 3,
                        "text": "Neck"
                    },
                    {
                        "id": 4,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 5,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 6,
                        "text": "Right Arm"
                    },
                    {
                        "id": 7,
                        "text": "Left Arm"
                    },
                    {
                        "id": 8,
                        "text": "Right elbow"
                    },
                    {
                        "id": 9,
                        "text": "Left elbow"
                    },
                    {
                        "id": 10,
                        "text": "Right wrist"
                    },
                    {
                        "id": 11,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 12,
                        "text": "Right hand"
                    },
                    {
                        "id": 13,
                        "text": "Left hand"
                    },
                    {
                        "id": 14,
                        "text": "Right fingers"
                    },
                    {
                        "id": 15,
                        "text": "Left fingers"
                    },
                    {
                        "id": 16,
                        "text": "Upper back"
                    },
                    {
                        "id": 17,
                        "text": "Lower Back"
                    },
                    {
                        "id": 18,
                        "text": "Chest"
                    },
                    {
                        "id": 19,
                        "text": "Stomach"
                    },
                    {
                        "id": 20,
                        "text": "Right hip"
                    },
                    {
                        "id": 21,
                        "text": "Left Hip"
                    },
                    {
                        "id": 22,
                        "text": "Right thigh"
                    },
                    {
                        "id": 23,
                        "text": "Left thigh"
                    },
                    {
                        "id": 24,
                        "text": "Right knee"
                    },
                    {
                        "id": 25,
                        "text": "Left knee"
                    },
                    {
                        "id": 26,
                        "text": "Right Leg"
                    },
                    {
                        "id": 27,
                        "text": "Left Leg"
                    },
                    {
                        "id": 28,
                        "text": "Right foot & ankle"
                    },
                    {
                        "id": 29,
                        "text": "Left foot & ankle"
                    },
                    {
                        "id": 30,
                        "text": "Right toes"
                    },
                    {
                        "id": 31,
                        "text": "Left toes"
                    }
                ]
            },
            {
                "answer_id": 23,
                "question_id": 23,
                "question_text": "Do you have any cramping or tightening in any muscle?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 24,
                "question_id": 24,
                "question_text": "Location of cramping/tightening",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    91,
                    92,
                    93,
                    94,
                    95,
                    96,
                    97,
                    98,
                    99,
                    100,
                    101,
                    102,
                    103,
                    104,
                    105,
                    106,
                    107,
                    108,
                    109,
                    110,
                    111,
                    112,
                    113,
                    114,
                    115,
                    116,
                    117,
                    118,
                    119,
                    120,
                    121
                ],
                "selected_choices": [
                    {
                        "id": 1,
                        "text": "Face"
                    },
                    {
                        "id": 2,
                        "text": "Head"
                    },
                    {
                        "id": 3,
                        "text": "Neck"
                    },
                    {
                        "id": 4,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 5,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 6,
                        "text": "Right Arm"
                    },
                    {
                        "id": 7,
                        "text": "Left Arm"
                    },
                    {
                        "id": 8,
                        "text": "Right elbow"
                    },
                    {
                        "id": 9,
                        "text": "Left elbow"
                    },
                    {
                        "id": 10,
                        "text": "Right wrist"
                    },
                    {
                        "id": 11,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 12,
                        "text": "Right hand"
                    },
                    {
                        "id": 13,
                        "text": "Left hand"
                    },
                    {
                        "id": 14,
                        "text": "Right fingers"
                    },
                    {
                        "id": 15,
                        "text": "Left fingers"
                    },
                    {
                        "id": 16,
                        "text": "Upper back"
                    },
                    {
                        "id": 17,
                        "text": "Lower Back"
                    },
                    {
                        "id": 18,
                        "text": "Chest"
                    },
                    {
                        "id": 19,
                        "text": "Stomach"
                    },
                    {
                        "id": 20,
                        "text": "Right hip"
                    },
                    {
                        "id": 21,
                        "text": "Left Hip"
                    },
                    {
                        "id": 22,
                        "text": "Right thigh"
                    },
                    {
                        "id": 23,
                        "text": "Left thigh"
                    },
                    {
                        "id": 24,
                        "text": "Right knee"
                    },
                    {
                        "id": 25,
                        "text": "Left knee"
                    },
                    {
                        "id": 26,
                        "text": "Right Leg"
                    },
                    {
                        "id": 27,
                        "text": "Left Leg"
                    },
                    {
                        "id": 28,
                        "text": "Right foot & ankle"
                    },
                    {
                        "id": 29,
                        "text": "Left foot & ankle"
                    },
                    {
                        "id": 30,
                        "text": "Right toes"
                    },
                    {
                        "id": 31,
                        "text": "Left toes"
                    }
                ]
            },
            {
                "answer_id": 25,
                "question_id": 100,
                "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 26,
                "question_id": 101,
                "question_text": "Diagnosis",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 27,
                "question_id": 102,
                "question_text": "Have you tried other medications for this condition?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 28,
                "question_id": 103,
                "question_text": "Medication name",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 29,
                "question_id": 104,
                "question_text": "Did it work?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 30,
                "question_id": 105,
                "question_text": "Location of lesion",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    122,
                    123,
                    124,
                    125,
                    126,
                    127,
                    128,
                    129,
                    130,
                    131,
                    132,
                    133,
                    134,
                    135,
                    136,
                    137,
                    138,
                    139,
                    140,
                    141,
                    142,
                    143,
                    144,
                    145,
                    146,
                    147,
                    148,
                    149,
                    150,
                    151,
                    152
                ],
                "selected_choices": [
                    {
                        "id": 1,
                        "text": "Face"
                    },
                    {
                        "id": 2,
                        "text": "Head"
                    },
                    {
                        "id": 3,
                        "text": "Neck"
                    },
                    {
                        "id": 4,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 5,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 6,
                        "text": "Right Arm"
                    },
                    {
                        "id": 7,
                        "text": "Left Arm"
                    },
                    {
                        "id": 8,
                        "text": "Right elbow"
                    },
                    {
                        "id": 9,
                        "text": "Left elbow"
                    },
                    {
                        "id": 10,
                        "text": "Right wrist"
                    },
                    {
                        "id": 11,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 12,
                        "text": "Right hand"
                    },
                    {
                        "id": 13,
                        "text": "Left hand"
                    },
                    {
                        "id": 14,
                        "text": "Right fingers"
                    },
                    {
                        "id": 15,
                        "text": "Left fingers"
                    },
                    {
                        "id": 16,
                        "text": "Upper back"
                    },
                    {
                        "id": 17,
                        "text": "Lower Back"
                    },
                    {
                        "id": 18,
                        "text": "Chest"
                    },
                    {
                        "id": 19,
                        "text": "Stomach"
                    },
                    {
                        "id": 20,
                        "text": "Right hip"
                    },
                    {
                        "id": 21,
                        "text": "Left Hip"
                    },
                    {
                        "id": 22,
                        "text": "Right thigh"
                    },
                    {
                        "id": 23,
                        "text": "Left thigh"
                    },
                    {
                        "id": 24,
                        "text": "Right knee"
                    },
                    {
                        "id": 25,
                        "text": "Left knee"
                    },
                    {
                        "id": 26,
                        "text": "Right Leg"
                    },
                    {
                        "id": 27,
                        "text": "Left Leg"
                    },
                    {
                        "id": 28,
                        "text": "Right foot & ankle"
                    },
                    {
                        "id": 29,
                        "text": "Left foot & ankle"
                    },
                    {
                        "id": 30,
                        "text": "Right toes"
                    },
                    {
                        "id": 31,
                        "text": "Left toes"
                    }
                ]
            },
            {
                "answer_id": 31,
                "question_id": 106,
                "question_text": "Size of lesion",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 32,
                "question_id": 92,
                "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 33,
                "question_id": 93,
                "question_text": "Diagnosis",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 34,
                "question_id": 94,
                "question_text": "Have you tried other medications for this condition?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 35,
                "question_id": 95,
                "question_text": "Medication name",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 36,
                "question_id": 96,
                "question_text": "Did it work?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 37,
                "question_id": 97,
                "question_text": "Location of lesion",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    153,
                    154,
                    155,
                    156,
                    157,
                    158,
                    159,
                    160,
                    161,
                    162,
                    163,
                    164,
                    165,
                    166,
                    167,
                    168,
                    169,
                    170,
                    171,
                    172,
                    173,
                    174,
                    175,
                    176,
                    177,
                    178,
                    179,
                    180,
                    181,
                    182,
                    183
                ],
                "selected_choices": [
                    {
                        "id": 1,
                        "text": "Face"
                    },
                    {
                        "id": 2,
                        "text": "Head"
                    },
                    {
                        "id": 3,
                        "text": "Neck"
                    },
                    {
                        "id": 4,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 5,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 6,
                        "text": "Right Arm"
                    },
                    {
                        "id": 7,
                        "text": "Left Arm"
                    },
                    {
                        "id": 8,
                        "text": "Right elbow"
                    },
                    {
                        "id": 9,
                        "text": "Left elbow"
                    },
                    {
                        "id": 10,
                        "text": "Right wrist"
                    },
                    {
                        "id": 11,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 12,
                        "text": "Right hand"
                    },
                    {
                        "id": 13,
                        "text": "Left hand"
                    },
                    {
                        "id": 14,
                        "text": "Right fingers"
                    },
                    {
                        "id": 15,
                        "text": "Left fingers"
                    },
                    {
                        "id": 16,
                        "text": "Upper back"
                    },
                    {
                        "id": 17,
                        "text": "Lower Back"
                    },
                    {
                        "id": 18,
                        "text": "Chest"
                    },
                    {
                        "id": 19,
                        "text": "Stomach"
                    },
                    {
                        "id": 20,
                        "text": "Right hip"
                    },
                    {
                        "id": 21,
                        "text": "Left Hip"
                    },
                    {
                        "id": 22,
                        "text": "Right thigh"
                    },
                    {
                        "id": 23,
                        "text": "Left thigh"
                    },
                    {
                        "id": 24,
                        "text": "Right knee"
                    },
                    {
                        "id": 25,
                        "text": "Left knee"
                    },
                    {
                        "id": 26,
                        "text": "Right Leg"
                    },
                    {
                        "id": 27,
                        "text": "Left Leg"
                    },
                    {
                        "id": 28,
                        "text": "Right foot & ankle"
                    },
                    {
                        "id": 29,
                        "text": "Left foot & ankle"
                    },
                    {
                        "id": 30,
                        "text": "Right toes"
                    },
                    {
                        "id": 31,
                        "text": "Left toes"
                    }
                ]
            },
            {
                "answer_id": 38,
                "question_id": 98,
                "question_text": "Size of lesion",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 39,
                "question_id": 99,
                "question_text": "Cause of lesion",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 40,
                "question_id": 83,
                "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 41,
                "question_id": 84,
                "question_text": "Diagnosis",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 42,
                "question_id": 85,
                "question_text": "Have you tried other medications for this condition?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 43,
                "question_id": 86,
                "question_text": "Medication name",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 44,
                "question_id": 87,
                "question_text": "Did it work?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 45,
                "question_id": 88,
                "question_text": "Do you have heartburn?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 46,
                "question_id": 89,
                "question_text": "On a scale of 1 to 10, rate heartburn severity",
                "text_answer": "1",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 47,
                "question_id": 90,
                "question_text": "How frequently does it occur?",
                "text_answer": "Constantly",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 48,
                "question_id": 91,
                "question_text": "Do you have bloating or gassy feelings?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 49,
                "question_id": 69,
                "question_text": "Do you have a cough?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 50,
                "question_id": 70,
                "question_text": "Is your cough dry (no phlegm)?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 51,
                "question_id": 71,
                "question_text": "How would you rate the severity of your cough?",
                "text_answer": "Mild",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 52,
                "question_id": 72,
                "question_text": "Is your cough due to an allergy?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 53,
                "question_id": 73,
                "question_text": "Allergy to what?",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 54,
                "question_id": 74,
                "question_text": "Do you have any type of allergy (food, drug, environment, dust chemical, hay, animal, insect, material, etc)?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 55,
                "question_id": 75,
                "question_text": "Allergy to",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 56,
                "question_id": 76,
                "question_text": "Reaction",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 57,
                "question_id": 77,
                "question_text": "What have you tried to alleviate your allergy symptoms?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    184,
                    185,
                    186,
                    187,
                    188
                ],
                "selected_choices": [
                    {
                        "id": 97,
                        "text": "Antihistamines"
                    },
                    {
                        "id": 98,
                        "text": "allergy shots"
                    },
                    {
                        "id": 99,
                        "text": "Steroids"
                    },
                    {
                        "id": 100,
                        "text": "Other"
                    },
                    {
                        "id": 101,
                        "text": "None"
                    }
                ]
            },
            {
                "answer_id": 58,
                "question_id": 78,
                "question_text": "Did antihistamines help?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 59,
                "question_id": 79,
                "question_text": "Did allergy shots help?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 60,
                "question_id": 80,
                "question_text": "Did steroids help?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 61,
                "question_id": 81,
                "question_text": "Other method name",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 62,
                "question_id": 82,
                "question_text": "Did other method help?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 63,
                "question_id": 25,
                "question_text": "What areas are affected by muscle or joint inflammation?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    189,
                    190,
                    191,
                    192,
                    193,
                    194,
                    195,
                    196,
                    197,
                    198,
                    199,
                    200,
                    201,
                    202,
                    203,
                    204,
                    205,
                    206,
                    207,
                    208,
                    209,
                    210,
                    211,
                    212,
                    213,
                    214,
                    215,
                    216,
                    217,
                    218,
                    219
                ],
                "selected_choices": [
                    {
                        "id": 1,
                        "text": "Face"
                    },
                    {
                        "id": 2,
                        "text": "Head"
                    },
                    {
                        "id": 3,
                        "text": "Neck"
                    },
                    {
                        "id": 4,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 5,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 6,
                        "text": "Right Arm"
                    },
                    {
                        "id": 7,
                        "text": "Left Arm"
                    },
                    {
                        "id": 8,
                        "text": "Right elbow"
                    },
                    {
                        "id": 9,
                        "text": "Left elbow"
                    },
                    {
                        "id": 10,
                        "text": "Right wrist"
                    },
                    {
                        "id": 11,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 12,
                        "text": "Right hand"
                    },
                    {
                        "id": 13,
                        "text": "Left hand"
                    },
                    {
                        "id": 14,
                        "text": "Right fingers"
                    },
                    {
                        "id": 15,
                        "text": "Left fingers"
                    },
                    {
                        "id": 16,
                        "text": "Upper back"
                    },
                    {
                        "id": 17,
                        "text": "Lower Back"
                    },
                    {
                        "id": 18,
                        "text": "Chest"
                    },
                    {
                        "id": 19,
                        "text": "Stomach"
                    },
                    {
                        "id": 20,
                        "text": "Right hip"
                    },
                    {
                        "id": 21,
                        "text": "Left Hip"
                    },
                    {
                        "id": 22,
                        "text": "Right thigh"
                    },
                    {
                        "id": 23,
                        "text": "Left thigh"
                    },
                    {
                        "id": 24,
                        "text": "Right knee"
                    },
                    {
                        "id": 25,
                        "text": "Left knee"
                    },
                    {
                        "id": 26,
                        "text": "Right Leg"
                    },
                    {
                        "id": 27,
                        "text": "Left Leg"
                    },
                    {
                        "id": 28,
                        "text": "Right foot & ankle"
                    },
                    {
                        "id": 29,
                        "text": "Left foot & ankle"
                    },
                    {
                        "id": 30,
                        "text": "Right toes"
                    },
                    {
                        "id": 31,
                        "text": "Left toes"
                    }
                ]
            },
            {
                "answer_id": 64,
                "question_id": 26,
                "question_text": "How long have you experienced inflammation?",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 65,
                "question_id": 27,
                "question_text": "Past inflammation treatments",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    220,
                    221,
                    222,
                    223,
                    224,
                    225,
                    226,
                    227,
                    228,
                    229,
                    230,
                    231,
                    232,
                    233
                ],
                "selected_choices": [
                    {
                        "id": 60,
                        "text": "Rest"
                    },
                    {
                        "id": 61,
                        "text": "Exercise"
                    },
                    {
                        "id": 62,
                        "text": "PT"
                    },
                    {
                        "id": 63,
                        "text": "injections"
                    },
                    {
                        "id": 64,
                        "text": "anti-inflammatories"
                    },
                    {
                        "id": 65,
                        "text": "corticosteroids"
                    },
                    {
                        "id": 66,
                        "text": "NSAIDs"
                    },
                    {
                        "id": 67,
                        "text": "steroids"
                    },
                    {
                        "id": 68,
                        "text": "opioids"
                    },
                    {
                        "id": 69,
                        "text": "oxycodone"
                    },
                    {
                        "id": 70,
                        "text": "non-prescription medications"
                    },
                    {
                        "id": 71,
                        "text": "prescription medications"
                    },
                    {
                        "id": 72,
                        "text": "muscle relaxants"
                    },
                    {
                        "id": 73,
                        "text": "Other"
                    }
                ]
            },
            {
                "answer_id": 66,
                "question_id": 28,
                "question_text": "Other past inflammation treatment",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 67,
                "question_id": 62,
                "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 68,
                "question_id": 63,
                "question_text": "Diagnosis",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 69,
                "question_id": 64,
                "question_text": "Have you tried other medications for this condition?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 70,
                "question_id": 65,
                "question_text": "Medication name",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 71,
                "question_id": 66,
                "question_text": "Did it work?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 72,
                "question_id": 67,
                "question_text": "Location of lesion",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    234,
                    235,
                    236,
                    237,
                    238,
                    239,
                    240,
                    241,
                    242,
                    243,
                    244,
                    245,
                    246,
                    247,
                    248,
                    249,
                    250,
                    251,
                    252,
                    253,
                    254,
                    255,
                    256,
                    257,
                    258,
                    259,
                    260,
                    261,
                    262,
                    263,
                    264
                ],
                "selected_choices": [
                    {
                        "id": 1,
                        "text": "Face"
                    },
                    {
                        "id": 2,
                        "text": "Head"
                    },
                    {
                        "id": 3,
                        "text": "Neck"
                    },
                    {
                        "id": 4,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 5,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 6,
                        "text": "Right Arm"
                    },
                    {
                        "id": 7,
                        "text": "Left Arm"
                    },
                    {
                        "id": 8,
                        "text": "Right elbow"
                    },
                    {
                        "id": 9,
                        "text": "Left elbow"
                    },
                    {
                        "id": 10,
                        "text": "Right wrist"
                    },
                    {
                        "id": 11,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 12,
                        "text": "Right hand"
                    },
                    {
                        "id": 13,
                        "text": "Left hand"
                    },
                    {
                        "id": 14,
                        "text": "Right fingers"
                    },
                    {
                        "id": 15,
                        "text": "Left fingers"
                    },
                    {
                        "id": 16,
                        "text": "Upper back"
                    },
                    {
                        "id": 17,
                        "text": "Lower Back"
                    },
                    {
                        "id": 18,
                        "text": "Chest"
                    },
                    {
                        "id": 19,
                        "text": "Stomach"
                    },
                    {
                        "id": 20,
                        "text": "Right hip"
                    },
                    {
                        "id": 21,
                        "text": "Left Hip"
                    },
                    {
                        "id": 22,
                        "text": "Right thigh"
                    },
                    {
                        "id": 23,
                        "text": "Left thigh"
                    },
                    {
                        "id": 24,
                        "text": "Right knee"
                    },
                    {
                        "id": 25,
                        "text": "Left knee"
                    },
                    {
                        "id": 26,
                        "text": "Right Leg"
                    },
                    {
                        "id": 27,
                        "text": "Left Leg"
                    },
                    {
                        "id": 28,
                        "text": "Right foot & ankle"
                    },
                    {
                        "id": 29,
                        "text": "Left foot & ankle"
                    },
                    {
                        "id": 30,
                        "text": "Right toes"
                    },
                    {
                        "id": 31,
                        "text": "Left toes"
                    }
                ]
            },
            {
                "answer_id": 73,
                "question_id": 68,
                "question_text": "Size of lesion",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 74,
                "question_id": 47,
                "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 75,
                "question_id": 48,
                "question_text": "Diagnosis",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 76,
                "question_id": 49,
                "question_text": "Do you have migraines 15 or more times a month?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 77,
                "question_id": 50,
                "question_text": "Have you tried other medications for this condition?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 78,
                "question_id": 51,
                "question_text": "Medication name",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 79,
                "question_id": 52,
                "question_text": "Did it work?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 80,
                "question_id": 53,
                "question_text": "Have you been previously diagnosed with migraine by a health professional?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 81,
                "question_id": 54,
                "question_text": "Is your headache throbbing, pulsating or pounding?",
                "text_answer": "Throbbing",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 82,
                "question_id": 55,
                "question_text": "Where is the head pain located?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    265,
                    266,
                    267,
                    268,
                    269
                ],
                "selected_choices": [
                    {
                        "id": 81,
                        "text": "Left"
                    },
                    {
                        "id": 82,
                        "text": "Right"
                    },
                    {
                        "id": 83,
                        "text": "Both Sides"
                    },
                    {
                        "id": 84,
                        "text": "Front"
                    },
                    {
                        "id": 85,
                        "text": "Back"
                    }
                ]
            },
            {
                "answer_id": 83,
                "question_id": 56,
                "question_text": "How often does your headache occur?",
                "text_answer": "Constantly",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 84,
                "question_id": 57,
                "question_text": "Do you experience symptoms prior to the migraine?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    270,
                    271,
                    272,
                    273,
                    274
                ],
                "selected_choices": [
                    {
                        "id": 86,
                        "text": "Light Sensitivity"
                    },
                    {
                        "id": 87,
                        "text": "Visual Symptoms"
                    },
                    {
                        "id": 88,
                        "text": "Dizziness"
                    },
                    {
                        "id": 89,
                        "text": "Nausea"
                    },
                    {
                        "id": 90,
                        "text": "Vomiting"
                    }
                ]
            },
            {
                "answer_id": 85,
                "question_id": 58,
                "question_text": "Are you currently taking any migraine medication(s)?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 86,
                "question_id": 59,
                "question_text": "Current migraine medication name",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 87,
                "question_id": 60,
                "question_text": "Do you have a history of hypertension, stroke, or any type of heart disease?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 88,
                "question_id": 61,
                "question_text": "Disease history types",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    275,
                    276,
                    277
                ],
                "selected_choices": [
                    {
                        "id": 91,
                        "text": "Hypertension"
                    },
                    {
                        "id": 92,
                        "text": "Stroke"
                    },
                    {
                        "id": 93,
                        "text": "Heart Disease"
                    }
                ]
            },
            {
                "answer_id": 89,
                "question_id": 112,
                "question_text": "Where is the location of your acne?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    278,
                    279,
                    280,
                    281,
                    282,
                    283,
                    284,
                    285,
                    286,
                    287,
                    288,
                    289,
                    290,
                    291,
                    292,
                    293,
                    294,
                    295,
                    296,
                    297,
                    298,
                    299,
                    300,
                    301,
                    302,
                    303,
                    304,
                    305,
                    306,
                    307,
                    308
                ],
                "selected_choices": [
                    {
                        "id": 1,
                        "text": "Face"
                    },
                    {
                        "id": 2,
                        "text": "Head"
                    },
                    {
                        "id": 3,
                        "text": "Neck"
                    },
                    {
                        "id": 4,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 5,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 6,
                        "text": "Right Arm"
                    },
                    {
                        "id": 7,
                        "text": "Left Arm"
                    },
                    {
                        "id": 8,
                        "text": "Right elbow"
                    },
                    {
                        "id": 9,
                        "text": "Left elbow"
                    },
                    {
                        "id": 10,
                        "text": "Right wrist"
                    },
                    {
                        "id": 11,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 12,
                        "text": "Right hand"
                    },
                    {
                        "id": 13,
                        "text": "Left hand"
                    },
                    {
                        "id": 14,
                        "text": "Right fingers"
                    },
                    {
                        "id": 15,
                        "text": "Left fingers"
                    },
                    {
                        "id": 16,
                        "text": "Upper back"
                    },
                    {
                        "id": 17,
                        "text": "Lower Back"
                    },
                    {
                        "id": 18,
                        "text": "Chest"
                    },
                    {
                        "id": 19,
                        "text": "Stomach"
                    },
                    {
                        "id": 20,
                        "text": "Right hip"
                    },
                    {
                        "id": 21,
                        "text": "Left Hip"
                    },
                    {
                        "id": 22,
                        "text": "Right thigh"
                    },
                    {
                        "id": 23,
                        "text": "Left thigh"
                    },
                    {
                        "id": 24,
                        "text": "Right knee"
                    },
                    {
                        "id": 25,
                        "text": "Left knee"
                    },
                    {
                        "id": 26,
                        "text": "Right Leg"
                    },
                    {
                        "id": 27,
                        "text": "Left Leg"
                    },
                    {
                        "id": 28,
                        "text": "Right foot & ankle"
                    },
                    {
                        "id": 29,
                        "text": "Left foot & ankle"
                    },
                    {
                        "id": 30,
                        "text": "Right toes"
                    },
                    {
                        "id": 31,
                        "text": "Left toes"
                    }
                ]
            },
            {
                "answer_id": 90,
                "question_id": 113,
                "question_text": "How many bumps do you have?",
                "text_answer": "1-2",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 91,
                "question_id": 114,
                "question_text": "Has this caused scabbing or scaring?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 92,
                "question_id": 115,
                "question_text": "Do you clean this location regularly?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 93,
                "question_id": 116,
                "question_text": "How many of these bumps are full of pus or fluid?",
                "text_answer": "3-5",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 94,
                "question_id": 117,
                "question_text": "What previous methods have you used to treat acne?",
                "text_answer": "Face washes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 95,
                "question_id": 40,
                "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 96,
                "question_id": 41,
                "question_text": "Diagnosis",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 97,
                "question_id": 42,
                "question_text": "Have you tried other medications for this condition?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 98,
                "question_id": 43,
                "question_text": "Medication name",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 99,
                "question_id": 44,
                "question_text": "Did it work?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 100,
                "question_id": 45,
                "question_text": "Location of lesion",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    309,
                    310,
                    311,
                    312,
                    313,
                    314,
                    315,
                    316,
                    317,
                    318,
                    319,
                    320,
                    321,
                    322,
                    323,
                    324,
                    325,
                    326,
                    327,
                    328,
                    329,
                    330,
                    331,
                    332,
                    333,
                    334,
                    335,
                    336,
                    337,
                    338,
                    339
                ],
                "selected_choices": [
                    {
                        "id": 1,
                        "text": "Face"
                    },
                    {
                        "id": 2,
                        "text": "Head"
                    },
                    {
                        "id": 3,
                        "text": "Neck"
                    },
                    {
                        "id": 4,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 5,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 6,
                        "text": "Right Arm"
                    },
                    {
                        "id": 7,
                        "text": "Left Arm"
                    },
                    {
                        "id": 8,
                        "text": "Right elbow"
                    },
                    {
                        "id": 9,
                        "text": "Left elbow"
                    },
                    {
                        "id": 10,
                        "text": "Right wrist"
                    },
                    {
                        "id": 11,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 12,
                        "text": "Right hand"
                    },
                    {
                        "id": 13,
                        "text": "Left hand"
                    },
                    {
                        "id": 14,
                        "text": "Right fingers"
                    },
                    {
                        "id": 15,
                        "text": "Left fingers"
                    },
                    {
                        "id": 16,
                        "text": "Upper back"
                    },
                    {
                        "id": 17,
                        "text": "Lower Back"
                    },
                    {
                        "id": 18,
                        "text": "Chest"
                    },
                    {
                        "id": 19,
                        "text": "Stomach"
                    },
                    {
                        "id": 20,
                        "text": "Right hip"
                    },
                    {
                        "id": 21,
                        "text": "Left Hip"
                    },
                    {
                        "id": 22,
                        "text": "Right thigh"
                    },
                    {
                        "id": 23,
                        "text": "Left thigh"
                    },
                    {
                        "id": 24,
                        "text": "Right knee"
                    },
                    {
                        "id": 25,
                        "text": "Left knee"
                    },
                    {
                        "id": 26,
                        "text": "Right Leg"
                    },
                    {
                        "id": 27,
                        "text": "Left Leg"
                    },
                    {
                        "id": 28,
                        "text": "Right foot & ankle"
                    },
                    {
                        "id": 29,
                        "text": "Left foot & ankle"
                    },
                    {
                        "id": 30,
                        "text": "Right toes"
                    },
                    {
                        "id": 31,
                        "text": "Left toes"
                    }
                ]
            },
            {
                "answer_id": 101,
                "question_id": 46,
                "question_text": "Size of lesion",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 102,
                "question_id": 29,
                "question_text": "Do you currently have blisters?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 103,
                "question_id": 30,
                "question_text": "Location of blisters",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    340,
                    341,
                    342,
                    343,
                    344,
                    345,
                    346,
                    347,
                    348,
                    349,
                    350,
                    351,
                    352,
                    353,
                    354,
                    355,
                    356,
                    357,
                    358,
                    359,
                    360,
                    361,
                    362,
                    363,
                    364,
                    365,
                    366,
                    367,
                    368,
                    369,
                    370
                ],
                "selected_choices": [
                    {
                        "id": 1,
                        "text": "Face"
                    },
                    {
                        "id": 2,
                        "text": "Head"
                    },
                    {
                        "id": 3,
                        "text": "Neck"
                    },
                    {
                        "id": 4,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 5,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 6,
                        "text": "Right Arm"
                    },
                    {
                        "id": 7,
                        "text": "Left Arm"
                    },
                    {
                        "id": 8,
                        "text": "Right elbow"
                    },
                    {
                        "id": 9,
                        "text": "Left elbow"
                    },
                    {
                        "id": 10,
                        "text": "Right wrist"
                    },
                    {
                        "id": 11,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 12,
                        "text": "Right hand"
                    },
                    {
                        "id": 13,
                        "text": "Left hand"
                    },
                    {
                        "id": 14,
                        "text": "Right fingers"
                    },
                    {
                        "id": 15,
                        "text": "Left fingers"
                    },
                    {
                        "id": 16,
                        "text": "Upper back"
                    },
                    {
                        "id": 17,
                        "text": "Lower Back"
                    },
                    {
                        "id": 18,
                        "text": "Chest"
                    },
                    {
                        "id": 19,
                        "text": "Stomach"
                    },
                    {
                        "id": 20,
                        "text": "Right hip"
                    },
                    {
                        "id": 21,
                        "text": "Left Hip"
                    },
                    {
                        "id": 22,
                        "text": "Right thigh"
                    },
                    {
                        "id": 23,
                        "text": "Left thigh"
                    },
                    {
                        "id": 24,
                        "text": "Right knee"
                    },
                    {
                        "id": 25,
                        "text": "Left knee"
                    },
                    {
                        "id": 26,
                        "text": "Right Leg"
                    },
                    {
                        "id": 27,
                        "text": "Left Leg"
                    },
                    {
                        "id": 28,
                        "text": "Right foot & ankle"
                    },
                    {
                        "id": 29,
                        "text": "Left foot & ankle"
                    },
                    {
                        "id": 30,
                        "text": "Right toes"
                    },
                    {
                        "id": 31,
                        "text": "Left toes"
                    }
                ]
            },
            {
                "answer_id": 104,
                "question_id": 31,
                "question_text": "Describe the blisters",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    371,
                    372,
                    373,
                    374
                ],
                "selected_choices": [
                    {
                        "id": 74,
                        "text": "Single"
                    },
                    {
                        "id": 75,
                        "text": "Multiple"
                    },
                    {
                        "id": 76,
                        "text": "Small (pinhead size)"
                    },
                    {
                        "id": 77,
                        "text": "Large (pea size)"
                    }
                ]
            },
            {
                "answer_id": 105,
                "question_id": 32,
                "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 106,
                "question_id": 33,
                "question_text": "Diagnosis",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 107,
                "question_id": 34,
                "question_text": "Have you tried other medications for this condition?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 108,
                "question_id": 35,
                "question_text": "Medication name",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 109,
                "question_id": 36,
                "question_text": "Did it work?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 110,
                "question_id": 37,
                "question_text": "Have you had previous cold sore episodes?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 111,
                "question_id": 38,
                "question_text": "Were the previous episodes similar to the current episode?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 112,
                "question_id": 39,
                "question_text": "Do you concurrently have eye symptoms, ear symptoms, or severe headaches?",
                "text_answer": "Yes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 113,
                "question_id": 107,
                "question_text": "Are you currently living with any of the following conditions?",
                "text_answer": "Diabetes or Prediabetes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 114,
                "question_id": 108,
                "question_text": "Which type of diabetes?",
                "text_answer": "Prediabetes",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 115,
                "question_id": 109,
                "question_text": "What was your most recent A1c result?",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 116,
                "question_id": 110,
                "question_text": "What was the approximate date of your most recent A1c results?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": "1990-01-01",
                "selected_choice_ids": []
            },
            {
                "answer_id": 117,
                "question_id": 111,
                "question_text": "Have you ever been diagnosed with any of the following?",
                "text_answer": "Kidney or Renal Disease",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 118,
                "question_id": 118,
                "question_text": "Where is the pain located?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    375,
                    376,
                    377,
                    378,
                    379,
                    380,
                    381,
                    382,
                    383,
                    384,
                    385,
                    386,
                    387,
                    388
                ],
                "selected_choices": [
                    {
                        "id": 148,
                        "text": "Neck"
                    },
                    {
                        "id": 149,
                        "text": "Right Shoulder"
                    },
                    {
                        "id": 150,
                        "text": "Left Shoulder"
                    },
                    {
                        "id": 151,
                        "text": "Right Elbow"
                    },
                    {
                        "id": 152,
                        "text": "Left Elbow"
                    },
                    {
                        "id": 153,
                        "text": "Right Wrist"
                    },
                    {
                        "id": 154,
                        "text": "Left Wrist"
                    },
                    {
                        "id": 155,
                        "text": "Lower Back"
                    },
                    {
                        "id": 156,
                        "text": "Right Knee"
                    },
                    {
                        "id": 157,
                        "text": "Left Knee"
                    },
                    {
                        "id": 158,
                        "text": "Right Foot & Ankle"
                    },
                    {
                        "id": 159,
                        "text": "Left Foot & Ankle"
                    },
                    {
                        "id": 160,
                        "text": "Right Hip"
                    },
                    {
                        "id": 161,
                        "text": "Left Hip"
                    }
                ]
            },
            {
                "answer_id": 119,
                "question_id": 119,
                "question_text": "What level of pain are you experiencing?",
                "text_answer": "No Pain",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 120,
                "question_id": 120,
                "question_text": "What prior therapeutic interventions have you tried?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    389,
                    390,
                    391,
                    392,
                    393,
                    394,
                    395,
                    396,
                    397,
                    398,
                    399,
                    400,
                    401,
                    402
                ],
                "selected_choices": [
                    {
                        "id": 60,
                        "text": "Rest"
                    },
                    {
                        "id": 61,
                        "text": "Exercise"
                    },
                    {
                        "id": 62,
                        "text": "PT"
                    },
                    {
                        "id": 63,
                        "text": "injections"
                    },
                    {
                        "id": 64,
                        "text": "anti-inflammatories"
                    },
                    {
                        "id": 65,
                        "text": "corticosteroids"
                    },
                    {
                        "id": 66,
                        "text": "NSAIDs"
                    },
                    {
                        "id": 67,
                        "text": "steroids"
                    },
                    {
                        "id": 68,
                        "text": "opioids"
                    },
                    {
                        "id": 69,
                        "text": "oxycodone"
                    },
                    {
                        "id": 70,
                        "text": "non-prescription medications"
                    },
                    {
                        "id": 71,
                        "text": "prescription medications"
                    },
                    {
                        "id": 72,
                        "text": "muscle relaxants"
                    },
                    {
                        "id": 73,
                        "text": "Other"
                    }
                ]
            },
            {
                "answer_id": 121,
                "question_id": 121,
                "question_text": "Other prior therapeutic intervention",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 122,
                "question_id": 122,
                "question_text": "Do you have difficulty attempting activities/movements with objects > 5lbs?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    403,
                    404,
                    405,
                    406,
                    407,
                    408
                ],
                "selected_choices": [
                    {
                        "id": 167,
                        "text": "None"
                    },
                    {
                        "id": 168,
                        "text": "Lifting"
                    },
                    {
                        "id": 169,
                        "text": "Pushing"
                    },
                    {
                        "id": 170,
                        "text": "Pulling"
                    },
                    {
                        "id": 171,
                        "text": "Bending"
                    },
                    {
                        "id": 172,
                        "text": "Rotating"
                    }
                ]
            },
            {
                "answer_id": 123,
                "question_id": 123,
                "question_text": "Date of accident",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": "1990-01-01",
                "selected_choice_ids": []
            },
            {
                "answer_id": 124,
                "question_id": 124,
                "question_text": "What activities/movements make the pain worse?",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 125,
                "question_id": 125,
                "question_text": "Have you had, or will have, surgery on the affected area?",
                "text_answer": "Yes (Surgical)",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 126,
                "question_id": 126,
                "question_text": "Date of surgery if applicable",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 127,
                "question_id": 127,
                "question_text": "Where is the pain located?",
                "text_answer": None,
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": [
                    409,
                    410,
                    411,
                    412,
                    413,
                    414,
                    415,
                    416
                ],
                "selected_choices": [
                    {
                        "id": 175,
                        "text": "Neck"
                    },
                    {
                        "id": 176,
                        "text": "Elbow"
                    },
                    {
                        "id": 177,
                        "text": "Leg"
                    },
                    {
                        "id": 178,
                        "text": "Foot/Ankle"
                    },
                    {
                        "id": 179,
                        "text": "Shoulder"
                    },
                    {
                        "id": 180,
                        "text": "Knee"
                    },
                    {
                        "id": 181,
                        "text": "Wrist"
                    },
                    {
                        "id": 182,
                        "text": "Back"
                    }
                ]
            },
            {
                "answer_id": 128,
                "question_id": 128,
                "question_text": "Orientation",
                "text_answer": "Left",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 129,
                "question_id": 129,
                "question_text": "Have you had, or will have, surgery on the affected area?",
                "text_answer": "Yes (Surgical)",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            },
            {
                "answer_id": 130,
                "question_id": 130,
                "question_text": "Date of surgery if applicable",
                "text_answer": "Test Entry",
                "number_answer": None,
                "boolean_answer": None,
                "date_answer": None,
                "selected_choice_ids": []
            }
        ]
    },
    "doctor": {
        "doctor": {
            "id": 1,
            "user": {
                "id": 3,
                "username": "doctor",
                "email": "wybubo@mailinator.com",
                "first_name": "Paloma",
                "last_name": "Mack",
                "profile": {
                    "role": "DOCTOR",
                    "organization_type": None,
                    "parent_organization": None
                }
            },
            "phone_number": "+1 (681) 561-4122",
            "email": "wybubo@mailinator.com",
            "address": "Nemo ex aut voluptat",
            "state": "TN",
            "postal_code": "64049",
            "npi": "Harum voluptatum des",
            "created_at": "2026-08-26T22:16:56.424949Z",
            "updated_at": "2026-08-26T22:18:44.216536Z"
        },
        "license": {
            "license_number": None,
            "state": None
        }
    },
    "prescription_items": [
        {
            "condition": {
                "id": 1,
                "condition_id": 1,
                "condition_name": "Pain condition request?",
                "condition_code": "pain_request",
                "requested": True
            },
            "primary_drug": {
                "id": 50,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1280,
                    "item_type": "medication",
                    "name": "Aspirin",
                    "generic_name": "Aspirin",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Tabs",
                    "usual_sig": "",
                    "quantity": "2",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 1
                }
            },
            "secondary_drugs": [
                {
                    "id": 1231,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1281,
                        "item_type": "medication",
                        "name": "(Pliaglis)Lidocaine 7%/Tetracaine 7% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams topically to affected area(s) up to 4 times daily. Peel off after.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f6f41fa6fa97604e77f0d1",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1232,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1282,
                        "item_type": "medication",
                        "name": "Acetaminophen",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "2 tablets Acetaminophen to affected area up to 4 times daily as needed for pain when not using patches",
                        "quantity": "3",
                        "refills": 0,
                        "duration": "5 days",
                        "description": "NDC: 0311-3512-03 | Unit: Tabs | Fax: 12 | Source ID: 61e6ec048567bfc3a89b4e48",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1233,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1283,
                        "item_type": "medication",
                        "name": "Atopaderm Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms into palm and apply to affected area(s) 3 times daily. Massage gently into skin until completely absorbed. If skin is broken, cover with appropriate dressing.",
                        "quantity": "300",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7e368a6fa97604e77f0d7",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1234,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1284,
                        "item_type": "medication",
                        "name": "CLOBETASOL 0.05% OINTMENT 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "APPLY A THIN LAYER (1-2 GRAMS) TO THE AFFECTED AREA(S) 3-4 TIMES DAILY. ( 1 DIME SIZE = 1 GRAM)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 52565-0039-60 | Unit: Grams | Source ID: 629a5338cccd1a393e040c98",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1235,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1285,
                        "item_type": "medication",
                        "name": "CLOBETASOL FOAM 0.05%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a cupful (2-4 gm) of foam to affected area(s) 2 times a day for swelling",
                        "quantity": "250",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 50742-0304-50 | Unit: Grams | Source ID: 629a529176fa474d4ce739a0",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1236,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1286,
                        "item_type": "medication",
                        "name": "Calcipotriene 0.005%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-4 grams to affected area twice daily. (1 dime size= 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 6271971c1fbbcc56ba48da79",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1237,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1287,
                        "item_type": "medication",
                        "name": "Calcipotriene 0.005% 69 gram topical foam aerosol",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Dispense a small amount of calcipotriene foam into the palm of your hand and apply a thin layer externally to the affected area and gently rub the foam into the affected area until it disappears into the skin. 3 to 4 times daily. For the scalp, apply calcipotriene foam to your scalp when your hair is dry. Part your hair and apply directly on the affected area. Wash hands with soap and water thoroughly after each application to avoid spreading to the eyes, face or other sensitive mucous membranes.",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 73352-886-60 | Unit: Grams | Source ID: 62029a0577e77dff84f73800",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1238,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1288,
                        "item_type": "medication",
                        "name": "Camphotrol (Camphor 4% and Menthol 10%) Gel",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Using the roll-on applicator massage a liberal amount of gel directly on the affected area, not more than 3 to 4 times daily. For adults and children above age 12 only.",
                        "quantity": "85",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 59088-448-07 | Unit: Grams | Source ID: 6202993277e77dff84f737ff",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1239,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1289,
                        "item_type": "medication",
                        "name": "Capsaicin 0.075% topical cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer to the affected area not more than 4 times daily. For first use, apply to small area to test for sensitivity or skin reaction. Gently massage into the skin until fully absorbed. Wash hands with soap and water thoroughly after each application to avoid spreading to the eyes or other sensitive mucous membranes",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 50488-1075-6 | Unit: Grams | Source ID: 61faece1b678ff31b54d5145",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1240,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1290,
                        "item_type": "medication",
                        "name": "Capsaicin patch 0.025%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Pads",
                        "usual_sig": "Apply 1 patch to the affected area of intact skin up to 3 times a day. Do not leave patch on for more than 8 hours at a time. For adults and children above the age of 18 only.",
                        "quantity": "20",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 69420-7025-1 | Unit: Pads | Source ID: 620299a1234a24fd441351b9",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1241,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1291,
                        "item_type": "medication",
                        "name": "Circatrix (Capsicum Oleoresin) 0.05% topical cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer to the affected area not more than 4 times daily. For first use, apply to small area to test for sensitivity or skin reaction. Gently massage into the skin until fully absorbed. Wash hands with soap and water thoroughly after each application to avoid spreading to the eyes or other sensitive mucous membranes",
                        "quantity": "57",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 59088-479-05 | Unit: Grams | Source ID: 61faec9ab678ff31b54d5144",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1242,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1292,
                        "item_type": "medication",
                        "name": "DESONIDE 0.05% CREAM 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2-3 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1280-03 | Unit: Grams | Source ID: 629a4ee1cccd1a393e040c95",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1243,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1293,
                        "item_type": "medication",
                        "name": "DESONIDE 0.05% GEL 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2-3 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 24470-0920-60 | Unit: Grams | Source ID: 629a4f81cccd1a393e040c96",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1244,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1294,
                        "item_type": "medication",
                        "name": "DESONIDE 0.05% LOTION 118 ML",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply a thin layer (1-2 gm) to affected area(s) 2 to 3 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "118ML",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-4079-08 | Unit: ml | Source ID: 629a4e231328fd88e4e879c3",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1245,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1295,
                        "item_type": "medication",
                        "name": "DermacinRX Lexitral Pharmap",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Packs",
                        "usual_sig": "Apply 40 drops (approx.2ml) to affected area up to 4 times a day.",
                        "quantity": "1 pack",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Packs | Source ID: 6227f9b78229341ac76f8196",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1246,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1296,
                        "item_type": "medication",
                        "name": "Dermalid",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Packs",
                        "usual_sig": "Apply 2-3grams to affected area(s) up to 4 times daily as need for pain",
                        "quantity": "1 Kit",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Packs | Source ID: 6227f14e49ef0cd8cee991d0",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1247,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1297,
                        "item_type": "medication",
                        "name": "Desoximetasone 0.05% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) 3-4 times daily (1 gram = dime size)",
                        "quantity": "360",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7ec4b47efb4e1132cd9f0",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1248,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1298,
                        "item_type": "medication",
                        "name": "Desoximetasone 0.05% OINT",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Sig: apply a thin layer (1-2gm) to affected area(s) 3-4 times daily for swelling (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1352-03 | Unit: Grams | Source ID: 629a501176fa474d4ce7399b",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1249,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1299,
                        "item_type": "medication",
                        "name": "Diclofenac 1.5% Topical Solution",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply 2-4mL topically to affected area up to 4 times daily for pain.",
                        "quantity": "480",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: ml | Source ID: 61f6f4ad47efb4e1132cd9e4",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1250,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1300,
                        "item_type": "medication",
                        "name": "Diclofenac 2%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "2 pumps(40mg) to affected area twice daily for pain",
                        "quantity": "112",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 66e3057a6559f7b10b4e49d1",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1251,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1301,
                        "item_type": "medication",
                        "name": "Diclofenac 3% Gel",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams to affected area(s) 3-4 times daily. 1 gram=1 dime size",
                        "quantity": "200",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: (WMC) 000 | Unit: Grams | Source ID: 634d70d03b84c3401bf237a9",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1252,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1302,
                        "item_type": "medication",
                        "name": "Diclofenac 3% Topica lGel",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-4 grams to affected area(s)up to 4 times as needed for pain.",
                        "quantity": "300",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227fa0a7b18c08a9addd754",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1253,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1303,
                        "item_type": "medication",
                        "name": "Diclofenac 3% Topical Gel",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams to affected area(s) up to 4 times as needed for pain.",
                        "quantity": "300",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 (300g) | Unit: Grams | Source ID: 6220ce0949ef0cd8cee9919b",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1254,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1304,
                        "item_type": "medication",
                        "name": "Diclofenac Epolamine 1.3% Patch",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Pads",
                        "usual_sig": "Apply one patch twice a day to pain area",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Pads | Source ID: 61f6fa2747efb4e1132cd9e7",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1255,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1305,
                        "item_type": "medication",
                        "name": "Diclofenac Epolamine 1.3%Patch",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Pads",
                        "usual_sig": "Apply 1 patch to the most painful area twice daily",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Pads | Source ID: 6227f9da49ef0cd8cee991d7",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1256,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1306,
                        "item_type": "medication",
                        "name": "Diclofenac Epolamine Patch 1.3% 30 EA UD",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Pads",
                        "usual_sig": "Apply 1 patch to the most painful area twice a day.",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00093-3727-55 | Unit: Pads | Source ID: 6298ba7376fa474d4ce7397c",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1257,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1307,
                        "item_type": "medication",
                        "name": "Diclofenac Epolamine Patch 1.3% 30 EA UoU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Pads",
                        "usual_sig": "Apply 1 patch to the most painful area twice a day.",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 59762-0707-02 | Unit: Pads | Source ID: 6298bab21328fd88e4e8792b",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1258,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1308,
                        "item_type": "medication",
                        "name": "Diclofenac Sodium 1.5% Solution",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply 40 drops to the affected area 4 times daily as needed",
                        "quantity": "150",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: ml | Source ID: 636d232b800e4a3aa41e05a0",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1259,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1309,
                        "item_type": "medication",
                        "name": "Diclofenac Sodium 1.5% Topical Sol 150ml",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply 2.5ml's to affected area three times daily as needed (20 drops =1ml)",
                        "quantity": "150ml",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: (WMC) 000 | Unit: ml | Source ID: 634d706bdada76f3db17c2bb",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1260,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1310,
                        "item_type": "medication",
                        "name": "Diclofenac Sodium 1.5% Topical Sol 300ml",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply 2.5 ml's to affected area four times daily as needed (20 drops=1ml)",
                        "quantity": "300ml",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: (WMC) 000 | Unit: ml | Source ID: 634d70a7dada76f3db17c2bc",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1261,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1311,
                        "item_type": "medication",
                        "name": "Diclofenac Sodium 3% Topical Gel",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams to affected area(s) up to 4 times as needed for pain. (1gram = 1 dime size)",
                        "quantity": "200",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 71085-0003-00 | Unit: Grams | Source ID: 61f6f48047efb4e1132cd9e3",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1262,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1312,
                        "item_type": "medication",
                        "name": "Diclona Gel",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams to affected area 3-4 times daily as needed for pain. 1 gram =1 dime size",
                        "quantity": "198",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 643033e6e6732b4a5237faac",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1263,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1313,
                        "item_type": "medication",
                        "name": "Diclovix",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Packs",
                        "usual_sig": "Apply 2.5ml of Diclofanac Solutions to the AA(s) 4 times daily as needed (20 drops = 1ml) & apply 1 patch up to twice daily as needed",
                        "quantity": "2",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 72275-0702-77 | Unit: Packs | Source ID: 61f6f55c47efb4e1132cd9e5",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1264,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1314,
                        "item_type": "medication",
                        "name": "Diflorasone 0.05% Ointment",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams to affected area twice daily. Do not exceed 50 grams in a week. Use 2weeks on / 1week off",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227f2d349ef0cd8cee991d5",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1265,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1315,
                        "item_type": "medication",
                        "name": "Diflorasone Diacetate Cream 0.05% 60 GM UoU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-3 gm (1 gm = dime size) to the affected area(s) 1-3 times a day.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1296-03 | Unit: Grams | Source ID: 6298bb0a76fa474d4ce7397d",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1266,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1316,
                        "item_type": "medication",
                        "name": "Diflorasone Ointment 0.05% QTY 240gm",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (1-2gm) ro affected area(s) 3-4 times a day for swelling (1-dime size = 1gm)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 71800-0009-60 | Unit: Grams | Source ID: 6298b9be1328fd88e4e8792a",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1267,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1317,
                        "item_type": "medication",
                        "name": "Doxepin 5% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-3 grams to affected area twice daily. Do not exceed 60 grams in a week",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227f1e249ef0cd8cee991d2",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1268,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1318,
                        "item_type": "medication",
                        "name": "Eucrisa 2%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer of EUCRISA twice daily to affected areas. (dime size = 1 gram)",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 55724-0211-21 | Unit: Grams | Source ID: 61f6f815a6fa97604e77f0d3",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1269,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1319,
                        "item_type": "medication",
                        "name": "FLUOCINOLONE ACETONIDE TOPICAL SOL USP SOL 0.0001 60ML",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply a thin layer (1-2 gm) to affected area(s) 3 to 4 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "240 ML",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 21922-0003-01 | Unit: ml | Source ID: 629a4e7b1328fd88e4e879c4",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1270,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1320,
                        "item_type": "medication",
                        "name": "FLUOCINONIDE E CREAM USP 0.05% 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4gm) to affected area(s) 1 to 2 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00713-0664-60 | Unit: Grams | Source ID: 6298dfd81328fd88e4e87965",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1271,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1321,
                        "item_type": "medication",
                        "name": "FLURANDRENOLIDE 0.05% LOT 120GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2 to 3 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-5298-08 | Unit: Grams | Source ID: 629a51b476fa474d4ce7399e",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1272,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1322,
                        "item_type": "medication",
                        "name": "FLURANDRENOLIDE 0.05% LOT 120ML",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2 to 3 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "240 ML",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 24470-0921-12 | Unit: ml | Source ID: 629a51e476fa474d4ce7399f",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1273,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1323,
                        "item_type": "medication",
                        "name": "FLURANDRENOLIDE OINTMENT 0.05% 60G TUBE",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2 to 3 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 52565-0017-60 | Unit: Grams | Source ID: 629a524dcccd1a393e040c97",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1274,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1324,
                        "item_type": "medication",
                        "name": "Fluovix 0.1% Therapy Pack",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Packs",
                        "usual_sig": "Apply 2-3grams to affected area(s) 1-2times daily",
                        "quantity": "1",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Packs | Source ID: 6227f28549ef0cd8cee991d4",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1275,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1325,
                        "item_type": "medication",
                        "name": "Flurandrenolide 0.05% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2 to 3 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 24470-0919-12 | Unit: Grams | Source ID: 629810da76fa474d4ce73972",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1276,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1326,
                        "item_type": "medication",
                        "name": "Flurandrenolide 0.05% Lotion",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "mls",
                        "usual_sig": "Apply 2-3 ml to affected area(s) up to 3 times daily.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: mls | Source ID: 6227f9388229341ac76f8195",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1277,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1327,
                        "item_type": "medication",
                        "name": "Flurandrenolide 0.05% Ointment",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-4 grams to affected area(s) 3 times daily",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227f3017b18c08a9addd753",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1278,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1328,
                        "item_type": "medication",
                        "name": "HALOBETASOL PROPIONATE CREAM 0.05% 50GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4 gm) to affected area(s) 1 to 2 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "250",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 45802-0129-32 | Unit: Grams | Source ID: 629e0d8676fa474d4ce739d7",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1279,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1329,
                        "item_type": "medication",
                        "name": "HALOBETASOL PROPIONATE OINT 0.05% 50GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4 gm) to affected area(s) 1 to 2 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "250",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 52565-0073-51 | Unit: Grams | Source ID: 62981042cccd1a393e040bf0",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1280,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1330,
                        "item_type": "medication",
                        "name": "HYDROCORTISONE ACETATE-PRAMOXINE HCL 2.35-1% 28.4GM CREAM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer topically to the affected skin area(s) 3 to 4 times daily. (1 gram=dime size)",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f6f8b247efb4e1132cd9e6",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1281,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1331,
                        "item_type": "medication",
                        "name": "Halcinonide Cream 0.1% 60 GM UoU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-3 gm (1 gm = dime size) to the affected area(s) 2-3 times a day for swelling",
                        "quantity": "250",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00378-8056-60 | Unit: Grams | Source ID: 629a4fce1328fd88e4e879c5",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1282,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1332,
                        "item_type": "medication",
                        "name": "Hydrocortisone Butyrate Lotion 0.1%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml -- or -- 1000 mls",
                        "usual_sig": "Apply a thin layer (1-2 gm) to affected area(s) 2 times a day for swelling",
                        "quantity": "118ML",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 52565-0087-04 | Unit: ml -- or -- 1000 mls | Source ID: 6298108bcccd1a393e040bf1",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1283,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1333,
                        "item_type": "medication",
                        "name": "LIDOCAINE/PRILOCAINE 2.5%/2.5% 30GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2gm to affected area(s) 3-4 times daily for pain (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00115-1468-45 | Unit: Grams | Source ID: 629a53aa76fa474d4ce739a1",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1284,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1334,
                        "item_type": "medication",
                        "name": "Lidocaine 3% Topical Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams to affected area(s) up to 4 times as needed for pain.",
                        "quantity": "340",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f6f5b6a6fa97604e77f0d2",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1285,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1335,
                        "item_type": "medication",
                        "name": "Lidocaine 4% Solution",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply 2-4 ml to affected area(s) 3 times daily",
                        "quantity": "250",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: ml | Source ID: 6227f2598229341ac76f8194",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1286,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1336,
                        "item_type": "medication",
                        "name": "Lidocaine 5% Ointment",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams to affected area(s) 3-4 times daily . 1 gram = 1 dime size",
                        "quantity": "150",
                        "refills": 0,
                        "duration": "14 days",
                        "description": "NDC: 64380-789-33 | Unit: Grams | Source ID: 634d70ed3b84c3401bf237aa",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1287,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1337,
                        "item_type": "medication",
                        "name": "Lidocaine 5% Patch",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Pads",
                        "usual_sig": "Apply 1-2 patches topically to affected area(s).12 hours on and12 hours off",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Pads | Source ID: 6227f20d7b18c08a9addd752",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1288,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1338,
                        "item_type": "medication",
                        "name": "Lidocaine 5% Topical Ointment",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2gm to affected area(s) up to 3 times daily for pain (1 dime size = 1 gram)",
                        "quantity": "150",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 52565-0008-14 | Unit: Grams | Source ID: 629a53d81328fd88e4e879c7",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1289,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1339,
                        "item_type": "medication",
                        "name": "Lidocaine Ointment USP, 5%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams to affected area(s) up to 3 times daily as need for pain (1 dime size = 1 gram)",
                        "quantity": "150",
                        "refills": 0,
                        "duration": "25 days",
                        "description": "NDC: 64380-789-33 | Unit: Grams | Source ID: 6227f23549ef0cd8cee991d3",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1290,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1340,
                        "item_type": "medication",
                        "name": "Lidocaine/Prilocaine 2.5/2.5%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2 grams to affected area 3-4 times daily",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61fc32551f7b33b73b1b7c36",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1291,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1341,
                        "item_type": "medication",
                        "name": "Lidocort 3-0.5% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) up to 3 times daily as needed for pain, when not using patches.(1 gram=dime size)",
                        "quantity": "270",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 59088-430-05 | Unit: Grams | Source ID: 61f6fb25a007ea6e2be20b6a",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1292,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1342,
                        "item_type": "medication",
                        "name": "Lidothol Gel Lidocaine 4.5% | Menthol 5%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-4g, up to 4x daily (max 8g in 24 hours)",
                        "quantity": "198",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 53225-1026-01 | Unit: Grams | Source ID: 636d22075a234cf5e7dfe3f2",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1293,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1343,
                        "item_type": "medication",
                        "name": "Lidothol Patch Lidocaine 4.5%/ Menthol 5%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Pads",
                        "usual_sig": "Apply 1-3 patches once daily. Keep patch(s) in place for up to 12 hours daily, followed by a 12-hour patch-free period per 24 hours",
                        "quantity": "30",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Pads | Source ID: 636d2178800e4a3aa41e059d",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1294,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1344,
                        "item_type": "medication",
                        "name": "Lidotral 3.88%Cream (Lidocaine)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams to affected area up to 3 times daily as needed, when not using patches",
                        "quantity": "255",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227f1887b18c08a9addd751",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1295,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1345,
                        "item_type": "medication",
                        "name": "Liquid phenol",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tubes",
                        "usual_sig": "Apply 2-3 grams Liquid phenol to affected area up to 4 times daily as needed for pain when not using patches",
                        "quantity": "2",
                        "refills": 0,
                        "duration": "5 days",
                        "description": "NDC: 17532-745-32 | Unit: Tubes | Source ID: 61e6ecd98567bfc3a89b4e4d",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1296,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1346,
                        "item_type": "medication",
                        "name": "Methyl Salic 25% topical cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply externally to the affected area 3 to 4 times daily. For first use, apply to small area to test for sensitivity or skin reaction. Gently massage into the skin until fully absorbed. Wash hands with soap and water thoroughly after each application to avoid spreading to the eyes or other sensitive mucous membranes",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 50488-1015-05 | Unit: Grams | Source ID: 61faecbbf682e19066959961",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1297,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1347,
                        "item_type": "medication",
                        "name": "NSAID",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "2 tablets NSAID to affected area up to 4 times daily as needed for pain when not using patches",
                        "quantity": "2",
                        "refills": 0,
                        "duration": "5 days",
                        "description": "NDC: 9678-5544-632 | Unit: Tabs | Source ID: 61e6ec508567bfc3a89b4e4a",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1298,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1348,
                        "item_type": "medication",
                        "name": "New pain drug 1",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "take 1 tab daily",
                        "quantity": "100",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 1245 | Unit: Tablets | Source ID: 61f0241b849c14cd6b140381",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1299,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1349,
                        "item_type": "medication",
                        "name": "New pain drug 1 (Client)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Pads",
                        "usual_sig": "Take 3 daily",
                        "quantity": "123",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 123 | Unit: Pads | Source ID: 61f046d88fa2aa26d904e508",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1300,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1350,
                        "item_type": "medication",
                        "name": "Panadol",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Apply 2-3 grams Panadol to affected area up to 4 times daily as needed for pain when not using patches",
                        "quantity": "2",
                        "refills": 0,
                        "duration": "5 days",
                        "description": "NDC: NDC | Unit: Tablets | Source ID: 61e6ec698567bfc3a89b4e4b",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1301,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1351,
                        "item_type": "medication",
                        "name": "TRIAMCINOLONE 0.147MG/G SPRAY 100grams",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "APPLY 1-2 SPRAYS TO AFFECTED AREA(S) 3-4 TIMES DAILY FOR SWELLING (1 SPRAY=1GM)",
                        "quantity": "200",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 64980-0429-01 | Unit: Grams | Source ID: 629a53741328fd88e4e879c6",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1302,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1352,
                        "item_type": "medication",
                        "name": "TRIAMCINOLONE ACETONIDE OINT 0.05% 430 GM UOU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4gm) to affected area(s) 2 to 4 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "430",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 21922-0024-11 | Unit: Grams | Source ID: 62981005cccd1a393e040bef",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1303,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1353,
                        "item_type": "medication",
                        "name": "Triamcinolone 0.05% Oint 430gm",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4gm) to affected area(s) 2 to 4 times a day for swelling (1 dime size = 1 gram)",
                        "quantity": "430",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 74157-0901-90 | Unit: Grams | Source ID: 6298b95acccd1a393e040bfb",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1304,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1354,
                        "item_type": "medication",
                        "name": "Triamcinolone Acetonide Spray 0.147mg/gm",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams topically to affected area(s) up to 4 times daily (2 second spray= 1gram)",
                        "quantity": "400",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227f97249ef0cd8cee991d6",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1305,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1355,
                        "item_type": "medication",
                        "name": "Zonalon 5% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply to the affected area topically 4 times daily, allowing at least 3 to 4 hours between applications, for up to 8 days (1gram = dime size)",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f6f936a6fa97604e77f0d4",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1306,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1356,
                        "item_type": "medication",
                        "name": "Zonalon 5%Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-3 grams to affected area twice daily. Do not exceed 60 grams in a week.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227f1b549ef0cd8cee991d1",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1307,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1357,
                        "item_type": "medication",
                        "name": "pain drug 1",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Pads",
                        "usual_sig": "Take 3 daily",
                        "quantity": "13221",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 123-00 Client | Unit: Pads | Source ID: 61f04785ef72b6a52ca7e627",
                        "active": True,
                        "category": 1
                    }
                },
                {
                    "id": 1308,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1358,
                        "item_type": "medication",
                        "name": "test drug",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "Take 1 tablet by mouth every 4 hours as needed for headaches.",
                        "quantity": "100",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tabs | Source ID: 6470ca9f928c11742fb58d59",
                        "active": True,
                        "category": 1
                    }
                }
            ]
        },
        {
            "condition": {
                "id": 2,
                "condition_id": 2,
                "condition_name": "Muscle relaxer condition request?",
                "condition_code": "muscle_relaxer",
                "requested": True
            },
            "primary_drug": {
                "id": 51,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1359,
                    "item_type": "medication",
                    "name": "ALT Cyclobenzaprine 7.5MG 100 tabs",
                    "generic_name": "ALT Cyclobenzaprine 7.5MG 100 tabs",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Tabs",
                    "usual_sig": "",
                    "quantity": "100",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 2
                }
            },
            "secondary_drugs": [
                {
                    "id": 1309,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1360,
                        "item_type": "medication",
                        "name": "Chlorzoxazone 250 mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth three or four times daily for muscle spasms.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 69499-0330-60 | Unit: Tablets | Source ID: 629a430c76fa474d4ce73996",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1310,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1361,
                        "item_type": "medication",
                        "name": "Chlorzoxazone 375 mg Tablet",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth 3-4 times daily as needed for muscle spasms.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f6fb8447efb4e1132cd9e8",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1311,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1362,
                        "item_type": "medication",
                        "name": "Chlorzoxazone 375mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take up to 2 tablet by mouth 3 times daily as needed for muscle spasms",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227ee3c8229341ac76f818e",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1312,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1363,
                        "item_type": "medication",
                        "name": "Chlorzoxazone 500 mg Tablet",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth every 6 hours as needed for pain/muscle spasms.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 73007-0013-03 | Unit: Tablets | Source ID: 61f6fd1947efb4e1132cd9eb",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1313,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1364,
                        "item_type": "medication",
                        "name": "Chlorzoxazone 500mgTablet",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth every 6-8 hours as needed",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227ed007b18c08a9addd748",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1314,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1365,
                        "item_type": "medication",
                        "name": "Chlorzoxazone 750mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth every 6 hours as needed for pain/muscle spasms.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f6fd55a007ea6e2be20b6c",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1315,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1366,
                        "item_type": "medication",
                        "name": "Chlorzoxazone Tablets 250 mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take1-2 tablets by mouth 3-4 times daily as needed for muscle spasms",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227ed3d8229341ac76f818d",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1316,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1367,
                        "item_type": "medication",
                        "name": "Cyclobenzaprine 7.5 mg Tablet - QTY 90 Tabs",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "Take I tablet by mouth up to 3 times daily as needed for muscle spasms",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 69420-1001-01 | Unit: Tabs | Source ID: 629a423476fa474d4ce73994",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1317,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1368,
                        "item_type": "medication",
                        "name": "Cyclobenzaprine 7.5mg Tablet",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth 3 times daily as needed for muscle spasms.",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f6fba847efb4e1132cd9e9",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1318,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1369,
                        "item_type": "medication",
                        "name": "Cyclobenzaprine 7.5mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth 2-3 times daily for muscle spasms",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227ed6d7b18c08a9addd749",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1319,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1370,
                        "item_type": "medication",
                        "name": "Cyclobenzaprine ER 15mg Capsule",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1 capsule by mouth once daily as needed for muscle spasms",
                        "quantity": "30",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: (WMC) 000 | Unit: Capsules | Source ID: 634d7136c6009cadfa4af6fc",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1320,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1371,
                        "item_type": "medication",
                        "name": "Cyclobenzaprine HCL 7.5mg Tabs",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "1 tablet by mouth three times daily as needed for muscle spasms",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: (WMC) 000 | Unit: Tablets | Source ID: 634d710bc6009cadfa4af6fb",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1321,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1372,
                        "item_type": "medication",
                        "name": "Diazepam",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tubes",
                        "usual_sig": "Apply 2-3 grams Diazepam to affected area up to 4 times daily as needed for pain when not using patches",
                        "quantity": "2",
                        "refills": 0,
                        "duration": "5 days",
                        "description": "NDC: 7263-382-21 | Unit: Tubes | Source ID: 61e6ecb58567bfc3a89b4e4c",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1322,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1373,
                        "item_type": "medication",
                        "name": "METHCARBAMOL 750MG TABLETS",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "TAKE 1 TABLET BY MOUTH 3 TIMES DAILY.",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 76385-0124-50 | Unit: Tabs | Source ID: 629a42dacccd1a393e040c8e",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1323,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1374,
                        "item_type": "medication",
                        "name": "Metaxalone 400mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 2 tablets by mouth every 3-4 as needed.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 62df1cc14da3274528f8b63d",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1324,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1375,
                        "item_type": "medication",
                        "name": "Metaxalone 800mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet every 6-8 hours as needed for pain",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227edd37b18c08a9addd74a",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1325,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1376,
                        "item_type": "medication",
                        "name": "Metaxalone 800mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth 3-4 times daily as needed for muscle spasms.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f6fbcca007ea6e2be20b6b",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1326,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1377,
                        "item_type": "medication",
                        "name": "Methocarbamol 750 mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth 3-4 times daily as needed for muscle spasms.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 70868-0901-90 | Unit: Tablets | Source ID: 61f6fce847efb4e1132cd9ea",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1327,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1378,
                        "item_type": "medication",
                        "name": "Methocarbamol Tabs 750mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1 capsule by mouth 3-4 times daily as needed for pain.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Capsules | Source ID: 6227ee5b8229341ac76f818f",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1328,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1379,
                        "item_type": "medication",
                        "name": "Naprosyn",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "25 MG/5ML Oral Suspension",
                        "quantity": "25 MG/5ML",
                        "refills": 0,
                        "duration": "",
                        "description": "NDC: 71511070116 | Unit: ml | Source ID: 62da335c4da3274528f8b62d",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1329,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1380,
                        "item_type": "medication",
                        "name": "Norgesic Forte Tablet",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "Take 1 tablet by mouth 3-4 times daily as needed for pain.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tabs | Source ID: 62278d7c49ef0cd8cee991c1",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1330,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1381,
                        "item_type": "medication",
                        "name": "Orphenadrine Citrate/Aspirin/Caffeine Tablets (50gm/770mg/60mg)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "Take 1 tablet by mouth 3-4 times daily as needed for pain",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tabs | Source ID: 62278dae8229341ac76f8174",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1331,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1382,
                        "item_type": "medication",
                        "name": "Ozobax Oral Solution",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Take 5-20ml (1-4teaspoons) by mouth up to 4 times daily as needed for muscle spasms",
                        "quantity": "946",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: ml | Source ID: 6227eda649ef0cd8cee991ca",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1332,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1383,
                        "item_type": "medication",
                        "name": "Tizanidine 4mg Capsules",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1 capsule by mouth up to 3-4 times daily.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Capsules | Source ID: 6227edfa7b18c08a9addd74b",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1333,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1384,
                        "item_type": "medication",
                        "name": "Tizanidine 4mg Tablet",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth max 3 times daily as needed for muscle spasms. Treatment can be repeated at 6 to 8 hour intervals",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f6fe5347efb4e1132cd9ec",
                        "active": True,
                        "category": 2
                    }
                },
                {
                    "id": 1334,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1385,
                        "item_type": "medication",
                        "name": "new muscle relaxer drug",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "take 1 tab daily",
                        "quantity": "100",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 134 | Unit: Tablets | Source ID: 61f0246b91e26694cfd7e40e",
                        "active": True,
                        "category": 2
                    }
                }
            ]
        },
        {
            "condition": {
                "id": 3,
                "condition_id": 3,
                "condition_name": "Dermatitis/Eczema/Psoriasis condition request?",
                "condition_code": "dermatitis_eczema_psoriasis",
                "requested": True
            },
            "primary_drug": {
                "id": 52,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1386,
                    "item_type": "medication",
                    "name": "AZELAIC ACID TOPICAL GEL 15% 50GM",
                    "generic_name": "AZELAIC ACID TOPICAL GEL 15% 50GM",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Grams",
                    "usual_sig": "",
                    "quantity": "250",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 3
                }
            },
            "secondary_drugs": [
                {
                    "id": 1335,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1387,
                        "item_type": "medication",
                        "name": "ADAPALENE-BENZ PER 0.1-2.5% PMP GEL",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) once daily (1 gram= dime size)",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 45802-0846-01 | Unit: Grams | Source ID: 61f7ebc7a6fa97604e77f0de",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1336,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1388,
                        "item_type": "medication",
                        "name": "AMCINONIDE 0.1% CREAM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) 2-3 times daily (1 gram= dime size)",
                        "quantity": "270",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7e5c8a007ea6e2be20b70",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1337,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1389,
                        "item_type": "medication",
                        "name": "AZELAIC ACID 15% GEL",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) twice daily (1 gram = Dime size)",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00781-7172-50 | Unit: Grams | Source ID: 61f7ec2547efb4e1132cd9ef",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1338,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1390,
                        "item_type": "medication",
                        "name": "Atopaderm Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams to affected area 3 times daily. Massage gently until completely absorbed. If skin is broken ,cover with appropriate dressing",
                        "quantity": "200",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 62278c838229341ac76f8173",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1339,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1391,
                        "item_type": "medication",
                        "name": "Augmented Betamethasone Lotion",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-4 grams topically to affected area(s) 3 times daily",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 622789ab8229341ac76f816e",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1340,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1392,
                        "item_type": "medication",
                        "name": "Bensal HP",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams to affected area(s)upto4timesdaily.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 62278c1049ef0cd8cee991bf",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1341,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1393,
                        "item_type": "medication",
                        "name": "CALCIP 0.005% BETAMETH DIPROPIONATE 0.064%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer to affected area(s) 1 time a day for skin condition",
                        "quantity": "100",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00781-7165-95 | Unit: Grams | Source ID: 6298dd8e1328fd88e4e87960",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1342,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1394,
                        "item_type": "medication",
                        "name": "CALCIP 0.005% BETAMETH DIPROPIONATE 0.064% 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer to affected area(s) 1 time a day for skin condition.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00781-7165-35 | Unit: Grams | Source ID: 6298df9dcccd1a393e040c40",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1343,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1395,
                        "item_type": "medication",
                        "name": "CALCIPOTRIENE 0.005% OINT 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4gm) to affected area(s) 1 to 2 times a day",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 68462-0310-65 | Unit: Grams | Source ID: 6297d75a76fa474d4ce7396e",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1344,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1396,
                        "item_type": "medication",
                        "name": "CALCIPOTRIENE FOAM 0.005% 60 GM UOU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4 gm) of foam to affected area(s) 2 times a day",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 73352-0886-60 | Unit: Grams | Source ID: 6297d7becccd1a393e040bed",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1345,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1397,
                        "item_type": "medication",
                        "name": "CLOBETASOL 0.05% OINTMENT 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "APPLY A THIN LAYER (1-2 GRAMS) TO THE AFFECTED AREA(S) 3-4 TIMES DAILY. ( 1 DIME SIZE = 1 GRAM)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 52565-0039-60 | Unit: Grams | Source ID: 629a4c361328fd88e4e879c2",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1346,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1398,
                        "item_type": "medication",
                        "name": "CLOCORTOLONE PIVALATE 0.1 % CRM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) 3 times daily (1 gram = dime size)",
                        "quantity": "270",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 66993-0947-48 | Unit: Grams | Source ID: 61f7eb77a007ea6e2be20b71",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1347,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1399,
                        "item_type": "medication",
                        "name": "CROTAN 10% LOTION 227ML",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Massage a thin layer gently into the affected area(s) 2-3 times daily to relieve itchy skin.",
                        "quantity": "237ML",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00682-0051-10 | Unit: ml | Source ID: 629a4c7476fa474d4ce7399a",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1348,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1400,
                        "item_type": "medication",
                        "name": "Calcipotriene 0.005%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-4 grams to affected area twice daily. (1 dime size= 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 62686b071fbbcc56ba48da0c",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1349,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1401,
                        "item_type": "medication",
                        "name": "Calcipotriene 0.005% Foam",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply thin layer of foam to the affected area(s) twice daily",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 622789f67b18c08a9addd73c",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1350,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1402,
                        "item_type": "medication",
                        "name": "Calcipotriene/Betamethasone 0.005%/0.064% Ointment",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-3 grams to affected area(s) up to 4 times daily. *Refill every other month.",
                        "quantity": "360",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 68462-0501-66 | Unit: Grams | Source ID: 61f7e3b8a6fa97604e77f0d9",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1351,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1403,
                        "item_type": "medication",
                        "name": "Calcipotriene/Betamethasone0.005%/0.064%Ointment",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply1-3gramstoaffectedarea(s)upto4timesdaily.",
                        "quantity": "300",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227896f7b18c08a9addd73b",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1352,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1404,
                        "item_type": "medication",
                        "name": "Chemical X",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Packs",
                        "usual_sig": "2 tablets Acetaminophen to affected area up to 4 times daily as needed for pain when not using patches",
                        "quantity": "2",
                        "refills": 0,
                        "duration": "5 days",
                        "description": "NDC: NDC | Unit: Packs | Source ID: 61f2ccf83664da89645f4bb1",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1353,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1405,
                        "item_type": "medication",
                        "name": "Clobetasol 0.05% Topical Spray",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2 to 3 grams (2 second spray = 1 gram) topically to affected area(s) 3-4 times daily *Refill every other month.",
                        "quantity": "375",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7e508a6fa97604e77f0da",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1354,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1406,
                        "item_type": "medication",
                        "name": "Crotan Lotion",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 3-4 grams to affected area(s) twice daily. Thoroughly massage lotion into affected area until completely absorbed.",
                        "quantity": "237",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 626882af9c8f06f0bbc9e38b",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1355,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1407,
                        "item_type": "medication",
                        "name": "DESONIDE 0.05% CREAM 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2-3 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1280-03 | Unit: Grams | Source ID: 629a4846cccd1a393e040c91",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1356,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1408,
                        "item_type": "medication",
                        "name": "DESONIDE 0.05% GEL 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2-3 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 24470-0920-60 | Unit: Grams | Source ID: 629a47b91328fd88e4e879bd",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1357,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1409,
                        "item_type": "medication",
                        "name": "DESONIDE 0.05% LOTION 118 ML",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml -- or -- 1000 mls",
                        "usual_sig": "Apply a thin layer (1-2 gm) to affected area(s) 2 to 3 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "118",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-4079-08 | Unit: ml -- or -- 1000 mls | Source ID: 6297d6a976fa474d4ce7396d",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1358,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1410,
                        "item_type": "medication",
                        "name": "DESONIDE 0.05% OINT 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2-3 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1281-03 | Unit: Grams | Source ID: 629a48a9cccd1a393e040c92",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1359,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1411,
                        "item_type": "medication",
                        "name": "Desonide 0.05% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-4 grams topically to affected area(s) 3 times daily",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 62278ae18229341ac76f816f",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1360,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1412,
                        "item_type": "medication",
                        "name": "Desoximetasone 0.05% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) 3-4 times daily (1 gram = dime size)",
                        "quantity": "360",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7ec89a6fa97604e77f0e0",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1361,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1413,
                        "item_type": "medication",
                        "name": "Desoximetasone 0.05% OINT",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Sig: apply a thin layer (1-2gm) to affected area(s) 3-4 times daily for skin condition (1 dime size = 1 gram)",
                        "quantity": "240gm",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1352-03 | Unit: Grams | Source ID: 6297d404cccd1a393e040bec",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1362,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1414,
                        "item_type": "medication",
                        "name": "Desoximetasone 0.05% Ointment",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-4 grams topically to affected area(s) 3 times daily",
                        "quantity": "300",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 62278b1349ef0cd8cee991bd",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1363,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1415,
                        "item_type": "medication",
                        "name": "Diflorasone Cream 0.05%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) 3-4 times daily",
                        "quantity": "360",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7e569a007ea6e2be20b6f",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1364,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1416,
                        "item_type": "medication",
                        "name": "Diflorasone Diacetate Cream 0.05% 60 GM UoU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-3 gm (1 gm = dime size) to the affected area(s) 1-3 times a day.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1296-03 | Unit: Grams | Source ID: 6298b8ab76fa474d4ce7397a",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1365,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1417,
                        "item_type": "medication",
                        "name": "Diflorasone Ointment 0.05%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams to affected area twice daily. Do not exceed 60 grams in a week. *Refill every other month.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7e531a6fa97604e77f0db",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1366,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1418,
                        "item_type": "medication",
                        "name": "Diflorasone Ointment 0.05% QTY 240gm",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (1-2gm) ro affected area(s) 3-4 times a day for skin condition (1-dime size = 1gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 71800-0009-60 | Unit: Grams | Source ID: 629a49d4cccd1a393e040c93",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1367,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1419,
                        "item_type": "medication",
                        "name": "Diflorasone0.05%Ointment",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-2 grams to affected area twice daily. Do not exceed 50 grams in a week. Use 2 weeks on / 1week off.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 62278a3d49ef0cd8cee991bc",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1368,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1420,
                        "item_type": "medication",
                        "name": "ENSTILAR",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2 to 3 grams (2 second spray = 1 gram) topically to affected area(s) once daily *Refill every other month.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 50222-0302-60 | Unit: Grams | Source ID: 61f7e71447efb4e1132cd9ed",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1369,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1421,
                        "item_type": "medication",
                        "name": "Entty Spray",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply 1mL topically to affected skin area(s), allow to dry. May repeat up to 4 times daily",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: ml | Source ID: 61f7ecb3a007ea6e2be20b72",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1370,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1422,
                        "item_type": "medication",
                        "name": "Eucrisa 2%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer of EUCRISA twice daily to affected areas. (dime size = 1 gram)",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "60 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 6238a1ddbf3f2d417136dc5f",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1371,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1423,
                        "item_type": "medication",
                        "name": "FLUOCINOLONE ACETONIDE TOPICAL SOL USP SOL 0.0001 60ML",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply a thin layer (1-2 gm) to affected area(s) 3 to 4 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 21922-0003-01 | Unit: ml | Source ID: 6298df2c1328fd88e4e87964",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1372,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1424,
                        "item_type": "medication",
                        "name": "FLURANDRENOLIDE CREAM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2 to 3 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 24470-0919-12 | Unit: Grams | Source ID: 629a4aa11328fd88e4e879bf",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1373,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1425,
                        "item_type": "medication",
                        "name": "FLURANDRENOLIDE OINTMENT 0.05% 60G TUBE",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-3 gm) to affected area(s) 2 to 3 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 52565-0017-60 | Unit: Grams | Source ID: 629a4b2b1328fd88e4e879c0",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1374,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1426,
                        "item_type": "medication",
                        "name": "Fluocinolone 0.01% Solution",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply 2-4 mls topically to affected area(s) 3 times daily",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: ml | Source ID: 62278b578229341ac76f8170",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1375,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1427,
                        "item_type": "medication",
                        "name": "Fluocinonide 0.05% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-4 grams to affected area twice daily. Do not exceed 60 grams in a week.",
                        "quantity": "360",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7ed1ea6fa97604e77f0e1",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1376,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1428,
                        "item_type": "medication",
                        "name": "Fluocinonide E Cream USP 0.05%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4gm) to affected area(s) 1 to 2 times a day for swelling",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00713-0664-60 | Unit: Grams | Source ID: 6298b81476fa474d4ce73979",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1377,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1429,
                        "item_type": "medication",
                        "name": "Flurandrenolide 0.05% Lotion",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply 2-3 ml to affected area(s) up to 3 times daily",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: ml | Source ID: 62278a7b7b18c08a9addd73d",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1378,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1430,
                        "item_type": "medication",
                        "name": "HALOBETASOL PROPIONATE OINT 0.05% 50GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4 gm) to affected area(s) 1 to 2 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "250",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 52565-0073-51 | Unit: Grams | Source ID: 629a4a2e76fa474d4ce73999",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1379,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1431,
                        "item_type": "medication",
                        "name": "HYDROCORTISONE BUTYRATE LOTION 0.1% 118 ML UOU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply a thin layer (1-2 gm) to affected area(s) 2 times a day for skin condition",
                        "quantity": "118ML",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 70512-0032-04 | Unit: ml | Source ID: 629a4b941328fd88e4e879c1",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1380,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1432,
                        "item_type": "medication",
                        "name": "Halcinonide Cream 0.1% 60 GM UoU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1-3 gm (1 gm = dime size) to the affected area(s) 2-3 times a day.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00378-8056-60 | Unit: Grams | Source ID: 6298b87bcccd1a393e040bfa",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1381,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1433,
                        "item_type": "medication",
                        "name": "Hydrocortisone Butyrate Cream 0.1% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) 2-3 times daily (1 gram= dime size)",
                        "quantity": "270",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7e4dba007ea6e2be20b6e",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1382,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1434,
                        "item_type": "medication",
                        "name": "Hylaguard Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams to affected area 4 times daily. Massage gently until completely absorbed. If skin is broken, cover with appropriate dressing",
                        "quantity": "450",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 62278cc97b18c08a9addd73f",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1383,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1435,
                        "item_type": "medication",
                        "name": "KamDoy Rx Skin Emulsion",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply a small amount (1ml) in sufficient quantity to cover the affected skin area to be protected and allow to dry 4 times daily",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: ml | Source ID: 62278bcc8229341ac76f8171",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1384,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1436,
                        "item_type": "medication",
                        "name": "Kamdoy skin Emulsion",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply 1mL (6sprays) topically to affected area(s). Allow to dry. May repeat up to 4 times daily.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: ml | Source ID: 61f7e34ca007ea6e2be20b6d",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1385,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1437,
                        "item_type": "medication",
                        "name": "New derm drug 1",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1 daily",
                        "quantity": "1200",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 554 | Unit: Capsules | Source ID: 61f0248b849c14cd6b140382",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1386,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1438,
                        "item_type": "medication",
                        "name": "PIMECROLIMUS CREAM 1% 30 g(ELIDEL)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4 gm) to affected area(s) 2 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 68682-0110-01 | Unit: Grams | Source ID: 6298dcf31328fd88e4e8795f",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1387,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1439,
                        "item_type": "medication",
                        "name": "PIMECROLIMUS CREAM 1% 60G (ELIDEL)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4 gm) to affected area(s) 2 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 68682-0111-02 | Unit: Grams | Source ID: 629a464e1328fd88e4e879bc",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1388,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1440,
                        "item_type": "medication",
                        "name": "Sorilux 0.005% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) twice daily (1 gram = Dime size)",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51862-0376-60 | Unit: Grams | Source ID: 61f7eb09a6fa97604e77f0dd",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1389,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1441,
                        "item_type": "medication",
                        "name": "Sorilux 0.005% foam",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Sig: Apply a thin layer (1-2 gm) to affected area(s) 2 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51862-0376-60 | Unit: Grams | Source ID: 6297d54776fa474d4ce7396c",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1390,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1442,
                        "item_type": "medication",
                        "name": "Synerderm Skin Emulsion",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply 1 ml to affected area(s) and allow to dry .May repeat up to 4 times daily.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: ml | Source ID: 62278c458229341ac76f8172",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1391,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1443,
                        "item_type": "medication",
                        "name": "TACROLIMUS 0.1%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) twice times daily (1 gram = dime size)",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 68462-0534-65 | Unit: Grams | Source ID: 61f7e8aa47efb4e1132cd9ee",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1392,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1444,
                        "item_type": "medication",
                        "name": "TAZAROTENE 0.1% CRM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) once daily (1 gram = dime size)",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 60758-0561-60 | Unit: Grams | Source ID: 61f7e7e8a6fa97604e77f0dc",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1393,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1445,
                        "item_type": "medication",
                        "name": "TRIAMCINOLONE 0.147MG/G SPRAY 100grams",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "APPLY 1-2 SPRAYS TO AFFECTED AREA(S) 3-4 TIMES DAILY FOR SKIN CONDITION. (1 SPRAY=1GM)",
                        "quantity": "200",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 64980-0429-01 | Unit: Grams | Source ID: 629a4bedcccd1a393e040c94",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1394,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1446,
                        "item_type": "medication",
                        "name": "Tacrolimus 0.03% Ointment",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Sig: Apply a thin layer (2-4 gm) to affected area(s) 2 times a day for skin condition (1 dime size = 1 gram)",
                        "quantity": "360",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 16729-0421-01 | Unit: Grams | Source ID: 6297d4ba1328fd88e4e87901",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1395,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1447,
                        "item_type": "medication",
                        "name": "Triamcinolone 0.05% Oint 430gm",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer (2-4gm) to affected area(s) 2 to 4 times a day for for skin condition (1 dime size = 1 gram)",
                        "quantity": "430",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 74157-0901-90 | Unit: Grams | Source ID: 629a494a1328fd88e4e879be",
                        "active": True,
                        "category": 3
                    }
                },
                {
                    "id": 1396,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1448,
                        "item_type": "medication",
                        "name": "Triamcinolone Acetonide Spray 0.147mg/gm",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams topically to affected area(s) up to 4 times daily (2second spray= 1gram)",
                        "quantity": "400",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 62278aaf7b18c08a9addd73e",
                        "active": True,
                        "category": 3
                    }
                }
            ]
        },
        {
            "condition": {
                "id": 5,
                "condition_id": 5,
                "condition_name": "Acid reflux condition request?",
                "condition_code": "acid_reflux",
                "requested": True
            },
            "primary_drug": {
                "id": 54,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1468,
                    "item_type": "medication",
                    "name": "Omeprazole and Sodium Bicarbonate Powder for Oral suspension 40mg/1680 mg -QTY: 30 packets",
                    "generic_name": "Omeprazole and Sodium Bicarbonate Powder for Oral suspension 40mg/1680 mg -QTY: 30 packets",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Packs",
                    "usual_sig": "",
                    "quantity": "30",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 5
                }
            },
            "secondary_drugs": [
                {
                    "id": 1415,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1469,
                        "item_type": "medication",
                        "name": "Omeprazole 20mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Caps",
                        "usual_sig": "Take 1-2 capsules daily",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Caps | Source ID: 61fc34de02f39a272f413d1f",
                        "active": True,
                        "category": 5
                    }
                },
                {
                    "id": 1416,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1470,
                        "item_type": "medication",
                        "name": "Omeprazole and Sodium Bicarbonate 40mg/1100mg -QTY:30 Capsules",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1 capsule by mouth daily",
                        "quantity": "30",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 27241-0032-03 | Unit: Capsules | Source ID: 6297d2d076fa474d4ce7396a",
                        "active": True,
                        "category": 5
                    }
                },
                {
                    "id": 1417,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1471,
                        "item_type": "medication",
                        "name": "Omeprazole/Sodium Bicarb 40mg / 1680mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Empty packet contents into a small cup containing 1-2 tablespoons of water. Stir well and drink immediately. Refill cup with water and drink.1 time daily",
                        "quantity": "30",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227f11249ef0cd8cee991cf",
                        "active": True,
                        "category": 5
                    }
                },
                {
                    "id": 1418,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1472,
                        "item_type": "medication",
                        "name": "Omeprazole/Sodium Bicarbonate 40mg-1680mg Packets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Packs",
                        "usual_sig": "Take 1 packet by mouth once daily on an empty stomach at least one hour before a meal. Empty packet contents into a small cup containing 1-2 tablespoons of water. Do not use other liquids or food. Stir well and drink immediately. Refill cup with water and drink.",
                        "quantity": "30",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Packs | Source ID: 61f7f032a007ea6e2be20b7c",
                        "active": True,
                        "category": 5
                    }
                }
            ]
        },
        {
            "condition": {
                "id": 6,
                "condition_id": 7,
                "condition_name": "Cough condition request?",
                "condition_code": "cough",
                "requested": True
            },
            "primary_drug": {
                "id": 55,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1473,
                    "item_type": "medication",
                    "name": "Benzonatate Capsules 150mg",
                    "generic_name": "Benzonatate Capsules 150mg",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Tablets",
                    "usual_sig": "",
                    "quantity": "90",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 7
                }
            },
            "secondary_drugs": [
                {
                    "id": 1419,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1474,
                        "item_type": "medication",
                        "name": "CLEMASTINE FUMARATE syrup (.5mg/5mL",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Take 10-20ml by mouth twice daily",
                        "quantity": "1200",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: ml | Source ID: 61f7f1cba6fa97604e77f0e8",
                        "active": True,
                        "category": 7
                    }
                },
                {
                    "id": 1420,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1475,
                        "item_type": "medication",
                        "name": "CLEMASTINE FUMARATE syrup (.67mg/5mL)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Take 10-20ml by mouth twice daily",
                        "quantity": "1200",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: ml | Source ID: 6285354ac601d48898b404b6",
                        "active": True,
                        "category": 7
                    }
                }
            ]
        },
        {
            "condition": {
                "id": 7,
                "condition_id": 8,
                "condition_name": "Allergy condition request?",
                "condition_code": "allergy",
                "requested": True
            },
            "primary_drug": {
                "id": 56,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1476,
                    "item_type": "medication",
                    "name": "Carbinoxamine Maleate 6 Mg",
                    "generic_name": "Carbinoxamine Maleate 6 Mg",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Tabs",
                    "usual_sig": "",
                    "quantity": "120",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 8
                }
            },
            "secondary_drugs": [
                {
                    "id": 1421,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1477,
                        "item_type": "medication",
                        "name": "CLEMASTINE FUMARATE syrup (.67mg/5mL)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Take 10-20ml by mouth twice daily",
                        "quantity": "1200",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: ml | Source ID: 6285326109cbfe84d20641e0",
                        "active": True,
                        "category": 8
                    }
                },
                {
                    "id": 1422,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1478,
                        "item_type": "medication",
                        "name": "Carbinoxamine Tablets 6mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth 3-4 times daily. Take on an empty stomach.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f7f08aa6fa97604e77f0e7",
                        "active": True,
                        "category": 8
                    }
                },
                {
                    "id": 1423,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1479,
                        "item_type": "medication",
                        "name": "Clemastine Fumarate Syrup",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Take 2 teaspoons full (10ml) orally every 12 hours",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: ml | Source ID: 6227fc758229341ac76f819b",
                        "active": True,
                        "category": 8
                    }
                },
                {
                    "id": 1424,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1480,
                        "item_type": "medication",
                        "name": "Dexchlorpheniramine Maleate Solution",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Take 2 to 3 teaspoons twice daily for allergies",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: ml | Source ID: 62278d0449ef0cd8cee991c0",
                        "active": True,
                        "category": 8
                    }
                }
            ]
        },
        {
            "condition": {
                "id": 8,
                "condition_id": 9,
                "condition_name": "Oral NSAIDs condition request?",
                "condition_code": "oral_nsaids",
                "requested": True
            },
            "primary_drug": {
                "id": 57,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1481,
                    "item_type": "medication",
                    "name": "Celecoxib 200mg Caps",
                    "generic_name": "Celecoxib 200mg Caps",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Capsules",
                    "usual_sig": "",
                    "quantity": "60",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 9
                }
            },
            "secondary_drugs": [
                {
                    "id": 1425,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1482,
                        "item_type": "medication",
                        "name": "ALT Cyclobenzaprine 7.5MG 100 tabs",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth up to 3 times daily as needed for muscle spasms.",
                        "quantity": "100",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00591-3330-01 | Unit: Tablets | Source ID: 6297cfc61328fd88e4e878fa",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1426,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1483,
                        "item_type": "medication",
                        "name": "ANother oal drug",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 2 daily",
                        "quantity": "20",
                        "refills": 0,
                        "duration": "20 days",
                        "description": "NDC: 123 | Unit: Tablets | Source ID: 61f3fbc3898ba1f39beafcc0",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1427,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1484,
                        "item_type": "medication",
                        "name": "Baclofen Oral Soln 5 MG/5ML 473 ML",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Take 5 ml there times a day as needed.",
                        "quantity": "473ml",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 69528-0301-16 | Unit: ml | Source ID: 6298b6bbcccd1a393e040bf9",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1428,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1485,
                        "item_type": "medication",
                        "name": "Chlorzoxazone 250 mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth three or four times daily for muscle spasms.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 69499-0330-60 | Unit: Tablets | Source ID: 6297d0fd1328fd88e4e878fd",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1429,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1486,
                        "item_type": "medication",
                        "name": "Cyclobenzaprine 7.5 mg Tablet - QTY 90 Tabs",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take I tablet by mouth up to 3 times daily as needed for muscle spasms.",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 69420-1001-01 | Unit: Tablets | Source ID: 6297cf75cccd1a393e040be9",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1430,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1487,
                        "item_type": "medication",
                        "name": "DICLOFENAC POTASSIUM 25MG TABLETS",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "Take 1-2 tablets by mouth three times a day with food for pain.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 74157-0007-60 | Unit: Tabs | Source ID: 629a45111328fd88e4e879bb",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1431,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1488,
                        "item_type": "medication",
                        "name": "DUEXIS 800-26.6 MG TABLET 90 TB",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "Take 1 tablet by mouth three times a day before a meal with a full glass of water for pain.",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 75987-0010-03 | Unit: Tabs | Source ID: 629a442c1328fd88e4e879b9",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1432,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1489,
                        "item_type": "medication",
                        "name": "Diclofenac 25mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet 4-5 times daily as needed for pain",
                        "quantity": "150",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227ee8049ef0cd8cee991cb",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1433,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1490,
                        "item_type": "medication",
                        "name": "Diclofenac Capsule 35mg (Zorvolex)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1 capsule orally up to 3 times daily as needed for pain",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Capsules | Source ID: 6227efe47b18c08a9addd74f",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1434,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1491,
                        "item_type": "medication",
                        "name": "Diclofenac Potassium 25mg Capsules",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1 capsule by mouth 4 times daily as needed for pain.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 74157-095-60 | Unit: Capsules | Source ID: 62cc833520ed3736e8aa8650",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1435,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1492,
                        "item_type": "medication",
                        "name": "Diclofenac Potassium Tablets 35mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1-2 Tablets by mouth every 6 hours as needed for pain.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 42211-204-29 | Unit: Tablets | Source ID: 61f7f36047efb4e1132cd9f8",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1436,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1493,
                        "item_type": "medication",
                        "name": "Diclofenac Potassium Tablets 50mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 Tablets by mouth every 6-8 hours as needed for pain.",
                        "quantity": "100",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f7f3a647efb4e1132cd9f9",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1437,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1494,
                        "item_type": "medication",
                        "name": "Fenoprofen 200mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 2 capsules by mouth 3 times daily as needed for pain.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Capsules | Source ID: 61f7f1fb47efb4e1132cd9f5",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1438,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1495,
                        "item_type": "medication",
                        "name": "Fenoprofen 200mg Capsules",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1-2 capsules by mouth every 6 hours as needed for pain",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227eea449ef0cd8cee991cc",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1439,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1496,
                        "item_type": "medication",
                        "name": "Fenoprofen 200mg capsule",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1-3 capsules by mouth 3-4 times daily for pain. Take with food.",
                        "quantity": "360",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 69336-0124-10 | Unit: Capsules | Source ID: 6297d1581328fd88e4e878fe",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1440,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1497,
                        "item_type": "medication",
                        "name": "Fenoprofen 400mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1 capsule by mouth 3-4 times daily as needed for pain.",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "15 days",
                        "description": "NDC: 000 | Unit: Capsules | Source ID: 61f7f210a6fa97604e77f0e9",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1441,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1498,
                        "item_type": "medication",
                        "name": "Fenoprofen 400mg Capsules",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1 capsule by mouth 3-4 times daily as needed for pain.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Capsules | Source ID: 6227ef6e8229341ac76f8191",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1442,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1499,
                        "item_type": "medication",
                        "name": "IBUPROFEN-FAMOTIDIN 800-26.6MG 90 TB",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "Take 1 tablet by mouth three times a day before a meal with a full glass of water for pain.",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 67877-0626-90 | Unit: Tabs | Source ID: 629a43e01328fd88e4e879b8",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1443,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1500,
                        "item_type": "medication",
                        "name": "Indomethacin 25mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "Take 1-2 tablets by mouth 2 to 3 times per day",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tabs | Source ID: 61f3fb741303497a68799a10",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1444,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1501,
                        "item_type": "medication",
                        "name": "Ketoprofen 25mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1-2 capsule by mouth every 6 hours as needed for pain.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Capsules | Source ID: 61f7f22747efb4e1132cd9f6",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1445,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1502,
                        "item_type": "medication",
                        "name": "Ketoprofen 25mg Capsules",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1-2 capsule by mouth every 6 hours as needed for pain.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Capsules | Source ID: 6227eec58229341ac76f8190",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1446,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1503,
                        "item_type": "medication",
                        "name": "Ketoprofen 25mg capsules (100ct)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1 to 2 capsules by mouth 3-4 times daily for pain. Take with food.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 69336-0127-10 | Unit: Capsules | Source ID: 6298b62776fa474d4ce73978",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1447,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1504,
                        "item_type": "medication",
                        "name": "Ketoprofen ER 200mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth daily as needed for pain.",
                        "quantity": "30",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f7f407a007ea6e2be20b7d",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1448,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1505,
                        "item_type": "medication",
                        "name": "LOFENA 25MG TABLETS",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1-2 tablets by mouth three times a day with food for pain.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 15370-0180-60 | Unit: Tablets | Source ID: 629a455f76fa474d4ce73998",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1449,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1506,
                        "item_type": "medication",
                        "name": "Lofena (Diclofenac Potassium) 25 mg tablet, film coated",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take one to two tablets by mouth three times daily, not to exceed three doses per day",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 15370-180-60 | Unit: Tablets | Source ID: 61faecfcb678ff31b54d5146",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1450,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1507,
                        "item_type": "medication",
                        "name": "Mefenamic Acid 250mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 2 cap twice daily with food",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "15 days",
                        "description": "NDC: 000 | Unit: Capsules | Source ID: 61f7f24147efb4e1132cd9f7",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1451,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1508,
                        "item_type": "medication",
                        "name": "Mefenamic Acid 250mg Capsule",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Two (2) capsules initially, then one (1) capsules every 6 hours. DNE 7 day therapy",
                        "quantity": "30",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Capsules | Source ID: 6227f05849ef0cd8cee991ce",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1452,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1509,
                        "item_type": "medication",
                        "name": "Meloxicam 5MG Capsule",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 2-3 capsules daily as needed for pain",
                        "quantity": "90",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Capsules | Source ID: 6227efb87b18c08a9addd74e",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1453,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1510,
                        "item_type": "medication",
                        "name": "Meloxicam 7.5mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1-2 tablets daily as needed for pain",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61fc357302f39a272f413d20",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1454,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1511,
                        "item_type": "medication",
                        "name": "Meloxicam Cap 5 MG 30 EA",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 1-2 capsule by mouth once daily",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 68180-0188-06 | Unit: Capsules | Source ID: 6298b65e1328fd88e4e87929",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1455,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1512,
                        "item_type": "medication",
                        "name": "NAPROXEN 125MG/5ML SUSPENSION 500ML",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml -- or -- 1000 mls",
                        "usual_sig": "Take 4 teaspoonful (20ml) two times a day with food for pain.",
                        "quantity": "1000",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 70954-0151-10 | Unit: ml -- or -- 1000 mls | Source ID: 629a44be76fa474d4ce73997",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1456,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1513,
                        "item_type": "medication",
                        "name": "NAPROXEN DR 500MG TAB 100CT",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth two times a day for pain. Take with food.",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 69784-0500-01 | Unit: Tablets | Source ID: 6297d19e76fa474d4ce73969",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1457,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1514,
                        "item_type": "medication",
                        "name": "NAPROXEN ESOMEPRAZOLE DR 375MG/20 MG 60 TB",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth two times a day before a meal with a full glass of water for pain.",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 55111-0289-60 | Unit: Tablets | Source ID: 6298dc0ecccd1a393e040c3e",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1458,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1515,
                        "item_type": "medication",
                        "name": "NAPROXEN ESOMEPRAZOLE DR 500MG/20 MG 60 TB",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth two times a day before a meal with a full glass of water for pain.",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 55111-0701-60 | Unit: Tablets | Source ID: 6298dc3f1328fd88e4e8795d",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1459,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1516,
                        "item_type": "medication",
                        "name": "NAPROXEN SODIUM TAB ER 24HR 375 MG (BASE EQUIV) 100",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 to 2 tablets by mouth two times a day for pain. Take with food.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 69420-1375-01 | Unit: Tablets | Source ID: 6298dc9c1328fd88e4e8795e",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1460,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1517,
                        "item_type": "medication",
                        "name": "Nabumetone500mgTablet",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1-2 tablets daily. Do not exceed 2000mg in 24 hours",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227f01a8229341ac76f8192",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1461,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1518,
                        "item_type": "medication",
                        "name": "Naproxen 125mg/5ml Suspension",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "mls",
                        "usual_sig": "Take 10-20ml's by mouth twice daily as needed for pain",
                        "quantity": "946mls",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: (WMC) 000 | Unit: mls | Source ID: 634d7161c6009cadfa4af6fd",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1462,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1519,
                        "item_type": "medication",
                        "name": "Naproxen CR 375mg Tablet",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "Take 2 tablets by mouth daily as needed for pain.",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Capsules | Source ID: 61f7f3e2a6fa97604e77f0ea",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1463,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1520,
                        "item_type": "medication",
                        "name": "Naproxen Sodium Controlled-Release Tablets 375mg Tablet - QTY 60 Tabs",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "Take two tablets by mouth once daily for pain. Take with food.",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 47781-0153-01 | Unit: Tabs | Source ID: 6297d07ccccd1a393e040bea",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1464,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1521,
                        "item_type": "medication",
                        "name": "Naproxen Suspension 125mg/5m",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "mls",
                        "usual_sig": "Take 10-20ml by mouth twice daily as needed for pain",
                        "quantity": "1000",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: mls | Source ID: 6227eef87b18c08a9addd74c",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1465,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1522,
                        "item_type": "medication",
                        "name": "Naproxen-Esomeprazole 375mg/20mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet twice daily",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227ef4549ef0cd8cee991cd",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1466,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1523,
                        "item_type": "medication",
                        "name": "Naproxen-Esomeprazole 500mg/20mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet twice daily",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "60 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227ef1f7b18c08a9addd74d",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1467,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1524,
                        "item_type": "medication",
                        "name": "Norgesic Forte",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1/2 to 1 tablet by mouth 3-4 times daily for pain.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 50991-0999-60 | Unit: Tablets | Source ID: 6297d0361328fd88e4e878fc",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1468,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1525,
                        "item_type": "medication",
                        "name": "Orphenadrine/ASA/Caffeine 50mg/770mg/60mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Take 1/2 to 1 tablet by mouth 3-4 times daily.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 74157-0999-60 | Unit: Grams | Source ID: 6298b5db76fa474d4ce73977",
                        "active": True,
                        "category": 9
                    }
                },
                {
                    "id": 1469,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1526,
                        "item_type": "medication",
                        "name": "orla nsaids",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tabs",
                        "usual_sig": "take 3 daily",
                        "quantity": "100",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tabs | Source ID: 61f0134f7546274e6ea7afdf",
                        "active": True,
                        "category": 9
                    }
                }
            ]
        },
        {
            "condition": {
                "id": 9,
                "condition_id": 10,
                "condition_name": "Topical anti-fungal condition request?",
                "condition_code": "topical_antifungal",
                "requested": True
            },
            "primary_drug": {
                "id": 58,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1527,
                    "item_type": "medication",
                    "name": "AnsDrug",
                    "generic_name": "AnsDrug",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Tablets",
                    "usual_sig": "",
                    "quantity": "12",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 10
                }
            },
            "secondary_drugs": [
                {
                    "id": 1470,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1528,
                        "item_type": "medication",
                        "name": "CICLOPIROX OLAMINE GEL 0.77% 100GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2 to 4 grams to and around the affected area(s) two times a day.",
                        "quantity": "300",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00574-2061-01 | Unit: Grams | Source ID: 629a3edb1328fd88e4e879b5",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1471,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1529,
                        "item_type": "medication",
                        "name": "Econazole 1%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Clean and dry the affected area(s).Apply thin layer(1-2grams) to affected area(s) twice daily",
                        "quantity": "255",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227fae18229341ac76f8199",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1472,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1530,
                        "item_type": "medication",
                        "name": "Econazole Nitrate Cream 1%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) 3 times daily.",
                        "quantity": "270",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00 | Unit: Grams | Source ID: 61f7f4fca6fa97604e77f0ee",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1473,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1531,
                        "item_type": "medication",
                        "name": "Ecoza (econazole nitrate) topical foam 1% 70gms",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) 3 times daily.",
                        "quantity": "270",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7f57e47efb4e1132cd9fb",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1474,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1532,
                        "item_type": "medication",
                        "name": "KETOCONAZOLE FOAM 2% 50 GM UOU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Hold container upright and dispense foam into the cap of the can. Scoop up foam with fingers and apply to the affected area(s) until the foam disappears. Administer two times daily.",
                        "quantity": "250",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00378-7007-50 | Unit: Grams | Source ID: 629a3e8e76fa474d4ce73993",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1475,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1533,
                        "item_type": "medication",
                        "name": "Ketoconazole 2% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams to affected area(s) up to 3 times daily",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227fa8849ef0cd8cee991d8",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1476,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1534,
                        "item_type": "medication",
                        "name": "Ketoconazole 2% Foam",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 3-4 grams of foam directly to affected area(s) and rub in up to 3 times daily",
                        "quantity": "300",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227fab68229341ac76f8198",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1477,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1535,
                        "item_type": "medication",
                        "name": "Ketoconazole 2% Form",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply foam directly onto affected area(s) and rub in 4 times daily.",
                        "quantity": "300",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7f4e7a6fa97604e77f0ed",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1478,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1536,
                        "item_type": "medication",
                        "name": "Ketoconazole Foam 2% 100 GM UoU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-4gm to the affected area(s) two times a day.",
                        "quantity": "300",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00378-7007-01 | Unit: Grams | Source ID: 6298b2f9cccd1a393e040bf7",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1479,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1537,
                        "item_type": "medication",
                        "name": "METRONIDAZOLE 0.75% CREAM 45GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2 to 4 grams to the affected area two times daily.",
                        "quantity": "225",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 66993-0960-45 | Unit: Grams | Source ID: 6298b24476fa474d4ce73973",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1480,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1538,
                        "item_type": "medication",
                        "name": "METRONIDAZOLE 1% GEL 55GM PUMP",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2 to 4 grams to the affected area two times daily.",
                        "quantity": "220",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-4215-09 | Unit: Grams | Source ID: 6298b27e76fa474d4ce73974",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1481,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1539,
                        "item_type": "medication",
                        "name": "METRONIDAZOLE GEL 1% 60 GM UOU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2 to 4 grams to the affected area two times daily.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-4164-03 | Unit: Grams | Source ID: 6298b002cccd1a393e040bf3",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1482,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1540,
                        "item_type": "medication",
                        "name": "METRONIDAZOLE TOPICAL GEL 1% 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2 to 4 grams to the affected area(s) two times daily.",
                        "quantity": "240",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 66993-0936-61 | Unit: Grams | Source ID: 629a3f2d1328fd88e4e879b6",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1483,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1541,
                        "item_type": "medication",
                        "name": "MUPIROCIN CREAM 2% 30GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2 to 3 grams to the affected area three times daily for bacterial infection.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1370-02 | Unit: Grams | Source ID: 6298b11dcccd1a393e040bf4",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1484,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1542,
                        "item_type": "medication",
                        "name": "NAFTIFINE HCL CREAM 1% 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer to and around the affected area once daily.",
                        "quantity": "180gm",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1368-03 | Unit: Grams | Source ID: 6297cb741328fd88e4e878f8",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1485,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1543,
                        "item_type": "medication",
                        "name": "NAFTIFINE HCL CREAM 2% 60GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply a thin layer to and around the affected area once daily.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1368-03 | Unit: Grams | Source ID: 6298b212cccd1a393e040bf5",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1486,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1544,
                        "item_type": "medication",
                        "name": "NEO-SYNALAR 0.5%-0.025% CREAM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tubes",
                        "usual_sig": "Apply a thin film (1 to 2 grams) to the affected area and gently rub in 2 to 4 times a day.",
                        "quantity": "240gm",
                        "refills": 0,
                        "duration": "",
                        "description": "NDC: 43538-0940-60 | Unit: Tubes | Source ID: 6297c87576fa474d4ce73963",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1487,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1545,
                        "item_type": "medication",
                        "name": "Naftafine 2% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 gms to affected area(s) 2 times daily (1 gram= dime size)",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7f5ab47efb4e1132cd9fc",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1488,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1546,
                        "item_type": "medication",
                        "name": "Naftifine HCL 2% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams to affected area(s) daily",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227fa337b18c08a9addd755",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1489,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1547,
                        "item_type": "medication",
                        "name": "Naftifine gel 1%",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams to affected area(s) twice daily",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227fb117b18c08a9addd756",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1490,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1548,
                        "item_type": "medication",
                        "name": "OXICONAZOLE 1% CREAM 30GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2 to 3 grams to the affected area three to four times daily.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1359-02 | Unit: Grams | Source ID: 629a3da11328fd88e4e879b3",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1491,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1549,
                        "item_type": "medication",
                        "name": "OXICONAZOLE 1% CREAM 90GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Appy 2 to 3 grams to the affected area three to four times daily",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1359-08 | Unit: Grams | Source ID: 629a3de276fa474d4ce73992",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1492,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1550,
                        "item_type": "medication",
                        "name": "Oxiconazole 1% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams to affected area(s) up to 3 times daily",
                        "quantity": "270",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Grams | Source ID: 6227fa5b8229341ac76f8197",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1493,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1551,
                        "item_type": "medication",
                        "name": "Oxiconazole Nitrate 1% CREAM 180 GM",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 1 to 2 gm to affected area(s) three to four times daily",
                        "quantity": "180gm",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 51672-1359-03 | Unit: Grams | Source ID: 6297caea76fa474d4ce73965",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1494,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1552,
                        "item_type": "medication",
                        "name": "Oxiconazole Nitrate 1% Cream",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Grams",
                        "usual_sig": "Apply 2-3 grams to affected area(s) twice daily.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Grams | Source ID: 61f7f4baa007ea6e2be20b7e",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1495,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1553,
                        "item_type": "medication",
                        "name": "TOBRAMYCIN NEBU SOLN 300 MG/5ML 5 ML X 56 UD",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "For each treatment empty 2 nebules (600mg) into soaking device and allow medication to fully dissolve in water. Place affected areas into water and soak for 10-15 minutes. Administer one time a day.",
                        "quantity": "280",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 65162-0914-46 | Unit: ml | Source ID: 6298b0d01328fd88e4e87927",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1496,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1554,
                        "item_type": "medication",
                        "name": "Tavaborole Soln 5% 10 ML UoU",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "Apply to affected toenails once daily.",
                        "quantity": "10",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 72763-0201-10 | Unit: ml | Source ID: 6298b39e76fa474d4ce73975",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1497,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1555,
                        "item_type": "medication",
                        "name": "Vancomycin 250mg Capsule",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Capsules",
                        "usual_sig": "FILL FOOT SOAKING DEVICE WITH WARM WATER THEN EMPTY THE CONTENTS OF 6 VANCOMYCIN CAPSULES INTO CONTAINER. PLACE AFFECTED AREAS INTO WATER AND SOAK FOR 10-15 MINUTES DAILY.",
                        "quantity": "180",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 62559-0391-20 | Unit: Capsules | Source ID: 6297ca1876fa474d4ce73964",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1498,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1556,
                        "item_type": "medication",
                        "name": "Voriconazole 200mg Vial QD #30 (Thirty)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Bottles",
                        "usual_sig": "For each treatment empty (1) 200 mg vial into soaking device and allow medication to fully dissolve in water. Place affected areas into water and soak for 10-15 minutes. Adminster one time per day.",
                        "quantity": "30",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 70436-0029-80 | Unit: Bottles | Source ID: 6297caa01328fd88e4e878f7",
                        "active": True,
                        "category": 10
                    }
                },
                {
                    "id": 1499,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1557,
                        "item_type": "medication",
                        "name": "Voriconazole 200mg x 1ml vial",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Bottles",
                        "usual_sig": "Empty 1 vial into footbath up to 2 times daily and soak for 10 minutes.",
                        "quantity": "60",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 00049-3190-28 | Unit: Bottles | Source ID: 61f7f492a6fa97604e77f0ec",
                        "active": True,
                        "category": 10
                    }
                }
            ]
        },
        {
            "condition": {
                "id": 10,
                "condition_id": 11,
                "condition_name": "Migraine and Headache condition request?",
                "condition_code": "migraine_headache",
                "requested": True
            },
            "primary_drug": {
                "id": 59,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1558,
                    "item_type": "medication",
                    "name": "Butalbital/Acetaminophen 50mg/300mg Tablets",
                    "generic_name": "Butalbital/Acetaminophen 50mg/300mg Tablets",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Tablets",
                    "usual_sig": "",
                    "quantity": "120",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 11
                }
            },
            "secondary_drugs": [
                {
                    "id": 1500,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1559,
                        "item_type": "medication",
                        "name": "Butalbital-Acetaminophen-Caffeine Soln 50-325-40 MG/15ML 473 ML",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "ml",
                        "usual_sig": "15 to 30 mL orally every 4 hours as needed not to exceed 90 mL per day",
                        "quantity": "473",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 70154-0111-16 | Unit: ml | Source ID: 6298b4e01328fd88e4e87928",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1501,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1560,
                        "item_type": "medication",
                        "name": "Butalbital/ASA/Caffeine 50mg/325mg/40mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth every 6 hours as needed.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 42543-0098-01 | Unit: Tablets | Source ID: 6297ce7bcccd1a393e040be8",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1502,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1561,
                        "item_type": "medication",
                        "name": "Dihydroergotamine 4mg/ml Solution",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Bottles",
                        "usual_sig": "Use one spray (0.5 mg) in each nostril. Fifteen minutes later, use an additional one spray (0.5 mg) in each nostril, for a total dosage of four sprays (2 mg).",
                        "quantity": "8",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 24201-0463-08 | Unit: Bottles | Source ID: 6297ce3c76fa474d4ce73968",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1503,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1562,
                        "item_type": "medication",
                        "name": "Dihydroergotamine Mesylate",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Packs",
                        "usual_sig": "1 spray in each nasal, repeat after 15 to 30mins for a total o f4 sprays. Do not exceed 6 sprays in 24 hours or 8 sprays per week",
                        "quantity": "1 Kit",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Packs | Source ID: 6227fb6b49ef0cd8cee991d9",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1504,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1563,
                        "item_type": "medication",
                        "name": "Eletriptan Hydrobromide 40mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "1 tablet at onset of headache repeat in 2 hours if needed. Do not exceed dosage of 2 tablets per 24 hours",
                        "quantity": "12",
                        "refills": 0,
                        "duration": "6 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 6a05ec59b1e1ae5eec9b2632",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1505,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1564,
                        "item_type": "medication",
                        "name": "Ergotamin Caffeine tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 2 tablet po at first side of attack; may take 1 tablet every 30 mins as needed. Do not exceed 6 tablets per attack or 10 tablets per week.",
                        "quantity": "30",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227fbc549ef0cd8cee991da",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1506,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1565,
                        "item_type": "medication",
                        "name": "Ergotamine/Caffeine 1/100mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 2 tablets at the first sign of headache, followed by 1 tablet every half hour until the headache is relieved. Do not take more than 6 tablets per headache.",
                        "quantity": "100",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 24470-0917-10 | Unit: Tablets | Source ID: 6297cee61328fd88e4e878f9",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1507,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1566,
                        "item_type": "medication",
                        "name": "Ergotamine/Caffeine Tablets 1 mg/100mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth every 4 hours as needed for headaches.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f7f796a007ea6e2be20b80",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1508,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1567,
                        "item_type": "medication",
                        "name": "NURTEC 75 MG TABLETS",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth every day hours as needed for headaches. Take 1 tablet by mouth every other day as needed for migraines",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f7f7b147efb4e1132cd9fd",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1509,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1568,
                        "item_type": "medication",
                        "name": "Naproxen/Sumatriptan 500mg/85mg Tablets",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet at onset of migraine; may repeat once after 2 hours. Do not exceed 2 tablets in 24 hours",
                        "quantity": "9",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: Medcillary(000) | Unit: Tablets | Source ID: 6227fc188229341ac76f819a",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1510,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1569,
                        "item_type": "medication",
                        "name": "Rizatriptan Benzoate 10mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "1 tablet at onset of headache repeat in 2 hours if needed. Do not exceed dosage of 3 tablets per 24 hours",
                        "quantity": "18",
                        "refills": 0,
                        "duration": "6 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 6a05ecca1d4a4a44bcace318",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1511,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1570,
                        "item_type": "medication",
                        "name": "Rizatriptan Benzoate 5mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth every 4 hours as needed for headaches.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f7f745a6fa97604e77f0ef",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1512,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1571,
                        "item_type": "medication",
                        "name": "Sumatriptan Succinate 50mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "1 tablet at onset of headache repeat in 2 hours if needed. Do not exceed dosage of 2 tablets per 24 hours",
                        "quantity": "27",
                        "refills": 0,
                        "duration": "13.5 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 6a05ee31bab3d202641de35f",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1513,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1572,
                        "item_type": "medication",
                        "name": "Sumatriptan Succinate/ Naproxen Sodium 85/500mg",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth every 4 hours as needed for headaches.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f7f76da6fa97604e77f0f0",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1514,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1573,
                        "item_type": "medication",
                        "name": "Sumatriptan-Naproxen Sodium Tab 85-500 MG 9 EA",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet when needed for migraine. Maximum of 2 tablets in a 24 hour period taken at least 2 hours apart.",
                        "quantity": "63",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 71800-0901-01 | Unit: Tablets | Source ID: 6298b49a76fa474d4ce73976",
                        "active": True,
                        "category": 11
                    }
                },
                {
                    "id": 1515,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1574,
                        "item_type": "medication",
                        "name": "UBRELVY 100MG TABLET",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Tablets",
                        "usual_sig": "Take 1 tablet by mouth every 4 hours as needed for headaches.",
                        "quantity": "120",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Tablets | Source ID: 61f7f7c7a007ea6e2be20b81",
                        "active": True,
                        "category": 11
                    }
                }
            ]
        },
        {
            "condition": {
                "id": 11,
                "condition_id": 12,
                "condition_name": "Acne condition request?",
                "condition_code": "acne",
                "requested": True
            },
            "primary_drug": {
                "id": 60,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1575,
                    "item_type": "medication",
                    "name": "Drug-2",
                    "generic_name": "Drug-2",
                    "ndc": "112120-1212-121212",
                    "strength": "12",
                    "dosage_form": "gel",
                    "usual_sig": "",
                    "quantity": "120",
                    "refills": 12,
                    "duration": "12",
                    "description": "",
                    "active": True,
                    "category": 12
                }
            },
            "secondary_drugs": []
        },
        {
            "condition": {
                "id": 15,
                "condition_id": 16,
                "condition_name": "Laser Therapy Pain treatment request?",
                "condition_code": "laser_therapy_pain",
                "requested": True
            },
            "primary_drug": {
                "id": 61,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1576,
                    "item_type": "medication",
                    "name": "PainAway (Shoulder/Neck/Elbow)",
                    "generic_name": "PainAway (Shoulder/Neck/Elbow)",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Units",
                    "usual_sig": "",
                    "quantity": "1",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 16
                }
            },
            "secondary_drugs": [
                {
                    "id": 1516,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1577,
                        "item_type": "medication",
                        "name": "OnLux Laser Therapy",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Units",
                        "usual_sig": "15 min. per day. Daily for 90 days, then as needed",
                        "quantity": "1",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Units | Source ID: 65411ce1d9eb8ce1707cf4f9",
                        "active": True,
                        "category": 16
                    }
                },
                {
                    "id": 1517,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1578,
                        "item_type": "medication",
                        "name": "Onlux",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Units",
                        "usual_sig": "Lumber (Lower back) , Knee (right and/or left Knee) Wrist (right and/or left wrist) Ankle (right and/or left ankle)",
                        "quantity": "1",
                        "refills": 0,
                        "duration": "1 days",
                        "description": "NDC: LMN | Unit: Units | Source ID: 66b99e8afe3d52e028933847",
                        "active": True,
                        "category": 16
                    }
                },
                {
                    "id": 1518,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1579,
                        "item_type": "medication",
                        "name": "PainAway",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Units",
                        "usual_sig": "At home daily treatment: 5-mintues/treatment, every 4-hours, 60-days (Follow-up in 30-days with patient to monitor their reduction in pain and inflammation",
                        "quantity": "1",
                        "refills": 0,
                        "duration": "1 days",
                        "description": "NDC: LMN | Unit: Units | Source ID: 647dea772087af6495dd8333",
                        "active": True,
                        "category": 16
                    }
                },
                {
                    "id": 1519,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1580,
                        "item_type": "medication",
                        "name": "Triad 3LT (Back/Knee/Wrist/Ankle)",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Units",
                        "usual_sig": "10-minutes per Treatment (Every 2-4 Hours): 8 - weeks",
                        "quantity": "1",
                        "refills": 0,
                        "duration": "30 days",
                        "description": "NDC: 000 | Unit: Units | Source ID: 647f3ccd6d0fe055a02cfecd",
                        "active": True,
                        "category": 16
                    }
                },
                {
                    "id": 1520,
                    "prescription": {
                        "id": 1,
                        "created_at": "2026-08-26T23:05:07.151849Z",
                        "updated_at": "2026-08-26T23:05:07.151942Z",
                        "patient": 1,
                        "doctor": None,
                        "script": None
                    },
                    "drug": {
                        "id": 1581,
                        "item_type": "medication",
                        "name": "Triad 3TL LMN",
                        "generic_name": "",
                        "ndc": None,
                        "strength": "",
                        "dosage_form": "Units",
                        "usual_sig": "Lumber (Lower back) , Knee (right and/or left Knee) Wrist (right and/or left wrist) Ankle (right and/or left ankle)",
                        "quantity": "1",
                        "refills": 0,
                        "duration": "1 days",
                        "description": "NDC: LMN | Unit: Units | Source ID: 647dea542087af6495dd8332",
                        "active": True,
                        "category": 16
                    }
                }
            ]
        },
        {
            "condition": {
                "id": 16,
                "condition_id": 17,
                "condition_name": "Cold Compression Therapy request?",
                "condition_code": "cold_compression",
                "requested": True
            },
            "primary_drug": {
                "id": 62,
                "prescription": {
                    "id": 1,
                    "created_at": "2026-08-26T23:05:07.151849Z",
                    "updated_at": "2026-08-26T23:05:07.151942Z",
                    "patient": 1,
                    "doctor": None,
                    "script": None
                },
                "drug": {
                    "id": 1582,
                    "item_type": "medication",
                    "name": "ARS Gel pack cold & compression CCT",
                    "generic_name": "ARS Gel pack cold & compression CCT",
                    "ndc": "",
                    "strength": "",
                    "dosage_form": "Packs",
                    "usual_sig": "",
                    "quantity": "1",
                    "refills": 12,
                    "duration": "",
                    "description": "",
                    "active": True,
                    "category": 17
                }
            },
            "secondary_drugs": []
        }
    ]
}





def draw_page_header(canvas, doc):
    """Callback function to draw the header on every page."""
    canvas.saveState()
    
    # Configure font and color
    canvas.setFont("Helvetica", 10)
    canvas.setFillColorRGB(0.3, 0.3, 0.3)  # Charcoal color
    logo_path = "./prescription/pdfbuilder/logo.jpg" 
    image_width = 120
    image_height = 36
    # Draw header text (Right-aligned or left-aligned)
    header_text = "From : 561-892-4617"
    header_date = "Date : " + datetime.today().strftime("%m/%d/%Y")
    canvas.drawImage(logo_path, 54, 730, 
                     width=image_width, height=image_height, 
                     mask='auto')
    # canvas.drawString(54 + image_width + 10, doc.height + doc.bottomMargin + 15, header_text)
    canvas.drawRightString(doc.width + doc.leftMargin, doc.height + doc.bottomMargin + 15, header_date)
    canvas.drawRightString(doc.width + doc.leftMargin, doc.height + doc.bottomMargin + 3, header_text)
    
    # Draw a thin horizontal rule below the header text
    canvas.setStrokeColorRGB(0.7, 0.7, 0.7)
    canvas.setLineWidth(0.5)
    canvas.line(
        doc.leftMargin, 
        doc.height + doc.bottomMargin, 
        doc.width + doc.leftMargin, 
        doc.height + doc.bottomMargin
    )
    
    canvas.restoreState()




def get_patient_info_table(intake_data):    # Simple, compact style for form labels and values
    patient_info = intake_data.get('patient_info')
    col_widths = [144, 90, 100, 60, 110]
    styles = getSampleStyleSheet()
    style_text = ParagraphStyle(
        'FormText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13
    )

    # 3. Define raw table grid data 
    # Use Paragraphs to style text fragments (like bold labels)
    data = [
        # Row 0
        [
            Paragraph("<b>Patient Name:</b> " + patient_info.get('first_name', '') + " " + patient_info.get('last_name', ''), style_text), "", "", 
            Paragraph("<b>DOB:</b> " + patient_info.get('dob', ''), style_text), ""
        ],
        # Row 1
        [
            Paragraph("<b>Address:</b> " + patient_info.get('address', ''), style_text), "", 
            Paragraph("<b>City:</b> " + patient_info.get('city', ''), style_text), 
            Paragraph("<b>State:</b> " + patient_info.get('state', ''), style_text), 
        ],
        # Row 2
        [
            Paragraph("<b>Patient Phone:</b> " + patient_info.get('phone_number', ''), style_text), "", "", 
            Paragraph("<b>Zip:</b> " + patient_info.get('zip', ''), style_text)
        ],
       
   
    ]

    # 4. Map cell structural merges and borders
    t_style = TableStyle([
        # Row 0: Merge Patient Name (cols 0-2), Merge DOB (cols 3-4)
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (3, 0), (4, 0)),
        
        # Row 1: Merge Address (cols 0-1)
        ('SPAN', (0, 1), (1, 1)),
        
        # Row 2: Merge Phone (cols 0-2), Merge Diagnosis (cols 3-4)
        ('SPAN', (0, 2), (2, 2)),
        ('SPAN', (3, 2), (4, 2)),
        
        # Row 3: Merge Allergies across all columns
        ('SPAN', (0, 3), (4, 3)),
        
        # Row 4: Merge Payer (cols 0-2), Merge Claim Num (cols 3-4)
        ('SPAN', (0, 4), (2, 4)),
        ('SPAN', (3, 4), (4, 4)),
        
        # Row 5: Merge Adjuster Name (cols 0-2), Merge Adjuster Num (cols 3-4)
        ('SPAN', (0, 5), (2, 5)),
        ('SPAN', (3, 5), (4, 5)),
        
        # Layout Alignment Rules
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        
        # Horizontal lines matching the original form image
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.black), # Darker thick top line
    ])

    # 5. Build and generate document
    table = Table(data, colWidths=col_widths, style=t_style)

    return table


def grey_divider():
    return HRFlowable(
        width="100%",
        thickness=0.5,
        color="#D3D3D3",
        spaceBefore=8,
        spaceAfter=8
    )

def generate_insurance_table(insurance_data):
    """
    Accepts a dictionary of insurance data and returns a styled ReportLab Table.
    """
    # 1. Total printable form width is 504 points (612 page width - 108 margins)
    # Define a versatile 4-column base grid (126 points each)
    col_widths = [126, 126, 126, 126]
    
    # 2. Typography Styles
    styles = getSampleStyleSheet()
    style_text = ParagraphStyle(
        'FormText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13
    )

    # Clean helper to parse None values safely
    def clean(val):
        return str(val) if val is not None else ""

    ins_type = insurance_data.get("insurance_type")
    
    # 3. Handle layouts conditionally based on type
    if ins_type == "RX":
        title = "RX INSURANCE INFORMATION"
        data = [
            # Row 0: Carrier & Phone
            [Paragraph(f"<b>Insurance Carrier:</b> {clean(insurance_data.get('insurance_carrier'))}", style_text), "",
             Paragraph(f"<b>Carrier Phone:</b> {clean(insurance_data.get('carrier_phone'))}", style_text), ""],
            # Row 1: Group ID & Patient ID
            [Paragraph(f"<b>Group ID:</b> {clean(insurance_data.get('group_id'))}", style_text), "",
             Paragraph(f"<b>Patient ID (RX):</b> {clean(insurance_data.get('patient_id_rx'))}", style_text), ""],
            # Row 2: BIN & PCN
            [Paragraph(f"<b>BIN:</b> {clean(insurance_data.get('bin'))}", style_text), "",
             Paragraph(f"<b>PCN:</b> {clean(insurance_data.get('pcn'))}", style_text), ""]
        ]
        # Merge columns (0 to 1) and columns (2 to 3) for all three rows
        span_rules = [
            ('SPAN', (0, 0), (1, 0)), ('SPAN', (2, 0), (3, 0)),
            ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)),
            ('SPAN', (0, 2), (1, 2)), ('SPAN', (2, 2), (3, 2)),
        ]

    elif ins_type == "PIP":
        title = "PIP INSURANCE INFORMATION"
        data = [
            # Row 0: Carrier & Phone
            [Paragraph(f"<b>Insurance Carrier:</b> {clean(insurance_data.get('insurance_carrier'))}", style_text), "",
             Paragraph(f"<b>Carrier Phone:</b> {clean(insurance_data.get('carrier_phone'))}", style_text), ""],
            # Row 1: Policy Num & Claim Num
            [Paragraph(f"<b>Policy Number:</b> {clean(insurance_data.get('policy_number'))}", style_text), "",
             Paragraph(f"<b>Claim Number:</b> {clean(insurance_data.get('claim_number'))}", style_text), ""],
            # Row 2: Adjuster Info & Accident Date
            [Paragraph(f"<b>Adjuster:</b> {clean(insurance_data.get('adjuster_name'))} ({clean(insurance_data.get('adjuster_phone'))})", style_text), "", "",
             Paragraph(f"<b>Date of Accident:</b> {clean(insurance_data.get('date_of_accident'))}", style_text)]
        ]
        span_rules = [
            ('SPAN', (0, 0), (1, 0)), ('SPAN', (2, 0), (3, 0)),
            ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)),
            ('SPAN', (0, 2), (2, 2)),  # Give more horizontal space to Adjuster Name/Phone
        ]

    elif ins_type == "WC":
        title = "WORKMEN'S COMPENSATION INFORMATION"
        data = [
            # Row 0: Payer & Carrier Phone
            [Paragraph(f"<b>Payer Name:</b> {clean(insurance_data.get('payer_name'))}", style_text), "",
             Paragraph(f"<b>Carrier Phone:</b> {clean(insurance_data.get('carrier_phone'))}", style_text), ""],
            # Row 1: Employer & Claim Num
            [Paragraph(f"<b>Employer Name:</b> {clean(insurance_data.get('employer_name'))}", style_text), "",
             Paragraph(f"<b>Claim Number:</b> {clean(insurance_data.get('claim_number'))}", style_text), ""],
            # Row 2: Adjuster & Injury Date
            [Paragraph(f"<b>Adjuster:</b> {clean(insurance_data.get('adjuster_name'))} ({clean(insurance_data.get('adjuster_phone'))})", style_text), "", "",
             Paragraph(f"<b>Date of Injury:</b> {clean(insurance_data.get('date_of_injury'))}", style_text)]
        ]
        span_rules = [
            ('SPAN', (0, 0), (1, 0)), ('SPAN', (2, 0), (3, 0)),
            ('SPAN', (0, 1), (1, 1)), ('SPAN', (2, 1), (3, 1)),
            ('SPAN', (0, 2), (2, 2)),
        ]
    else:
        # Fallback if an unknown insurance type is passed
        return None

    # 4. Prefix a Title header row at index 0 for all layouts
    data.insert(0, [Paragraph(f"<b>{title}</b>", style_text), "", "", ""])
    
    # Shift coordinate row pointers down by 1 to accommodate our injected title row
    adjusted_spans = [('SPAN', (0, 0), (3, 0))]
    for rule, start, end in span_rules:
        adjusted_spans.append((rule, (start[0], start[1] + 1), (end[0], end[1] + 1)))

    # 5. Compile global layout styles
    base_style = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        # Subtle horizontal dividing grid lines
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        # Bold line setting off the section block title row
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.black),
    ]
    base_style.extend(adjusted_spans)

    # 6. Generate final table instance
    return Table(data, colWidths=col_widths, style=TableStyle(base_style))

def get_docs_signature_png(signature_file_name=None):
    if signature_file_name:
        relative = signature_file_name.removeprefix(settings.MEDIA_URL)  # '/media/' -> ''
        file_path = os.path.join(settings.MEDIA_ROOT, relative)
    else:
        file_path = None

    if not file_path or not os.path.isfile(file_path):
        file_path = os.path.join(os.path.dirname(__file__), "doc.png")  # fallback
    signature = Image(file_path, width=120, height=36)
    signature._restrictSize(120, 36)
    return signature
    

def generate_doctors_info_for_medication(canvas, doctor_data):
    styles = getSampleStyleSheet()
    style_text = ParagraphStyle(
        'DoctorFormText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13
    )

    def clean(val):
        return str(val) if val is not None else ""

    doctor = (doctor_data or {}).get('doctor', {})
    user = doctor.get('user', {})
    license_info = (doctor_data or {}).get('license', {})

    prescriber_name = " ".join(
        part for part in [user.get('first_name', ''), user.get('last_name', '')] if part
    )
    npi = clean(doctor.get('npi', ''))
    dea = clean(license_info.get('license_number') or 'Supervising Physician')
    phone = clean(doctor.get('phone_number', ''))
    address = clean(doctor.get('address', ''))
    city = clean(doctor.get('city', ''))
    state = clean(doctor.get('state', ''))
    postal_code = clean(doctor.get('postal_code', ''))

    signature = get_docs_signature_png(doctor.get('signature'))

    table_data = [
        [
            Paragraph(f"<b>Name/NPI:</b> {clean(prescriber_name)} / {npi}", style_text),
            "",
            Paragraph(f"<b>Phone:</b> {phone}", style_text),
            "",
        ],
        [
            Paragraph(f"<b>Address:</b> {address}", style_text),
            "",
            Paragraph(
                f"<b>City:</b> {city} <b>State:</b> {state} <b>Zip:</b> {postal_code}",
                style_text,
            ),
            "",
        ],
    ]

    table = Table(
        table_data,
        colWidths=[126, 126, 126, 126],
        style=TableStyle([
            ('SPAN', (0, 0), (1, 0)),
            ('SPAN', (2, 0), (3, 0)),
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (2, 1), (3, 1)),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.black),
        ]),
    )

    spacer = Paragraph("<br/>", style_text)
    return signature, spacer, table

def get_medications_footer_text():
    styles = getSampleStyleSheet()
    style_text = ParagraphStyle(
        'FooterText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10
    )

    authorization_text = """
                            I authorize the P.I.C. (Pharmacists in Charge) to substitute the prescribed product that I prescribed with one of the
                            alternative formulas or products I have prescribed if the patient does not have insurance, has a high deductible or
                            copay, or has an insurance policy that does not cover the particular product or compound I have prescribed. By
                            signing this prescription, I authorize the pharmacy to adjust the quantity written as needed based on patient's
                            insurance plan limitations.I understand that the purpose of this agreement is to provide each patient with an
                            affordable option within the same scope as the initially-prescribed medication.
                        """
    footer_text = """This document is NOT valid for any patient covered by Medicare (Parts A, B, C, or D,) or other federally funded payor plans."""

    para = [
        Paragraph(authorization_text, style_text),
        Paragraph(footer_text, style_text)
    ]

    return para

def generate_drug_table(drug, style_text, available_width=504):
    # Create a table for the drug information

    drug_data = [
        [
            Paragraph(f"<b>Drug Name:</b> {drug.get('name', '')}", style_text),
            "", "", "", "", "", "", "", "", "", "", "", "", "",
            Paragraph(f"<b>QTY:</b> {drug.get('quantity', '')}", style_text),
            "",
            "",
            Paragraph(f"<b>Refills:</b> {drug.get('refills', '')}", style_text),
            "",
            "",
        ],
        [
            Paragraph(f"<b>Dosage Form:</b> {drug.get('dosage_form', '')}", style_text),
            "", "", "", "", "",
            Paragraph(f"<b>Sig:</b> {drug.get('usual_sig', '')}", style_text),
            "", "", "", "", "", "", "", "", "", "", "", "", "",
        ],

    ]

    # Use a 20-column grid (5% each) so spans can represent exact percentages.
    col_widths = [available_width / 20.0] * 20

    drug_table = Table(
        drug_data,
        colWidths=col_widths,
        hAlign="LEFT",
        style=TableStyle([
            # Row 1: Drug Name 70%, QTY 15%, Refills 15%
            ('SPAN', (0, 0), (13, 0)),
            ('SPAN', (14, 0), (16, 0)),
            ('SPAN', (17, 0), (19, 0)),

            # Row 2: Dosage Form 30%, Sig 70%
            ('SPAN', (0, 1), (5, 1)),
            ('SPAN', (6, 1), (19, 1)),

            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),

            # ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            # ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.black),
        ]),
    )

    return drug_table

def generate_letter_of_medical_necessity(prescribeable_item_id, doctor_info=None, patient_info=None, condition_info=None, treatment_plan=None, available_width=504):
    """
    Generate a letter of medical necessity for a prescribeable item.
    
    Args:
        prescribeable_item_id: ID of the PrescribeAbleItem
        doctor_info: Dictionary containing doctor information (optional)
        patient_info: Dictionary containing patient information (optional)
        condition_info: Dictionary containing condition/questionnaire information (optional)
        treatment_plan: String containing the treatment plan (optional)
        available_width: Width available for the letter content
    
    Returns:
        List of Platypus flowable objects for the letter, or None if no letter found
    """
    try:
        letter = LetterOfMedicalNecessity.objects.filter(
            prescribeable_item_id=prescribeable_item_id,
            included_in_script=True
        ).first()
        
        if not letter:
            return None
        
        story = []
        style_sheet = getSampleStyleSheet()
        body_style = style_sheet['BodyText']
        heading_style = ParagraphStyle(
            'LetterHeading',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=colors.black,
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Add title if present
        if letter.title:
            story.append(Paragraph(letter.title, heading_style))
        
        # Add custom logo if uploaded
        if letter.custom_logo_upload:
            try:
                img = Image(letter.custom_logo_upload.path, width=150, height=75)
                story.append(img)
                story.append(Spacer(1, 0.2))
            except:
                pass  # Skip logo if it can't be loaded
        
        # Add doctor's information if flagged
        if letter.include_doctors_information and doctor_info:
            doctor_text = f"""
            <b>Physician Information:</b><br/>
            {doctor_info.get('name', '')}<br/>
            {doctor_info.get('specialty', '')}<br/>
            {doctor_info.get('contact', '')}<br/>
            """
            story.append(Paragraph(doctor_text, body_style))
            story.append(Spacer(1, 0.2))
        
        # Add condition questionnaire if flagged
        if letter.include_condition_questionnaire and condition_info:
            condition_text = f"""
            <b>Clinical Justification:</b><br/>
            {condition_info}
            """
            story.append(Paragraph(condition_text, body_style))
            story.append(Spacer(1, 0.2))
        
        # Add main letter content
        if letter.letter_content_html:
            story.append(Paragraph(letter.letter_content_html, body_style))
            story.append(Spacer(1, 0.2))
        
        # Add treatment plan if flagged
        if letter.include_treatment_plan and treatment_plan:
            treatment_text = f"""
            <b>Treatment Plan:</b><br/>
            {treatment_plan}
            """
            story.append(Paragraph(treatment_text, body_style))
            story.append(Spacer(1, 0.2))
        
        # Add description if present
        if letter.description:
            desc_text = f"<i>{letter.description}</i>"
            story.append(Paragraph(desc_text, body_style))
        
        return story if story else None
        
    except LetterOfMedicalNecessity.DoesNotExist:
        return None
    except Exception as e:
        print(f"Error generating letter of medical necessity: {str(e)}")
        return None

def generate_lmn_from_prescription_item(item):
    story = []
    if not isinstance(item, dict):
        return story

    try:
        item_drug = item.get("drug", item)
        lmn_id = item.get("letter_of_medical_necessity") or item_drug.get("letter_of_medical_necessity")
        if not lmn_id:
            return story

        lmn_obj = LetterOfMedicalNecessity.objects.select_related("prescribeable_item").filter(
            id=lmn_id,
            included_in_script=True
        ).first()
        if not lmn_obj:
            return story

        styles = getSampleStyleSheet()
        title_style = styles['Title']
        section_title_style = ParagraphStyle(
            'LMNSectionTitle',
            parent=styles['Heading4'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=13,
            spaceAfter=6,
            spaceBefore=8,
        )
        body_style = ParagraphStyle(
            'LMNBody',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=10,
            leading=13,
        )

        title_text = lmn_obj.title or f"Letter of Medical Necessity - {lmn_obj.prescribeable_item.name}"
        story.append(Paragraph(title_text, title_style))
        story.append(Paragraph(datetime.now().strftime("Date: %B %d, %Y"), body_style))
        story.append(Spacer(1, 12))

        if lmn_obj.custom_logo_upload:
            try:
                story.append(Image(lmn_obj.custom_logo_upload.path, width=140, height=70))
                story.append(Spacer(1, 8))
            except Exception:
                pass

        if lmn_obj.include_doctors_information:
            doctor_payload = item.get('doctor_info') or item.get('doctor') or {}
            story.append(Paragraph("Prescribing Physician", section_title_style))
            try:
                doctor_signature, doctor_spacer, doctor_table = generate_doctors_info_for_medication(None, doctor_payload)
                story.append(doctor_table)
                story.append(doctor_spacer)
                story.append(doctor_signature)
            except Exception:
                doctor = (doctor_payload or {}).get('doctor', {})
                user = doctor.get('user', {})
                provider_name = " ".join(
                    x for x in [user.get('first_name', ''), user.get('last_name', '')] if x
                ) or "N/A"
                story.append(Paragraph(f"<b>Name:</b> {provider_name}", body_style))
                story.append(Paragraph(f"<b>NPI:</b> {doctor.get('npi', '')}", body_style))
                story.append(Paragraph(f"<b>Phone:</b> {doctor.get('phone_number', '')}", body_style))
                story.append(Paragraph(f"<b>Address:</b> {doctor.get('address', '')}", body_style))
            story.append(Spacer(1, 10))

        patient_info = item.get('patient_info') or {}
        if patient_info:
            full_name = " ".join(
                x for x in [patient_info.get('first_name', ''), patient_info.get('last_name', '')] if x
            )
            story.append(Paragraph("Patient", section_title_style))
            story.append(Paragraph(f"<b>Name:</b> {full_name}", body_style))
            if patient_info.get('date_of_birth'):
                story.append(Paragraph(f"<b>DOB:</b> {patient_info.get('date_of_birth')}", body_style))
            story.append(Spacer(1, 8))

        story.append(Paragraph("Medical Necessity", section_title_style))
        condition_info = item.get('condition_info') or item.get('condition') or ""
        if lmn_obj.include_condition_questionnaire and condition_info:
            if isinstance(condition_info, dict):
                condition_name = condition_info.get('condition_name') or condition_info.get('name') or str(condition_info)
            else:
                condition_name = str(condition_info)
            story.append(Paragraph(f"<b>Condition/Clinical Context:</b> {condition_name}", body_style))
            story.append(Spacer(1, 6))

        if lmn_obj.letter_content_html:
            story.append(Paragraph(lmn_obj.letter_content_html, body_style))
            story.append(Spacer(1, 8))

        if lmn_obj.include_treatment_plan:
            treatment_plan = item.get('treatment_plan') or item_drug.get('usual_sig') or ""
            if treatment_plan:
                story.append(Paragraph("Treatment Plan", section_title_style))
                story.append(Paragraph(str(treatment_plan), body_style))
                story.append(Spacer(1, 8))

        if lmn_obj.description:
            story.append(Paragraph(f"<i>{lmn_obj.description}</i>", body_style))

        story.append(PageBreak())
        return story
    except Exception as e:
        print(f"Error generating LMN from prescription item: {str(e)}")
        return []


def generate_medications(data__, available_width=504):
    intake_data = data__.get('intake_info')
    # patient_info = intake_data.get('patient_info')
    insurance_info = intake_data.get('insurances')
    prescription_items = data__.get('prescription_items')
    
    story = []
    condition_style = ParagraphStyle(
    'WhiteBlack',
    fontName='Helvetica',    
    fontSize=12,
    textColor=colors.white,
    backColor=colors.black,
    leading=20,
    spaceBefore=0,
    spaceAfter=0,
    alignment=1  # Center alignment
)
    primary_drug_style = getSampleStyleSheet()['BodyText']
    available_width = 504
    secodary_drug_style = getSampleStyleSheet()['BodyText']
    lmn_medications = []
    lmn_story = []
    for conditions in prescription_items:
        condition = conditions.get('condition', {})
        condition_name = condition.get('condition_name', "")
        
        condition_name = condition_name.replace("?", "")
        primary_drug = conditions.get('primary_drug', {})
        secondary_drugs = conditions.get('secondary_drugs', [])
        if primary_drug.get('drug').get('show_in_script') == False:
            if primary_drug.get('drug').get('requires_letter_of_medical_necessity') == True:
                lmn_medications.append(primary_drug)
                continue
            
        # Generate the table for the current condition and its drugs
        condition_heading = Paragraph(f"<i><b>Condition:</b> {condition_name}</i>", condition_style)
        print("Primary_drug", primary_drug)


        doctor_section_signature, doctor_section_spacer, doctor_section_table = generate_doctors_info_for_medication(None, data__.get('doctor', {}))
        paragraphs = get_medications_footer_text()
        story.append(get_patient_info_table(intake_data))
        story.append(generate_insurance_table(insurance_info[0]))
        story.append(condition_heading)

        story.append(generate_drug_table(primary_drug.get('drug'), primary_drug_style, available_width))
        story.append(doctor_section_signature)
        story.append(doctor_section_spacer)
        story.append(doctor_section_table)
        story.append(Spacer(1, 12))  # Add some space between secondary drugs
        story.append(Paragraph("<b>Authorized Substitutes:</b>", condition_style))

        for secondary_drug in secondary_drugs:
            story.append(generate_drug_table(secondary_drug.get('drug'), secodary_drug_style, available_width))
            story.append(grey_divider())  # Add some space between secondary drugs
        story.append(PageBreak())
        
        # Generate and append letter of medical necessity for the primary drug
        primary_drug_data = primary_drug.get('drug', {})
        prescribeable_item_id = primary_drug_data.get('id') or primary_drug_data.get('prescribeable_item_id')
        for secondary_drug in secondary_drugs:
            story.append(get_patient_info_table(intake_data))
            story.append(generate_insurance_table(insurance_info[0]))
            story.append(condition_heading)
            story.append(generate_drug_table(secondary_drug.get('drug'), secodary_drug_style, available_width))
            story.append(grey_divider())  # Add some space between secondary drugs
            story.append(doctor_section_signature)
            story.append(doctor_section_spacer)
            story.append(doctor_section_table)
            story.append(PageBreak())
        if prescribeable_item_id:
            doctor_info = data__.get('doctor', {})
            patient_info = intake_data.get('patient_info', {})
            condition_text = condition.get('condition_name', '')
            
            letter_content = generate_letter_of_medical_necessity(
                prescribeable_item_id=prescribeable_item_id,
                doctor_info=doctor_info,
                patient_info=patient_info,
                condition_info=condition_text)
            
            if letter_content:
                lmn_story.append(Spacer(1, 12))
                lmn_story.extend(letter_content)
                lmn_story.append(Spacer(1, 12))
        
        story.append(doctor_section_signature)
        story.append(doctor_section_spacer)
        story.append(doctor_section_table)
        for paragraph in paragraphs:
            story.append(paragraph)
        story.append(PageBreak())


    # for drugs in lmn_medications:


    story.extend(lmn_story)
    return story

def build_soap_notes_section(soap_notes):
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'SoapNotesTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#173D4A'),
        spaceAfter=5
    )
    heading_style = ParagraphStyle(
        'SoapNotesSubheading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#176B70'),
        spaceBefore=9,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'SoapNotesBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#25343A'),
        spaceAfter=2
    )

    story = [
        Paragraph('SOAP NOTES', title_style),
        HRFlowable(width='100%', thickness=1, color=colors.HexColor('#176B70'),
                   spaceBefore=1, spaceAfter=7)
    ]
    for heading, key in (
        ('Subjective', 'subjective'),
        ('Objective', 'objective'),
        ('Assessment', 'assessment'),
        ('Plan', 'plan')
    ):
        value = soap_notes.get(key) or 'Not documented.'
        note_text = '<br/>'.join(escape(line) for line in str(value).splitlines())
        story.append(Paragraph(heading, heading_style))
        story.append(Paragraph(note_text, body_style))
    return story


def visit_summary_section(date_time_of_call):
    styles = getSampleStyleSheet()
    text = f"""
        Telephone consults<br/>
        Total time spent: 15 minutes, greater than half the time spent on
        counseling and/or coordination of care<br/><br/>

        Date and Time of call: {date_time_of_call}<br/><br/>

        Length of call (min): 15<br/><br/>

        Orders: EM pending coding (CPT-code 99202).
        Patient understands and agrees with care. Chart routed to physician.
    """

    heading_style = ParagraphStyle(
        'VisitSummaryHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=colors.HexColor('#173D4A'),
        spaceAfter=5
    )
    story = [Paragraph('Visit Summary', heading_style)]
    story.append(Paragraph(text, styles['Normal']))
    return story


def create_pdf(filename, prescription_instance, data__):
    # Establish document with safe margins for the header
    # prescription_instance = data__.get('prescription_instance')
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        leftMargin=54,  # 0.75 inch
        rightMargin=54,
        topMargin=70,   # Leave room so text doesn't overlap header
        bottomMargin=70
    )

    intake_data = data__.get('intake_info')
    patient_info = intake_data.get('patient_info')
    insurance_info = intake_data.get('insurances')
    prescription_items = data__.get('prescription_items')
    
    styles = getSampleStyleSheet()
    story = []
    
    # Medications Content
    intake_id = prescription_instance.patient.id
    story.extend( generate_medications(data__))

    soap_notes_instance = Soap_notes.objects.get(patient_intake=intake_id)
    story.extend(build_soap_notes_section({
        'subjective': soap_notes_instance.subjective,
        'objective': soap_notes_instance.objective,
        'assessment': soap_notes_instance.assessment,
        'plan': soap_notes_instance.plan
    }))

    story.append(PageBreak())
    story.extend(visit_summary_section(intake_data.get('patient_intake').get('updated_at', 'N/A')))
    # Page 2 Content

    # Bind the header callback to the build process
    doc.build(story, onFirstPage=draw_page_header, onLaterPages=draw_page_header)
    buffer.seek(0)

    # 8. STEP 2: Save the buffer content directly to your FileField
    # Django triggers 'prescription_upload_path', using the real ID from step 2
    prescription_instance.pdf_file.save(
        filename,
        ContentFile(buffer.read()), 
        save=True
    )
    
    # Clean up memory
    buffer.close()

