
# intake_data = {
#         "patient_info": {
#             "id": 1,
#             "first_name": "John",
#             "last_name": "Doe",
#             "date_of_birth": "1990-01-01",
#             "email": "test@example.com",
#             "phone_number": "1234567890",
#             "address": "Test Entry",
#             "state": "AL",
#             "created_at": "2026-08-26T22:45:47.229944Z",
#             "updated_at": "2026-08-26T22:45:47.230041Z"
#         },
#         "patient_intake": {
#             "id": 1,
#             "height": "1.00",
#             "weight": "1.00",
#             "status": "Assigned",
#             "created_at": "2026-08-26T22:45:47.386322Z",
#             "updated_at": "2026-08-26T22:48:23.303829Z",
#             "patient": 1,
#             "client": 4,
#             "intake_agent": 7,
#             "cordinator": 5,
#             "doctor": 1
#         },
#         "insurances": [
#             {
#                 "id": 1,
#                 "insurance_type": "RX",
#                 "primary_insured": True,
#                 "insurance_carrier": "Test Entry",
#                 "carrier_phone": "1234567890",
#                 "group_id": "123456789",
#                 "patient_id_rx": "123456789",
#                 "bin": "123456789",
#                 "pcn": "123456789",
#                 "adjuster_name": None,
#                 "adjuster_phone": None,
#                 "policy_number": None,
#                 "claim_number": None,
#                 "date_of_accident": None,
#                 "payer_name": None,
#                 "date_of_injury": None,
#                 "employer_name": None,
#                 "created_at": "2026-08-26T22:45:47.409559Z",
#                 "updated_at": "2026-08-26T22:45:47.409600Z",
#                 "patient": 1
#             }
#         ],
#         "family_history": [
#             {
#                 "id": 1,
#                 "asthama": "Yes",
#                 "bleeding_tendency": "Yes",
#                 "cancer": "Yes",
#                 "colitis": "Yes",
#                 "depression": "Yes",
#                 "diabetes": "Yes",
#                 "epilepsy": "Yes",
#                 "heart_attack": "Yes",
#                 "high_blood_pressure": "Yes",
#                 "kidney_disease": "Yes",
#                 "leukemia": "Yes",
#                 "migraine": "Yes",
#                 "schizophrenia": "Yes",
#                 "stomach_ulcers": "Yes",
#                 "stroke": "Yes",
#                 "suicide": "Yes",
#                 "tuberculosis": "Yes",
#                 "patient": 1
#             }
#         ],
#         "health_records": [
#             {
#                 "id": 1,
#                 "record_type": "Medical Conditions",
#                 "record_date": "1990-01-01",
#                 "description": "Test Entry",
#                 "created_at": "2026-08-26T22:45:47.422759Z",
#                 "updated_at": "2026-08-26T22:45:47.422796Z",
#                 "patient": 1
#             }
#         ],
#         "medical_history": [
#             {
#                 "id": 1,
#                 "condition": "Test Entry",
#                 "diagnosis_date": "1990-01-01",
#                 "notes": "Test Entry",
#                 "created_at": "2026-08-26T22:45:47.430334Z",
#                 "updated_at": "2026-08-26T22:45:47.430369Z",
#                 "patient": 1
#             }
#         ],
#         "requested_conditions": [
#             {
#                 "id": 1,
#                 "condition_id": 1,
#                 "condition_name": "Pain condition request?",
#                 "condition_code": "pain_request",
#                 "requested": True
#             },
#             {
#                 "id": 2,
#                 "condition_id": 2,
#                 "condition_name": "Muscle relaxer condition request?",
#                 "condition_code": "muscle_relaxer",
#                 "requested": True
#             },
#             {
#                 "id": 3,
#                 "condition_id": 3,
#                 "condition_name": "Dermatitis/Eczema/Psoriasis condition request?",
#                 "condition_code": "dermatitis_eczema_psoriasis",
#                 "requested": True
#             },
#             {
#                 "id": 4,
#                 "condition_id": 4,
#                 "condition_name": "Scar/wound/actinic keratosis condition request?",
#                 "condition_code": "scar_wound_actinic",
#                 "requested": True
#             },
#             {
#                 "id": 5,
#                 "condition_id": 5,
#                 "condition_name": "Acid reflux condition request?",
#                 "condition_code": "acid_reflux",
#                 "requested": True
#             },
#             {
#                 "id": 6,
#                 "condition_id": 7,
#                 "condition_name": "Cough condition request?",
#                 "condition_code": "cough",
#                 "requested": True
#             },
#             {
#                 "id": 7,
#                 "condition_id": 8,
#                 "condition_name": "Allergy condition request?",
#                 "condition_code": "allergy",
#                 "requested": True
#             },
#             {
#                 "id": 8,
#                 "condition_id": 9,
#                 "condition_name": "Oral NSAIDs condition request?",
#                 "condition_code": "oral_nsaids",
#                 "requested": True
#             },
#             {
#                 "id": 9,
#                 "condition_id": 10,
#                 "condition_name": "Topical anti-fungal condition request?",
#                 "condition_code": "topical_antifungal",
#                 "requested": True
#             },
#             {
#                 "id": 10,
#                 "condition_id": 11,
#                 "condition_name": "Migraine and Headache condition request?",
#                 "condition_code": "migraine_headache",
#                 "requested": True
#             },
#             {
#                 "id": 11,
#                 "condition_id": 12,
#                 "condition_name": "Acne condition request?",
#                 "condition_code": "acne",
#                 "requested": True
#             },
#             {
#                 "id": 12,
#                 "condition_id": 13,
#                 "condition_name": "Foot bath condition request?",
#                 "condition_code": "foot_bath",
#                 "requested": True
#             },
#             {
#                 "id": 13,
#                 "condition_id": 14,
#                 "condition_name": "Cold sores condition request?",
#                 "condition_code": "cold_sores",
#                 "requested": True
#             },
#             {
#                 "id": 14,
#                 "condition_id": 15,
#                 "condition_name": "Diabetes condition request?",
#                 "condition_code": "diabetes",
#                 "requested": True
#             },
#             {
#                 "id": 15,
#                 "condition_id": 16,
#                 "condition_name": "Laser Therapy Pain treatment request?",
#                 "condition_code": "laser_therapy_pain",
#                 "requested": True
#             },
#             {
#                 "id": 16,
#                 "condition_id": 17,
#                 "condition_name": "Cold Compression Therapy request?",
#                 "condition_code": "cold_compression",
#                 "requested": True
#             }
#         ],
#         "condition_answers": [
#             {
#                 "answer_id": 1,
#                 "question_id": 1,
#                 "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 2,
#                 "question_id": 2,
#                 "question_text": "Diagnosis",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 3,
#                 "question_id": 3,
#                 "question_text": "Have you tried other medications for this condition?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 4,
#                 "question_id": 4,
#                 "question_text": "Medications",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 5,
#                 "question_id": 5,
#                 "question_text": "Have you ever used Lidocaine for pain?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 6,
#                 "question_id": 6,
#                 "question_text": "For what pain",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 7,
#                 "question_id": 7,
#                 "question_text": "What type of pain are you experiencing?",
#                 "text_answer": "Aching",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 8,
#                 "question_id": 8,
#                 "question_text": "On a scale of 1 to 10, rate severity of your pain",
#                 "text_answer": "1",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 9,
#                 "question_id": 9,
#                 "question_text": "Where is the pain located?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     1,
#                     2,
#                     3,
#                     4,
#                     5,
#                     6,
#                     7,
#                     8,
#                     9,
#                     10,
#                     11,
#                     12,
#                     13,
#                     14,
#                     15,
#                     16,
#                     17,
#                     18,
#                     19,
#                     20,
#                     21,
#                     22,
#                     23,
#                     24,
#                     25,
#                     26,
#                     27,
#                     28,
#                     29,
#                     30,
#                     31
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 1,
#                         "text": "Face"
#                     },
#                     {
#                         "id": 2,
#                         "text": "Head"
#                     },
#                     {
#                         "id": 3,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 4,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 5,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 6,
#                         "text": "Right Arm"
#                     },
#                     {
#                         "id": 7,
#                         "text": "Left Arm"
#                     },
#                     {
#                         "id": 8,
#                         "text": "Right elbow"
#                     },
#                     {
#                         "id": 9,
#                         "text": "Left elbow"
#                     },
#                     {
#                         "id": 10,
#                         "text": "Right wrist"
#                     },
#                     {
#                         "id": 11,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 12,
#                         "text": "Right hand"
#                     },
#                     {
#                         "id": 13,
#                         "text": "Left hand"
#                     },
#                     {
#                         "id": 14,
#                         "text": "Right fingers"
#                     },
#                     {
#                         "id": 15,
#                         "text": "Left fingers"
#                     },
#                     {
#                         "id": 16,
#                         "text": "Upper back"
#                     },
#                     {
#                         "id": 17,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 18,
#                         "text": "Chest"
#                     },
#                     {
#                         "id": 19,
#                         "text": "Stomach"
#                     },
#                     {
#                         "id": 20,
#                         "text": "Right hip"
#                     },
#                     {
#                         "id": 21,
#                         "text": "Left Hip"
#                     },
#                     {
#                         "id": 22,
#                         "text": "Right thigh"
#                     },
#                     {
#                         "id": 23,
#                         "text": "Left thigh"
#                     },
#                     {
#                         "id": 24,
#                         "text": "Right knee"
#                     },
#                     {
#                         "id": 25,
#                         "text": "Left knee"
#                     },
#                     {
#                         "id": 26,
#                         "text": "Right Leg"
#                     },
#                     {
#                         "id": 27,
#                         "text": "Left Leg"
#                     },
#                     {
#                         "id": 28,
#                         "text": "Right foot & ankle"
#                     },
#                     {
#                         "id": 29,
#                         "text": "Left foot & ankle"
#                     },
#                     {
#                         "id": 30,
#                         "text": "Right toes"
#                     },
#                     {
#                         "id": 31,
#                         "text": "Left toes"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 10,
#                 "question_id": 10,
#                 "question_text": "How long have you had this problem (days, weeks, months etc.)?",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 11,
#                 "question_id": 11,
#                 "question_text": "How often do you experience the symptoms?",
#                 "text_answer": "Constantly",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 12,
#                 "question_id": 12,
#                 "question_text": "How are your symptoms changing with time?",
#                 "text_answer": "Getting worse",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 13,
#                 "question_id": 13,
#                 "question_text": "How do you think your problem began?",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 14,
#                 "question_id": 14,
#                 "question_text": "What activities make the pain worse?",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 15,
#                 "question_id": 15,
#                 "question_text": "What activities reduce the pain?",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 16,
#                 "question_id": 16,
#                 "question_text": "What prior therapeutic interventions have you tried?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     32,
#                     33,
#                     34,
#                     35,
#                     36,
#                     37,
#                     38,
#                     39,
#                     40,
#                     41,
#                     42,
#                     43,
#                     44,
#                     45
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 60,
#                         "text": "Rest"
#                     },
#                     {
#                         "id": 61,
#                         "text": "Exercise"
#                     },
#                     {
#                         "id": 62,
#                         "text": "PT"
#                     },
#                     {
#                         "id": 63,
#                         "text": "injections"
#                     },
#                     {
#                         "id": 64,
#                         "text": "anti-inflammatories"
#                     },
#                     {
#                         "id": 65,
#                         "text": "corticosteroids"
#                     },
#                     {
#                         "id": 66,
#                         "text": "NSAIDs"
#                     },
#                     {
#                         "id": 67,
#                         "text": "steroids"
#                     },
#                     {
#                         "id": 68,
#                         "text": "opioids"
#                     },
#                     {
#                         "id": 69,
#                         "text": "oxycodone"
#                     },
#                     {
#                         "id": 70,
#                         "text": "non-prescription medications"
#                     },
#                     {
#                         "id": 71,
#                         "text": "prescription medications"
#                     },
#                     {
#                         "id": 72,
#                         "text": "muscle relaxants"
#                     },
#                     {
#                         "id": 73,
#                         "text": "Other"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 17,
#                 "question_id": 17,
#                 "question_text": "Other prior therapeutic intervention",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 18,
#                 "question_id": 18,
#                 "question_text": "Which therapeutic interventions afforded improvement of symptoms?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     46,
#                     47,
#                     48,
#                     49,
#                     50,
#                     51,
#                     52,
#                     53,
#                     54,
#                     55,
#                     56,
#                     57,
#                     58,
#                     59
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 60,
#                         "text": "Rest"
#                     },
#                     {
#                         "id": 61,
#                         "text": "Exercise"
#                     },
#                     {
#                         "id": 62,
#                         "text": "PT"
#                     },
#                     {
#                         "id": 63,
#                         "text": "injections"
#                     },
#                     {
#                         "id": 64,
#                         "text": "anti-inflammatories"
#                     },
#                     {
#                         "id": 65,
#                         "text": "corticosteroids"
#                     },
#                     {
#                         "id": 66,
#                         "text": "NSAIDs"
#                     },
#                     {
#                         "id": 67,
#                         "text": "steroids"
#                     },
#                     {
#                         "id": 68,
#                         "text": "opioids"
#                     },
#                     {
#                         "id": 69,
#                         "text": "oxycodone"
#                     },
#                     {
#                         "id": 70,
#                         "text": "non-prescription medications"
#                     },
#                     {
#                         "id": 71,
#                         "text": "prescription medications"
#                     },
#                     {
#                         "id": 72,
#                         "text": "muscle relaxants"
#                     },
#                     {
#                         "id": 73,
#                         "text": "Other"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 19,
#                 "question_id": 19,
#                 "question_text": "Other intervention that afforded improvement",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 20,
#                 "question_id": 20,
#                 "question_text": "Do you have a history of seizures, heart arrhythmias, or pacemaker use?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 21,
#                 "question_id": 21,
#                 "question_text": "Do you have muscle spasms?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 22,
#                 "question_id": 22,
#                 "question_text": "Location of muscle spasms",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     60,
#                     61,
#                     62,
#                     63,
#                     64,
#                     65,
#                     66,
#                     67,
#                     68,
#                     69,
#                     70,
#                     71,
#                     72,
#                     73,
#                     74,
#                     75,
#                     76,
#                     77,
#                     78,
#                     79,
#                     80,
#                     81,
#                     82,
#                     83,
#                     84,
#                     85,
#                     86,
#                     87,
#                     88,
#                     89,
#                     90
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 1,
#                         "text": "Face"
#                     },
#                     {
#                         "id": 2,
#                         "text": "Head"
#                     },
#                     {
#                         "id": 3,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 4,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 5,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 6,
#                         "text": "Right Arm"
#                     },
#                     {
#                         "id": 7,
#                         "text": "Left Arm"
#                     },
#                     {
#                         "id": 8,
#                         "text": "Right elbow"
#                     },
#                     {
#                         "id": 9,
#                         "text": "Left elbow"
#                     },
#                     {
#                         "id": 10,
#                         "text": "Right wrist"
#                     },
#                     {
#                         "id": 11,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 12,
#                         "text": "Right hand"
#                     },
#                     {
#                         "id": 13,
#                         "text": "Left hand"
#                     },
#                     {
#                         "id": 14,
#                         "text": "Right fingers"
#                     },
#                     {
#                         "id": 15,
#                         "text": "Left fingers"
#                     },
#                     {
#                         "id": 16,
#                         "text": "Upper back"
#                     },
#                     {
#                         "id": 17,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 18,
#                         "text": "Chest"
#                     },
#                     {
#                         "id": 19,
#                         "text": "Stomach"
#                     },
#                     {
#                         "id": 20,
#                         "text": "Right hip"
#                     },
#                     {
#                         "id": 21,
#                         "text": "Left Hip"
#                     },
#                     {
#                         "id": 22,
#                         "text": "Right thigh"
#                     },
#                     {
#                         "id": 23,
#                         "text": "Left thigh"
#                     },
#                     {
#                         "id": 24,
#                         "text": "Right knee"
#                     },
#                     {
#                         "id": 25,
#                         "text": "Left knee"
#                     },
#                     {
#                         "id": 26,
#                         "text": "Right Leg"
#                     },
#                     {
#                         "id": 27,
#                         "text": "Left Leg"
#                     },
#                     {
#                         "id": 28,
#                         "text": "Right foot & ankle"
#                     },
#                     {
#                         "id": 29,
#                         "text": "Left foot & ankle"
#                     },
#                     {
#                         "id": 30,
#                         "text": "Right toes"
#                     },
#                     {
#                         "id": 31,
#                         "text": "Left toes"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 23,
#                 "question_id": 23,
#                 "question_text": "Do you have any cramping or tightening in any muscle?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 24,
#                 "question_id": 24,
#                 "question_text": "Location of cramping/tightening",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     91,
#                     92,
#                     93,
#                     94,
#                     95,
#                     96,
#                     97,
#                     98,
#                     99,
#                     100,
#                     101,
#                     102,
#                     103,
#                     104,
#                     105,
#                     106,
#                     107,
#                     108,
#                     109,
#                     110,
#                     111,
#                     112,
#                     113,
#                     114,
#                     115,
#                     116,
#                     117,
#                     118,
#                     119,
#                     120,
#                     121
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 1,
#                         "text": "Face"
#                     },
#                     {
#                         "id": 2,
#                         "text": "Head"
#                     },
#                     {
#                         "id": 3,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 4,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 5,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 6,
#                         "text": "Right Arm"
#                     },
#                     {
#                         "id": 7,
#                         "text": "Left Arm"
#                     },
#                     {
#                         "id": 8,
#                         "text": "Right elbow"
#                     },
#                     {
#                         "id": 9,
#                         "text": "Left elbow"
#                     },
#                     {
#                         "id": 10,
#                         "text": "Right wrist"
#                     },
#                     {
#                         "id": 11,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 12,
#                         "text": "Right hand"
#                     },
#                     {
#                         "id": 13,
#                         "text": "Left hand"
#                     },
#                     {
#                         "id": 14,
#                         "text": "Right fingers"
#                     },
#                     {
#                         "id": 15,
#                         "text": "Left fingers"
#                     },
#                     {
#                         "id": 16,
#                         "text": "Upper back"
#                     },
#                     {
#                         "id": 17,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 18,
#                         "text": "Chest"
#                     },
#                     {
#                         "id": 19,
#                         "text": "Stomach"
#                     },
#                     {
#                         "id": 20,
#                         "text": "Right hip"
#                     },
#                     {
#                         "id": 21,
#                         "text": "Left Hip"
#                     },
#                     {
#                         "id": 22,
#                         "text": "Right thigh"
#                     },
#                     {
#                         "id": 23,
#                         "text": "Left thigh"
#                     },
#                     {
#                         "id": 24,
#                         "text": "Right knee"
#                     },
#                     {
#                         "id": 25,
#                         "text": "Left knee"
#                     },
#                     {
#                         "id": 26,
#                         "text": "Right Leg"
#                     },
#                     {
#                         "id": 27,
#                         "text": "Left Leg"
#                     },
#                     {
#                         "id": 28,
#                         "text": "Right foot & ankle"
#                     },
#                     {
#                         "id": 29,
#                         "text": "Left foot & ankle"
#                     },
#                     {
#                         "id": 30,
#                         "text": "Right toes"
#                     },
#                     {
#                         "id": 31,
#                         "text": "Left toes"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 25,
#                 "question_id": 100,
#                 "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 26,
#                 "question_id": 101,
#                 "question_text": "Diagnosis",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 27,
#                 "question_id": 102,
#                 "question_text": "Have you tried other medications for this condition?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 28,
#                 "question_id": 103,
#                 "question_text": "Medication name",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 29,
#                 "question_id": 104,
#                 "question_text": "Did it work?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 30,
#                 "question_id": 105,
#                 "question_text": "Location of lesion",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     122,
#                     123,
#                     124,
#                     125,
#                     126,
#                     127,
#                     128,
#                     129,
#                     130,
#                     131,
#                     132,
#                     133,
#                     134,
#                     135,
#                     136,
#                     137,
#                     138,
#                     139,
#                     140,
#                     141,
#                     142,
#                     143,
#                     144,
#                     145,
#                     146,
#                     147,
#                     148,
#                     149,
#                     150,
#                     151,
#                     152
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 1,
#                         "text": "Face"
#                     },
#                     {
#                         "id": 2,
#                         "text": "Head"
#                     },
#                     {
#                         "id": 3,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 4,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 5,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 6,
#                         "text": "Right Arm"
#                     },
#                     {
#                         "id": 7,
#                         "text": "Left Arm"
#                     },
#                     {
#                         "id": 8,
#                         "text": "Right elbow"
#                     },
#                     {
#                         "id": 9,
#                         "text": "Left elbow"
#                     },
#                     {
#                         "id": 10,
#                         "text": "Right wrist"
#                     },
#                     {
#                         "id": 11,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 12,
#                         "text": "Right hand"
#                     },
#                     {
#                         "id": 13,
#                         "text": "Left hand"
#                     },
#                     {
#                         "id": 14,
#                         "text": "Right fingers"
#                     },
#                     {
#                         "id": 15,
#                         "text": "Left fingers"
#                     },
#                     {
#                         "id": 16,
#                         "text": "Upper back"
#                     },
#                     {
#                         "id": 17,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 18,
#                         "text": "Chest"
#                     },
#                     {
#                         "id": 19,
#                         "text": "Stomach"
#                     },
#                     {
#                         "id": 20,
#                         "text": "Right hip"
#                     },
#                     {
#                         "id": 21,
#                         "text": "Left Hip"
#                     },
#                     {
#                         "id": 22,
#                         "text": "Right thigh"
#                     },
#                     {
#                         "id": 23,
#                         "text": "Left thigh"
#                     },
#                     {
#                         "id": 24,
#                         "text": "Right knee"
#                     },
#                     {
#                         "id": 25,
#                         "text": "Left knee"
#                     },
#                     {
#                         "id": 26,
#                         "text": "Right Leg"
#                     },
#                     {
#                         "id": 27,
#                         "text": "Left Leg"
#                     },
#                     {
#                         "id": 28,
#                         "text": "Right foot & ankle"
#                     },
#                     {
#                         "id": 29,
#                         "text": "Left foot & ankle"
#                     },
#                     {
#                         "id": 30,
#                         "text": "Right toes"
#                     },
#                     {
#                         "id": 31,
#                         "text": "Left toes"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 31,
#                 "question_id": 106,
#                 "question_text": "Size of lesion",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 32,
#                 "question_id": 92,
#                 "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 33,
#                 "question_id": 93,
#                 "question_text": "Diagnosis",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 34,
#                 "question_id": 94,
#                 "question_text": "Have you tried other medications for this condition?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 35,
#                 "question_id": 95,
#                 "question_text": "Medication name",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 36,
#                 "question_id": 96,
#                 "question_text": "Did it work?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 37,
#                 "question_id": 97,
#                 "question_text": "Location of lesion",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     153,
#                     154,
#                     155,
#                     156,
#                     157,
#                     158,
#                     159,
#                     160,
#                     161,
#                     162,
#                     163,
#                     164,
#                     165,
#                     166,
#                     167,
#                     168,
#                     169,
#                     170,
#                     171,
#                     172,
#                     173,
#                     174,
#                     175,
#                     176,
#                     177,
#                     178,
#                     179,
#                     180,
#                     181,
#                     182,
#                     183
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 1,
#                         "text": "Face"
#                     },
#                     {
#                         "id": 2,
#                         "text": "Head"
#                     },
#                     {
#                         "id": 3,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 4,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 5,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 6,
#                         "text": "Right Arm"
#                     },
#                     {
#                         "id": 7,
#                         "text": "Left Arm"
#                     },
#                     {
#                         "id": 8,
#                         "text": "Right elbow"
#                     },
#                     {
#                         "id": 9,
#                         "text": "Left elbow"
#                     },
#                     {
#                         "id": 10,
#                         "text": "Right wrist"
#                     },
#                     {
#                         "id": 11,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 12,
#                         "text": "Right hand"
#                     },
#                     {
#                         "id": 13,
#                         "text": "Left hand"
#                     },
#                     {
#                         "id": 14,
#                         "text": "Right fingers"
#                     },
#                     {
#                         "id": 15,
#                         "text": "Left fingers"
#                     },
#                     {
#                         "id": 16,
#                         "text": "Upper back"
#                     },
#                     {
#                         "id": 17,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 18,
#                         "text": "Chest"
#                     },
#                     {
#                         "id": 19,
#                         "text": "Stomach"
#                     },
#                     {
#                         "id": 20,
#                         "text": "Right hip"
#                     },
#                     {
#                         "id": 21,
#                         "text": "Left Hip"
#                     },
#                     {
#                         "id": 22,
#                         "text": "Right thigh"
#                     },
#                     {
#                         "id": 23,
#                         "text": "Left thigh"
#                     },
#                     {
#                         "id": 24,
#                         "text": "Right knee"
#                     },
#                     {
#                         "id": 25,
#                         "text": "Left knee"
#                     },
#                     {
#                         "id": 26,
#                         "text": "Right Leg"
#                     },
#                     {
#                         "id": 27,
#                         "text": "Left Leg"
#                     },
#                     {
#                         "id": 28,
#                         "text": "Right foot & ankle"
#                     },
#                     {
#                         "id": 29,
#                         "text": "Left foot & ankle"
#                     },
#                     {
#                         "id": 30,
#                         "text": "Right toes"
#                     },
#                     {
#                         "id": 31,
#                         "text": "Left toes"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 38,
#                 "question_id": 98,
#                 "question_text": "Size of lesion",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 39,
#                 "question_id": 99,
#                 "question_text": "Cause of lesion",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 40,
#                 "question_id": 83,
#                 "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 41,
#                 "question_id": 84,
#                 "question_text": "Diagnosis",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 42,
#                 "question_id": 85,
#                 "question_text": "Have you tried other medications for this condition?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 43,
#                 "question_id": 86,
#                 "question_text": "Medication name",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 44,
#                 "question_id": 87,
#                 "question_text": "Did it work?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 45,
#                 "question_id": 88,
#                 "question_text": "Do you have heartburn?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 46,
#                 "question_id": 89,
#                 "question_text": "On a scale of 1 to 10, rate heartburn severity",
#                 "text_answer": "1",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 47,
#                 "question_id": 90,
#                 "question_text": "How frequently does it occur?",
#                 "text_answer": "Constantly",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 48,
#                 "question_id": 91,
#                 "question_text": "Do you have bloating or gassy feelings?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 49,
#                 "question_id": 69,
#                 "question_text": "Do you have a cough?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 50,
#                 "question_id": 70,
#                 "question_text": "Is your cough dry (no phlegm)?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 51,
#                 "question_id": 71,
#                 "question_text": "How would you rate the severity of your cough?",
#                 "text_answer": "Mild",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 52,
#                 "question_id": 72,
#                 "question_text": "Is your cough due to an allergy?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 53,
#                 "question_id": 73,
#                 "question_text": "Allergy to what?",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 54,
#                 "question_id": 74,
#                 "question_text": "Do you have any type of allergy (food, drug, environment, dust chemical, hay, animal, insect, material, etc)?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 55,
#                 "question_id": 75,
#                 "question_text": "Allergy to",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 56,
#                 "question_id": 76,
#                 "question_text": "Reaction",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 57,
#                 "question_id": 77,
#                 "question_text": "What have you tried to alleviate your allergy symptoms?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     184,
#                     185,
#                     186,
#                     187,
#                     188
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 97,
#                         "text": "Antihistamines"
#                     },
#                     {
#                         "id": 98,
#                         "text": "allergy shots"
#                     },
#                     {
#                         "id": 99,
#                         "text": "Steroids"
#                     },
#                     {
#                         "id": 100,
#                         "text": "Other"
#                     },
#                     {
#                         "id": 101,
#                         "text": "None"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 58,
#                 "question_id": 78,
#                 "question_text": "Did antihistamines help?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 59,
#                 "question_id": 79,
#                 "question_text": "Did allergy shots help?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 60,
#                 "question_id": 80,
#                 "question_text": "Did steroids help?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 61,
#                 "question_id": 81,
#                 "question_text": "Other method name",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 62,
#                 "question_id": 82,
#                 "question_text": "Did other method help?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 63,
#                 "question_id": 25,
#                 "question_text": "What areas are affected by muscle or joint inflammation?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     189,
#                     190,
#                     191,
#                     192,
#                     193,
#                     194,
#                     195,
#                     196,
#                     197,
#                     198,
#                     199,
#                     200,
#                     201,
#                     202,
#                     203,
#                     204,
#                     205,
#                     206,
#                     207,
#                     208,
#                     209,
#                     210,
#                     211,
#                     212,
#                     213,
#                     214,
#                     215,
#                     216,
#                     217,
#                     218,
#                     219
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 1,
#                         "text": "Face"
#                     },
#                     {
#                         "id": 2,
#                         "text": "Head"
#                     },
#                     {
#                         "id": 3,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 4,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 5,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 6,
#                         "text": "Right Arm"
#                     },
#                     {
#                         "id": 7,
#                         "text": "Left Arm"
#                     },
#                     {
#                         "id": 8,
#                         "text": "Right elbow"
#                     },
#                     {
#                         "id": 9,
#                         "text": "Left elbow"
#                     },
#                     {
#                         "id": 10,
#                         "text": "Right wrist"
#                     },
#                     {
#                         "id": 11,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 12,
#                         "text": "Right hand"
#                     },
#                     {
#                         "id": 13,
#                         "text": "Left hand"
#                     },
#                     {
#                         "id": 14,
#                         "text": "Right fingers"
#                     },
#                     {
#                         "id": 15,
#                         "text": "Left fingers"
#                     },
#                     {
#                         "id": 16,
#                         "text": "Upper back"
#                     },
#                     {
#                         "id": 17,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 18,
#                         "text": "Chest"
#                     },
#                     {
#                         "id": 19,
#                         "text": "Stomach"
#                     },
#                     {
#                         "id": 20,
#                         "text": "Right hip"
#                     },
#                     {
#                         "id": 21,
#                         "text": "Left Hip"
#                     },
#                     {
#                         "id": 22,
#                         "text": "Right thigh"
#                     },
#                     {
#                         "id": 23,
#                         "text": "Left thigh"
#                     },
#                     {
#                         "id": 24,
#                         "text": "Right knee"
#                     },
#                     {
#                         "id": 25,
#                         "text": "Left knee"
#                     },
#                     {
#                         "id": 26,
#                         "text": "Right Leg"
#                     },
#                     {
#                         "id": 27,
#                         "text": "Left Leg"
#                     },
#                     {
#                         "id": 28,
#                         "text": "Right foot & ankle"
#                     },
#                     {
#                         "id": 29,
#                         "text": "Left foot & ankle"
#                     },
#                     {
#                         "id": 30,
#                         "text": "Right toes"
#                     },
#                     {
#                         "id": 31,
#                         "text": "Left toes"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 64,
#                 "question_id": 26,
#                 "question_text": "How long have you experienced inflammation?",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 65,
#                 "question_id": 27,
#                 "question_text": "Past inflammation treatments",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     220,
#                     221,
#                     222,
#                     223,
#                     224,
#                     225,
#                     226,
#                     227,
#                     228,
#                     229,
#                     230,
#                     231,
#                     232,
#                     233
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 60,
#                         "text": "Rest"
#                     },
#                     {
#                         "id": 61,
#                         "text": "Exercise"
#                     },
#                     {
#                         "id": 62,
#                         "text": "PT"
#                     },
#                     {
#                         "id": 63,
#                         "text": "injections"
#                     },
#                     {
#                         "id": 64,
#                         "text": "anti-inflammatories"
#                     },
#                     {
#                         "id": 65,
#                         "text": "corticosteroids"
#                     },
#                     {
#                         "id": 66,
#                         "text": "NSAIDs"
#                     },
#                     {
#                         "id": 67,
#                         "text": "steroids"
#                     },
#                     {
#                         "id": 68,
#                         "text": "opioids"
#                     },
#                     {
#                         "id": 69,
#                         "text": "oxycodone"
#                     },
#                     {
#                         "id": 70,
#                         "text": "non-prescription medications"
#                     },
#                     {
#                         "id": 71,
#                         "text": "prescription medications"
#                     },
#                     {
#                         "id": 72,
#                         "text": "muscle relaxants"
#                     },
#                     {
#                         "id": 73,
#                         "text": "Other"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 66,
#                 "question_id": 28,
#                 "question_text": "Other past inflammation treatment",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 67,
#                 "question_id": 62,
#                 "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 68,
#                 "question_id": 63,
#                 "question_text": "Diagnosis",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 69,
#                 "question_id": 64,
#                 "question_text": "Have you tried other medications for this condition?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 70,
#                 "question_id": 65,
#                 "question_text": "Medication name",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 71,
#                 "question_id": 66,
#                 "question_text": "Did it work?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 72,
#                 "question_id": 67,
#                 "question_text": "Location of lesion",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     234,
#                     235,
#                     236,
#                     237,
#                     238,
#                     239,
#                     240,
#                     241,
#                     242,
#                     243,
#                     244,
#                     245,
#                     246,
#                     247,
#                     248,
#                     249,
#                     250,
#                     251,
#                     252,
#                     253,
#                     254,
#                     255,
#                     256,
#                     257,
#                     258,
#                     259,
#                     260,
#                     261,
#                     262,
#                     263,
#                     264
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 1,
#                         "text": "Face"
#                     },
#                     {
#                         "id": 2,
#                         "text": "Head"
#                     },
#                     {
#                         "id": 3,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 4,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 5,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 6,
#                         "text": "Right Arm"
#                     },
#                     {
#                         "id": 7,
#                         "text": "Left Arm"
#                     },
#                     {
#                         "id": 8,
#                         "text": "Right elbow"
#                     },
#                     {
#                         "id": 9,
#                         "text": "Left elbow"
#                     },
#                     {
#                         "id": 10,
#                         "text": "Right wrist"
#                     },
#                     {
#                         "id": 11,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 12,
#                         "text": "Right hand"
#                     },
#                     {
#                         "id": 13,
#                         "text": "Left hand"
#                     },
#                     {
#                         "id": 14,
#                         "text": "Right fingers"
#                     },
#                     {
#                         "id": 15,
#                         "text": "Left fingers"
#                     },
#                     {
#                         "id": 16,
#                         "text": "Upper back"
#                     },
#                     {
#                         "id": 17,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 18,
#                         "text": "Chest"
#                     },
#                     {
#                         "id": 19,
#                         "text": "Stomach"
#                     },
#                     {
#                         "id": 20,
#                         "text": "Right hip"
#                     },
#                     {
#                         "id": 21,
#                         "text": "Left Hip"
#                     },
#                     {
#                         "id": 22,
#                         "text": "Right thigh"
#                     },
#                     {
#                         "id": 23,
#                         "text": "Left thigh"
#                     },
#                     {
#                         "id": 24,
#                         "text": "Right knee"
#                     },
#                     {
#                         "id": 25,
#                         "text": "Left knee"
#                     },
#                     {
#                         "id": 26,
#                         "text": "Right Leg"
#                     },
#                     {
#                         "id": 27,
#                         "text": "Left Leg"
#                     },
#                     {
#                         "id": 28,
#                         "text": "Right foot & ankle"
#                     },
#                     {
#                         "id": 29,
#                         "text": "Left foot & ankle"
#                     },
#                     {
#                         "id": 30,
#                         "text": "Right toes"
#                     },
#                     {
#                         "id": 31,
#                         "text": "Left toes"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 73,
#                 "question_id": 68,
#                 "question_text": "Size of lesion",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 74,
#                 "question_id": 47,
#                 "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 75,
#                 "question_id": 48,
#                 "question_text": "Diagnosis",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 76,
#                 "question_id": 49,
#                 "question_text": "Do you have migraines 15 or more times a month?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 77,
#                 "question_id": 50,
#                 "question_text": "Have you tried other medications for this condition?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 78,
#                 "question_id": 51,
#                 "question_text": "Medication name",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 79,
#                 "question_id": 52,
#                 "question_text": "Did it work?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 80,
#                 "question_id": 53,
#                 "question_text": "Have you been previously diagnosed with migraine by a health professional?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 81,
#                 "question_id": 54,
#                 "question_text": "Is your headache throbbing, pulsating or pounding?",
#                 "text_answer": "Throbbing",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 82,
#                 "question_id": 55,
#                 "question_text": "Where is the head pain located?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     265,
#                     266,
#                     267,
#                     268,
#                     269
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 81,
#                         "text": "Left"
#                     },
#                     {
#                         "id": 82,
#                         "text": "Right"
#                     },
#                     {
#                         "id": 83,
#                         "text": "Both Sides"
#                     },
#                     {
#                         "id": 84,
#                         "text": "Front"
#                     },
#                     {
#                         "id": 85,
#                         "text": "Back"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 83,
#                 "question_id": 56,
#                 "question_text": "How often does your headache occur?",
#                 "text_answer": "Constantly",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 84,
#                 "question_id": 57,
#                 "question_text": "Do you experience symptoms prior to the migraine?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     270,
#                     271,
#                     272,
#                     273,
#                     274
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 86,
#                         "text": "Light Sensitivity"
#                     },
#                     {
#                         "id": 87,
#                         "text": "Visual Symptoms"
#                     },
#                     {
#                         "id": 88,
#                         "text": "Dizziness"
#                     },
#                     {
#                         "id": 89,
#                         "text": "Nausea"
#                     },
#                     {
#                         "id": 90,
#                         "text": "Vomiting"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 85,
#                 "question_id": 58,
#                 "question_text": "Are you currently taking any migraine medication(s)?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 86,
#                 "question_id": 59,
#                 "question_text": "Current migraine medication name",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 87,
#                 "question_id": 60,
#                 "question_text": "Do you have a history of hypertension, stroke, or any type of heart disease?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 88,
#                 "question_id": 61,
#                 "question_text": "Disease history types",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     275,
#                     276,
#                     277
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 91,
#                         "text": "Hypertension"
#                     },
#                     {
#                         "id": 92,
#                         "text": "Stroke"
#                     },
#                     {
#                         "id": 93,
#                         "text": "Heart Disease"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 89,
#                 "question_id": 112,
#                 "question_text": "Where is the location of your acne?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     278,
#                     279,
#                     280,
#                     281,
#                     282,
#                     283,
#                     284,
#                     285,
#                     286,
#                     287,
#                     288,
#                     289,
#                     290,
#                     291,
#                     292,
#                     293,
#                     294,
#                     295,
#                     296,
#                     297,
#                     298,
#                     299,
#                     300,
#                     301,
#                     302,
#                     303,
#                     304,
#                     305,
#                     306,
#                     307,
#                     308
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 1,
#                         "text": "Face"
#                     },
#                     {
#                         "id": 2,
#                         "text": "Head"
#                     },
#                     {
#                         "id": 3,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 4,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 5,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 6,
#                         "text": "Right Arm"
#                     },
#                     {
#                         "id": 7,
#                         "text": "Left Arm"
#                     },
#                     {
#                         "id": 8,
#                         "text": "Right elbow"
#                     },
#                     {
#                         "id": 9,
#                         "text": "Left elbow"
#                     },
#                     {
#                         "id": 10,
#                         "text": "Right wrist"
#                     },
#                     {
#                         "id": 11,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 12,
#                         "text": "Right hand"
#                     },
#                     {
#                         "id": 13,
#                         "text": "Left hand"
#                     },
#                     {
#                         "id": 14,
#                         "text": "Right fingers"
#                     },
#                     {
#                         "id": 15,
#                         "text": "Left fingers"
#                     },
#                     {
#                         "id": 16,
#                         "text": "Upper back"
#                     },
#                     {
#                         "id": 17,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 18,
#                         "text": "Chest"
#                     },
#                     {
#                         "id": 19,
#                         "text": "Stomach"
#                     },
#                     {
#                         "id": 20,
#                         "text": "Right hip"
#                     },
#                     {
#                         "id": 21,
#                         "text": "Left Hip"
#                     },
#                     {
#                         "id": 22,
#                         "text": "Right thigh"
#                     },
#                     {
#                         "id": 23,
#                         "text": "Left thigh"
#                     },
#                     {
#                         "id": 24,
#                         "text": "Right knee"
#                     },
#                     {
#                         "id": 25,
#                         "text": "Left knee"
#                     },
#                     {
#                         "id": 26,
#                         "text": "Right Leg"
#                     },
#                     {
#                         "id": 27,
#                         "text": "Left Leg"
#                     },
#                     {
#                         "id": 28,
#                         "text": "Right foot & ankle"
#                     },
#                     {
#                         "id": 29,
#                         "text": "Left foot & ankle"
#                     },
#                     {
#                         "id": 30,
#                         "text": "Right toes"
#                     },
#                     {
#                         "id": 31,
#                         "text": "Left toes"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 90,
#                 "question_id": 113,
#                 "question_text": "How many bumps do you have?",
#                 "text_answer": "1-2",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 91,
#                 "question_id": 114,
#                 "question_text": "Has this caused scabbing or scaring?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 92,
#                 "question_id": 115,
#                 "question_text": "Do you clean this location regularly?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 93,
#                 "question_id": 116,
#                 "question_text": "How many of these bumps are full of pus or fluid?",
#                 "text_answer": "3-5",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 94,
#                 "question_id": 117,
#                 "question_text": "What previous methods have you used to treat acne?",
#                 "text_answer": "Face washes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 95,
#                 "question_id": 40,
#                 "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 96,
#                 "question_id": 41,
#                 "question_text": "Diagnosis",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 97,
#                 "question_id": 42,
#                 "question_text": "Have you tried other medications for this condition?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 98,
#                 "question_id": 43,
#                 "question_text": "Medication name",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 99,
#                 "question_id": 44,
#                 "question_text": "Did it work?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 100,
#                 "question_id": 45,
#                 "question_text": "Location of lesion",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     309,
#                     310,
#                     311,
#                     312,
#                     313,
#                     314,
#                     315,
#                     316,
#                     317,
#                     318,
#                     319,
#                     320,
#                     321,
#                     322,
#                     323,
#                     324,
#                     325,
#                     326,
#                     327,
#                     328,
#                     329,
#                     330,
#                     331,
#                     332,
#                     333,
#                     334,
#                     335,
#                     336,
#                     337,
#                     338,
#                     339
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 1,
#                         "text": "Face"
#                     },
#                     {
#                         "id": 2,
#                         "text": "Head"
#                     },
#                     {
#                         "id": 3,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 4,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 5,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 6,
#                         "text": "Right Arm"
#                     },
#                     {
#                         "id": 7,
#                         "text": "Left Arm"
#                     },
#                     {
#                         "id": 8,
#                         "text": "Right elbow"
#                     },
#                     {
#                         "id": 9,
#                         "text": "Left elbow"
#                     },
#                     {
#                         "id": 10,
#                         "text": "Right wrist"
#                     },
#                     {
#                         "id": 11,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 12,
#                         "text": "Right hand"
#                     },
#                     {
#                         "id": 13,
#                         "text": "Left hand"
#                     },
#                     {
#                         "id": 14,
#                         "text": "Right fingers"
#                     },
#                     {
#                         "id": 15,
#                         "text": "Left fingers"
#                     },
#                     {
#                         "id": 16,
#                         "text": "Upper back"
#                     },
#                     {
#                         "id": 17,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 18,
#                         "text": "Chest"
#                     },
#                     {
#                         "id": 19,
#                         "text": "Stomach"
#                     },
#                     {
#                         "id": 20,
#                         "text": "Right hip"
#                     },
#                     {
#                         "id": 21,
#                         "text": "Left Hip"
#                     },
#                     {
#                         "id": 22,
#                         "text": "Right thigh"
#                     },
#                     {
#                         "id": 23,
#                         "text": "Left thigh"
#                     },
#                     {
#                         "id": 24,
#                         "text": "Right knee"
#                     },
#                     {
#                         "id": 25,
#                         "text": "Left knee"
#                     },
#                     {
#                         "id": 26,
#                         "text": "Right Leg"
#                     },
#                     {
#                         "id": 27,
#                         "text": "Left Leg"
#                     },
#                     {
#                         "id": 28,
#                         "text": "Right foot & ankle"
#                     },
#                     {
#                         "id": 29,
#                         "text": "Left foot & ankle"
#                     },
#                     {
#                         "id": 30,
#                         "text": "Right toes"
#                     },
#                     {
#                         "id": 31,
#                         "text": "Left toes"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 101,
#                 "question_id": 46,
#                 "question_text": "Size of lesion",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 102,
#                 "question_id": 29,
#                 "question_text": "Do you currently have blisters?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 103,
#                 "question_id": 30,
#                 "question_text": "Location of blisters",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     340,
#                     341,
#                     342,
#                     343,
#                     344,
#                     345,
#                     346,
#                     347,
#                     348,
#                     349,
#                     350,
#                     351,
#                     352,
#                     353,
#                     354,
#                     355,
#                     356,
#                     357,
#                     358,
#                     359,
#                     360,
#                     361,
#                     362,
#                     363,
#                     364,
#                     365,
#                     366,
#                     367,
#                     368,
#                     369,
#                     370
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 1,
#                         "text": "Face"
#                     },
#                     {
#                         "id": 2,
#                         "text": "Head"
#                     },
#                     {
#                         "id": 3,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 4,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 5,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 6,
#                         "text": "Right Arm"
#                     },
#                     {
#                         "id": 7,
#                         "text": "Left Arm"
#                     },
#                     {
#                         "id": 8,
#                         "text": "Right elbow"
#                     },
#                     {
#                         "id": 9,
#                         "text": "Left elbow"
#                     },
#                     {
#                         "id": 10,
#                         "text": "Right wrist"
#                     },
#                     {
#                         "id": 11,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 12,
#                         "text": "Right hand"
#                     },
#                     {
#                         "id": 13,
#                         "text": "Left hand"
#                     },
#                     {
#                         "id": 14,
#                         "text": "Right fingers"
#                     },
#                     {
#                         "id": 15,
#                         "text": "Left fingers"
#                     },
#                     {
#                         "id": 16,
#                         "text": "Upper back"
#                     },
#                     {
#                         "id": 17,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 18,
#                         "text": "Chest"
#                     },
#                     {
#                         "id": 19,
#                         "text": "Stomach"
#                     },
#                     {
#                         "id": 20,
#                         "text": "Right hip"
#                     },
#                     {
#                         "id": 21,
#                         "text": "Left Hip"
#                     },
#                     {
#                         "id": 22,
#                         "text": "Right thigh"
#                     },
#                     {
#                         "id": 23,
#                         "text": "Left thigh"
#                     },
#                     {
#                         "id": 24,
#                         "text": "Right knee"
#                     },
#                     {
#                         "id": 25,
#                         "text": "Left knee"
#                     },
#                     {
#                         "id": 26,
#                         "text": "Right Leg"
#                     },
#                     {
#                         "id": 27,
#                         "text": "Left Leg"
#                     },
#                     {
#                         "id": 28,
#                         "text": "Right foot & ankle"
#                     },
#                     {
#                         "id": 29,
#                         "text": "Left foot & ankle"
#                     },
#                     {
#                         "id": 30,
#                         "text": "Right toes"
#                     },
#                     {
#                         "id": 31,
#                         "text": "Left toes"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 104,
#                 "question_id": 31,
#                 "question_text": "Describe the blisters",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     371,
#                     372,
#                     373,
#                     374
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 74,
#                         "text": "Single"
#                     },
#                     {
#                         "id": 75,
#                         "text": "Multiple"
#                     },
#                     {
#                         "id": 76,
#                         "text": "Small (pinhead size)"
#                     },
#                     {
#                         "id": 77,
#                         "text": "Large (pea size)"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 105,
#                 "question_id": 32,
#                 "question_text": "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 106,
#                 "question_id": 33,
#                 "question_text": "Diagnosis",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 107,
#                 "question_id": 34,
#                 "question_text": "Have you tried other medications for this condition?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 108,
#                 "question_id": 35,
#                 "question_text": "Medication name",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 109,
#                 "question_id": 36,
#                 "question_text": "Did it work?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 110,
#                 "question_id": 37,
#                 "question_text": "Have you had previous cold sore episodes?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 111,
#                 "question_id": 38,
#                 "question_text": "Were the previous episodes similar to the current episode?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 112,
#                 "question_id": 39,
#                 "question_text": "Do you concurrently have eye symptoms, ear symptoms, or severe headaches?",
#                 "text_answer": "Yes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 113,
#                 "question_id": 107,
#                 "question_text": "Are you currently living with any of the following conditions?",
#                 "text_answer": "Diabetes or Prediabetes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 114,
#                 "question_id": 108,
#                 "question_text": "Which type of diabetes?",
#                 "text_answer": "Prediabetes",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 115,
#                 "question_id": 109,
#                 "question_text": "What was your most recent A1c result?",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 116,
#                 "question_id": 110,
#                 "question_text": "What was the approximate date of your most recent A1c results?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": "1990-01-01",
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 117,
#                 "question_id": 111,
#                 "question_text": "Have you ever been diagnosed with any of the following?",
#                 "text_answer": "Kidney or Renal Disease",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 118,
#                 "question_id": 118,
#                 "question_text": "Where is the pain located?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     375,
#                     376,
#                     377,
#                     378,
#                     379,
#                     380,
#                     381,
#                     382,
#                     383,
#                     384,
#                     385,
#                     386,
#                     387,
#                     388
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 148,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 149,
#                         "text": "Right Shoulder"
#                     },
#                     {
#                         "id": 150,
#                         "text": "Left Shoulder"
#                     },
#                     {
#                         "id": 151,
#                         "text": "Right Elbow"
#                     },
#                     {
#                         "id": 152,
#                         "text": "Left Elbow"
#                     },
#                     {
#                         "id": 153,
#                         "text": "Right Wrist"
#                     },
#                     {
#                         "id": 154,
#                         "text": "Left Wrist"
#                     },
#                     {
#                         "id": 155,
#                         "text": "Lower Back"
#                     },
#                     {
#                         "id": 156,
#                         "text": "Right Knee"
#                     },
#                     {
#                         "id": 157,
#                         "text": "Left Knee"
#                     },
#                     {
#                         "id": 158,
#                         "text": "Right Foot & Ankle"
#                     },
#                     {
#                         "id": 159,
#                         "text": "Left Foot & Ankle"
#                     },
#                     {
#                         "id": 160,
#                         "text": "Right Hip"
#                     },
#                     {
#                         "id": 161,
#                         "text": "Left Hip"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 119,
#                 "question_id": 119,
#                 "question_text": "What level of pain are you experiencing?",
#                 "text_answer": "No Pain",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 120,
#                 "question_id": 120,
#                 "question_text": "What prior therapeutic interventions have you tried?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     389,
#                     390,
#                     391,
#                     392,
#                     393,
#                     394,
#                     395,
#                     396,
#                     397,
#                     398,
#                     399,
#                     400,
#                     401,
#                     402
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 60,
#                         "text": "Rest"
#                     },
#                     {
#                         "id": 61,
#                         "text": "Exercise"
#                     },
#                     {
#                         "id": 62,
#                         "text": "PT"
#                     },
#                     {
#                         "id": 63,
#                         "text": "injections"
#                     },
#                     {
#                         "id": 64,
#                         "text": "anti-inflammatories"
#                     },
#                     {
#                         "id": 65,
#                         "text": "corticosteroids"
#                     },
#                     {
#                         "id": 66,
#                         "text": "NSAIDs"
#                     },
#                     {
#                         "id": 67,
#                         "text": "steroids"
#                     },
#                     {
#                         "id": 68,
#                         "text": "opioids"
#                     },
#                     {
#                         "id": 69,
#                         "text": "oxycodone"
#                     },
#                     {
#                         "id": 70,
#                         "text": "non-prescription medications"
#                     },
#                     {
#                         "id": 71,
#                         "text": "prescription medications"
#                     },
#                     {
#                         "id": 72,
#                         "text": "muscle relaxants"
#                     },
#                     {
#                         "id": 73,
#                         "text": "Other"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 121,
#                 "question_id": 121,
#                 "question_text": "Other prior therapeutic intervention",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 122,
#                 "question_id": 122,
#                 "question_text": "Do you have difficulty attempting activities/movements with objects > 5lbs?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     403,
#                     404,
#                     405,
#                     406,
#                     407,
#                     408
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 167,
#                         "text": "None"
#                     },
#                     {
#                         "id": 168,
#                         "text": "Lifting"
#                     },
#                     {
#                         "id": 169,
#                         "text": "Pushing"
#                     },
#                     {
#                         "id": 170,
#                         "text": "Pulling"
#                     },
#                     {
#                         "id": 171,
#                         "text": "Bending"
#                     },
#                     {
#                         "id": 172,
#                         "text": "Rotating"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 123,
#                 "question_id": 123,
#                 "question_text": "Date of accident",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": "1990-01-01",
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 124,
#                 "question_id": 124,
#                 "question_text": "What activities/movements make the pain worse?",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 125,
#                 "question_id": 125,
#                 "question_text": "Have you had, or will have, surgery on the affected area?",
#                 "text_answer": "Yes (Surgical)",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 126,
#                 "question_id": 126,
#                 "question_text": "Date of surgery if applicable",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 127,
#                 "question_id": 127,
#                 "question_text": "Where is the pain located?",
#                 "text_answer": None,
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": [
#                     409,
#                     410,
#                     411,
#                     412,
#                     413,
#                     414,
#                     415,
#                     416
#                 ],
#                 "selected_choices": [
#                     {
#                         "id": 175,
#                         "text": "Neck"
#                     },
#                     {
#                         "id": 176,
#                         "text": "Elbow"
#                     },
#                     {
#                         "id": 177,
#                         "text": "Leg"
#                     },
#                     {
#                         "id": 178,
#                         "text": "Foot/Ankle"
#                     },
#                     {
#                         "id": 179,
#                         "text": "Shoulder"
#                     },
#                     {
#                         "id": 180,
#                         "text": "Knee"
#                     },
#                     {
#                         "id": 181,
#                         "text": "Wrist"
#                     },
#                     {
#                         "id": 182,
#                         "text": "Back"
#                     }
#                 ]
#             },
#             {
#                 "answer_id": 128,
#                 "question_id": 128,
#                 "question_text": "Orientation",
#                 "text_answer": "Left",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 129,
#                 "question_id": 129,
#                 "question_text": "Have you had, or will have, surgery on the affected area?",
#                 "text_answer": "Yes (Surgical)",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             },
#             {
#                 "answer_id": 130,
#                 "question_id": 130,
#                 "question_text": "Date of surgery if applicable",
#                 "text_answer": "Test Entry",
#                 "number_answer": None,
#                 "boolean_answer": None,
#                 "date_answer": None,
#                 "selected_choice_ids": []
#             }
#         ]
#     },

# }

# trucare/prescription/pdfbuilder/intake_pdf_builder.py

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import json
from io import BytesIO

class IntakePDFBuilder:
    """Generate professional PDF from intake data with minimal, maintainable code."""
    
    def __init__(self, intake_data: dict, filename: str = None):
        print(intake_data)

        self.intake_data = intake_data
        self.filename = filename or f"intake_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Define custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='Header1',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.black,
            background=colors.HexColor('#1f4788'),
            spaceAfter=6,
            fontName='Helvetica-Bold',
            leftIndent=5,
            rightIndent=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='Label',
            fontSize=9,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Value',
            fontSize=9,
            textColor=colors.HexColor('#555555'),
            fontName='Helvetica'
        ))
    
    def _build_header(self):
        """Create professional header with company info and patient details."""

        patient = self.intake_data.get('patient_info', {})
        
        # Company header
        logo_path = "./prescription/pdfbuilder/logo.jpg" 
        logo = Image(logo_path, width=2.5*inch, height=1*inch)
        header_data = [
            [logo],
            [
                Paragraph("<br/>Telemedicine Services", self.styles['Header1']),
            ]
        ]
        
        header_table = Table(header_data, colWidths=[7.5*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            # ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f4f8')),
            ('LINEBELOW', (0, 0), (-1, -1), 2, colors.HexColor('#1f4788')),
        ]))
        
        # Patient info strip
        patient_full_name = f"{patient.get('first_name', 'N/A')} {patient.get('last_name', 'N/A')}"
        patient_info_data = [
            [
                f"<b>Patient:</b> {patient_full_name}",
                f"<b>DOB:</b> {patient.get('date_of_birth', 'N/A')}",
                f"<b>ID:</b> {patient.get('id', 'N/A')}"
            ],
            [
                f"<b>Email:</b> {patient.get('email', 'N/A')}",
                f"<b>Phone:</b> {patient.get('phone_number', 'N/A')}",
                f"<b>State:</b> {patient.get('state', 'N/A')}"
            ],
            [
                {
                    'value': f"<b>Address:</b> {patient.get('address', 'N/A')}",
                    'colspan': 3
                }
            ]
        ]
        
        patient_table = Table(
            [[Paragraph(cell['value'] if isinstance(cell, dict) else cell, self.styles['Value']) 
              for cell in row] for row in patient_info_data],
            colWidths=[2.5*inch, 2.5*inch, 2.5*inch]
        )
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f0f7')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        return [header_table, Spacer(1, 0.2*inch), patient_table, Spacer(1, 0.3*inch)]
    
    def _section_to_table(self, section_title: str, data: dict) -> Table:
        """Convert a data section into a formatted table."""
        rows = [
            [Paragraph(f"<b>{key.replace('_', ' ').title()}</b>", self.styles['Label']),
             Paragraph(str(value) if value is not None else 'N/A', self.styles['Value'])]
            for key, value in data.items()
            if not key.startswith('created_at') and not key.startswith('updated_at') and not key.startswith('id')
        ]
        
        if not rows:
            rows = [[Paragraph("No data available", self.styles['Value'])]]
        
        table = Table(rows, colWidths=[2.0*inch, 5.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        
        return table
    
    def _build_sections(self):
        """Build all data sections dynamically."""
        elements = []
        info = self.intake_data.get('intake_info', {})
        
        # Main sections to display
        sections = {
            'Patient Information': self.intake_data.get('patient_info', {}),
            'Patient Intake': self.intake_data.get('patient_intake', {}),
        }
        
        for section_title, section_data in sections.items():
            if section_data:
                elements.append(Paragraph(section_title, self.styles['SectionHeader']))
                elements.append(Spacer(1, 0.1*inch))
                elements.append(self._section_to_table(section_title, section_data))
                elements.append(Spacer(1, 0.3*inch))
        
        # List-based sections
        list_sections = {
            'Insurance Information': self.intake_data.get('insurances', []),
            'Medical History': self.intake_data.get('medical_history', []),
            'Family History': self.intake_data.get('family_history', []),
            'Health Records': self.intake_data.get('health_records', []),
        }
        
        for section_title, items in list_sections.items():
            if items and len(items) > 0:
                elements.append(Paragraph(section_title, self.styles['SectionHeader']))
                elements.append(Spacer(1, 0.1*inch))
                
                for idx, item in enumerate(items):
                    elements.append(self._section_to_table(f"{section_title} #{idx+1}", item))
                    if idx < len(items) - 1:
                        elements.append(Spacer(1, 0.15*inch))
                
                elements.append(Spacer(1, 0.3*inch))
        
        # Requested conditions
        conditions = self.intake_data.get('requested_conditions', [])
        self.conditions = conditions  # Store for potential future use
        if conditions:
            condition_rows = [
                [Paragraph(c.get('condition_name', 'N/A'), self.styles['Value']),
                 Paragraph('✓ Yes' if c.get('requested') else '✗ No', self.styles['Value'])]
                for c in conditions
            ]
            
            elements.append(Paragraph('Requested Conditions', self.styles['SectionHeader']))
            elements.append(Spacer(1, 0.1*inch))
            
            conditions_table = Table(condition_rows, colWidths=[5.0*inch, 2.5*inch])
            conditions_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            elements.append(conditions_table)

        
        for condition in self.conditions:
            condition_answers_row = []

            for answer in self.intake_data.get('condition_answers', []):
                if answer.get('condition_id') == condition.get('id'):
                    question = answer.get('question_text', 'N/A')
                    text_answer = answer.get('text_answer', 'N/A')
                    if text_answer is None:
                        text_answer = answer.get('number_answer', 'N/A')
                    if text_answer is None:
                        text_answer = answer.get('boolean_answer', 'N/A')
                    if text_answer is None:
                        text_answer = answer.get('selected_choices', 'N/A')
                        if isinstance(text_answer, list):
                            text_answer = ', '.join([choice.get('text', 'N/A') for choice in text_answer])
                    if text_answer is None: 
                        text_answer = 'N/A'
                    # Add logic to format and add the question and answer to the PDF
                    condition_answers_row.append([Paragraph(question, self.styles['Value']),
                                                  Paragraph(text_answer, self.styles['Value'])])

            if condition_answers_row!=[]:
                elements.append(Paragraph(condition.get('condition_name', 'N/A'), self.styles['SectionHeader']))

                condition_answers_table = Table(condition_answers_row, colWidths=[5.0*inch, 2.5*inch])
                condition_answers_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ]))
                elements.append(Spacer(1, 0.1*inch))
                elements.append(condition_answers_table)
                elements.append(Spacer(1, 0.3*inch))

        return elements
    
    def _build_footer(self):
        """Add footer with generation timestamp."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        footer = Paragraph(
            f"<i>Report generated on {timestamp}</i>",
            ParagraphStyle(
                name='Footer',
                fontSize=8,
                textColor=colors.HexColor('#999999'),
                alignment=TA_CENTER
            )
        )
        return [Spacer(1, 0.4*inch), footer]
    
    def generate(self, output_path: str = None) -> bytes:
        """Generate PDF and return bytes or save to file."""
        # Create in-memory PDF if no output path
        if output_path:
            pdf_file = output_path
        else:
            pdf_file = BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Build elements
        elements = []
        elements.extend(self._build_header())
        elements.extend(self._build_sections())
        elements.extend(self._build_footer())
        
        # Build PDF
        doc.build(elements)
        
        # Return bytes if in-memory, otherwise return path
        if not output_path:
            pdf_file.seek(0)
            return pdf_file.read()
        
        return None