"""
Seed script for dynamic condition form data.

Creates/updates:
- ChoiceSet
- Choice
- Condition
- ConditionQuestion

Run from /Telemed-Django/trucare:
    python intake/seed_patient_form_data.py

or:
    python manage.py shell < intake/seed_patient_form_data.py
"""

import os
from typing import Dict, List

import django
from django.db import transaction


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trucare.settings")
django.setup()

from intake.models import Choice, ChoiceSet, Condition, ConditionQuestion  # noqa: E402


CHOICE_SETS: Dict[str, List[str]] = {
    "PAIN_LOCATIONS_ALL": [
        "Face", "Head", "Neck", "Right Shoulder", "Left Shoulder", "Right Arm", "Left Arm",
        "Right elbow", "Left elbow", "Right wrist", "Left Wrist", "Right hand", "Left hand",
        "Right fingers", "Left fingers", "Upper back", "Lower Back", "Chest", "Stomach",
        "Right hip", "Left Hip", "Right thigh", "Left thigh", "Right knee", "Left knee",
        "Right Leg", "Left Leg", "Right foot & ankle", "Left foot & ankle", "Right toes", "Left toes",
    ],
    "YES_NO_DONT_KNOW": ["Yes", "No", "Don't Know"],
    "FREQUENCY_STANDARD": ["Constantly", "Frequently", "Occasionally", "Intermittently"],
    "SYMPTOMS_CHANGING": ["Getting worse", "Staying the same", "Getting better"],
    "PAIN_TYPE": ["Aching", "Burning", "Stabbing", "Cramping", "Sharp", "Dull"],
    "SCALE_1_TO_10": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    "THERAPEUTIC_INTERVENTIONS": [
        "Rest", "Exercise", "PT", "injections", "anti-inflammatories", "corticosteroids", "NSAIDs",
        "steroids", "opioids", "oxycodone", "non-prescription medications", "prescription medications",
        "muscle relaxants", "Other",
    ],
    "COLD_SORES_BLISTER_DESCRIPTION": [
        "Single", "Multiple", "Small (pinhead size)", "Large (pea size)",
    ],
    "MIGRAINE_HEADACHE_CHARACTER": ["Throbbing", "pulsating", "pounding"],
    "MIGRAINE_HEAD_PAIN_LOCATION": ["Left", "Right", "Both Sides", "Front", "Back"],
    "MIGRAINE_PRIOR_SYMPTOMS": ["Light Sensitivity", "Visual Symptoms", "Dizziness", "Nausea", "Vomiting"],
    "MIGRAINE_DISEASE_HISTORY_TYPES": ["Hypertension", "Stroke", "Heart Disease"],
    "COUGH_SEVERITY": ["Mild", "Moderate", "Severe"],
    "ALLERGY_RELIEF_METHODS": ["Antihistamines", "allergy shots", "Steroids", "Other", "None"],
    "DIABETES_CURRENT_CONDITIONS": [
        "Diabetes or Prediabetes",
        "I might have diabetes or Prediabetes but have never been diagnosed",
        "High blood pressure aka hypertension",
        "High Cholesterol aka hyperlipidemia",
        "None of the above",
    ],
    "DIABETES_TYPE": ["Prediabetes", "Type 2 diabetes", "Type 1 diabetes", "Gestational diabetes", "I am not sure"],
    "DIABETES_FURTHER_DIAGNOSED": [
        "Kidney or Renal Disease", "Live or Hepatic Disease", "Stroke", "Congestive heart failure",
        "Peripheral artery disease", "Coronary artery disease", "Acute or Chronic metabolic acidosis",
        "None of the above",
    ],
    "ACNE_BUMPS_COUNT": ["1-2", "3-5", "5-10", "11-20", "21-30", "More than 30", "Unspecified"],
    "YES_NO_UNSPECIFIED": ["Yes", "No", "Unspecified"],
    "ACNE_PUS_COUNT": ["3-5", "5-10", "11-20", "21-30", "More than 30", "Most of them", "All of them", "Unspecified"],
    "ACNE_PREVIOUS_TREATMENTS": [
        "Face washes", "Retinoids -like drugs", "Oral Antibiotics", "Topical Antibiotics", "Azelaic Acid",
        "Salicylic Acid", "Benzoyl Peroxide", "Hormones or birth control", "No past treatments", "Unspecified",
    ],
    "LASER_PAIN_LOCATIONS": [
        "Neck", "Right Shoulder", "Left Shoulder", "Right Elbow", "Left Elbow", "Right Wrist", "Left Wrist",
        "Lower Back", "Right Knee", "Left Knee", "Right Foot & Ankle", "Left Foot & Ankle", "Right Hip", "Left Hip",
    ],
    "LASER_PAIN_LEVEL": ["No Pain", "Mild Pain", "Moderate Pain", "Severe Pain", "Worst Pain Possible"],
    "DIFFICULTY_MOVEMENTS_GT_5LB": ["None", "Lifting", "Pushing", "Pulling", "Bending", "Rotating"],
    "SURGERY_HISTORY": ["Yes (Surgical)", "No (Non Surgical)"],
    "CCT_PAIN_LOCATIONS": ["Neck", "Elbow", "Leg", "Foot/Ankle", "Shoulder", "Knee", "Wrist", "Back"],
    "CCT_ORIENTATION": ["Left", "Right", "Bilateral", "N/A"],
}


CONDITIONS = [
    {"code": "pain_request", "name": "Pain condition request?"},
    {"code": "muscle_relaxer", "name": "Muscle relaxer condition request?"},
    {"code": "dermatitis_eczema_psoriasis", "name": "Dermatitis/Eczema/Psoriasis condition request?"},
    {"code": "scar_wound_actinic", "name": "Scar/wound/actinic keratosis condition request?"},
    {"code": "acid_reflux", "name": "Acid reflux condition request?"},
    {"code": "allergy", "name": "Allergy condition request?"},
    {"code": "cough", "name": "Cough condition request?"},
    {"code": "topical_antifungal", "name": "Topical anti-fungal condition request?"},
    {"code": "migraine_headache", "name": "Migraine and Headache condition request?"},
    {"code": "foot_bath", "name": "Foot bath condition request?"},
    {"code": "cold_sores", "name": "Cold sores condition request?"},
    {"code": "oral_nsaids", "name": "Oral NSAIDs condition request?"},
    {"code": "acne", "name": "Acne condition request?"},
    {"code": "diabetes", "name": "Diabetes condition request?"},
    {"code": "laser_therapy_pain", "name": "Laser Therapy Pain treatment request?"},
    {"code": "cold_compression", "name": "Cold Compression Therapy request?"},
]


QUESTIONS = {
    "pain_request": [
        ("Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?", "yes_no", None),
        ("Diagnosis", "text", None),
        ("Have you tried other medications for this condition?", "yes_no", None),
        ("Medications", "text", None),
        ("Have you ever used Lidocaine for pain?", "yes_no", None),
        ("For what pain", "text", None),
        ("What type of pain are you experiencing?", "single_choice", "PAIN_TYPE"),
        ("On a scale of 1 to 10, rate severity of your pain", "single_choice", "SCALE_1_TO_10"),
        ("Where is the pain located?", "multiple_choice", "PAIN_LOCATIONS_ALL"),
        ("How long have you had this problem (days, weeks, months etc.)?", "text", None),
        ("How often do you experience the symptoms?", "single_choice", "FREQUENCY_STANDARD"),
        ("How are your symptoms changing with time?", "single_choice", "SYMPTOMS_CHANGING"),
        ("How do you think your problem began?", "text", None),
        ("What activities make the pain worse?", "text", None),
        ("What activities reduce the pain?", "text", None),
        ("What prior therapeutic interventions have you tried?", "multiple_choice", "THERAPEUTIC_INTERVENTIONS"),
        ("Other prior therapeutic intervention", "text", None),
        ("Which therapeutic interventions afforded improvement of symptoms?", "multiple_choice", "THERAPEUTIC_INTERVENTIONS"),
        ("Other intervention that afforded improvement", "text", None),
        ("Do you have a history of seizures, heart arrhythmias, or pacemaker use?", "yes_no", None),
    ],
    "muscle_relaxer": [
        ("Do you have muscle spasms?", "yes_no", None),
        ("Location of muscle spasms", "multiple_choice", "PAIN_LOCATIONS_ALL"),
        ("Do you have any cramping or tightening in any muscle?", "yes_no", None),
        ("Location of cramping/tightening", "multiple_choice", "PAIN_LOCATIONS_ALL"),
    ],
    "oral_nsaids": [
        ("What areas are affected by muscle or joint inflammation?", "multiple_choice", "PAIN_LOCATIONS_ALL"),
        ("How long have you experienced inflammation?", "text", None),
        ("Past inflammation treatments", "multiple_choice", "THERAPEUTIC_INTERVENTIONS"),
        ("Other past inflammation treatment", "text", None),
    ],
    "cold_sores": [
        ("Do you currently have blisters?", "yes_no", None),
        ("Location of blisters", "multiple_choice", "PAIN_LOCATIONS_ALL"),
        ("Describe the blisters", "multiple_choice", "COLD_SORES_BLISTER_DESCRIPTION"),
        ("Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?", "yes_no", None),
        ("Diagnosis", "text", None),
        ("Have you tried other medications for this condition?", "yes_no", None),
        ("Medication name", "text", None),
        ("Did it work?", "yes_no", None),
        ("Have you had previous cold sore episodes?", "yes_no", None),
        ("Were the previous episodes similar to the current episode?", "yes_no", None),
        ("Do you concurrently have eye symptoms, ear symptoms, or severe headaches?", "yes_no", None),
    ],
    "foot_bath": [
        ("Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?", "yes_no", None),
        ("Diagnosis", "text", None),
        ("Have you tried other medications for this condition?", "yes_no", None),
        ("Medication name", "text", None),
        ("Did it work?", "yes_no", None),
        ("Location of lesion", "multiple_choice", "PAIN_LOCATIONS_ALL"),
        ("Size of lesion", "text", None),
    ],
    "migraine_headache": [
        ("Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?", "yes_no", None),
        ("Diagnosis", "text", None),
        ("Do you have migraines 15 or more times a month?", "yes_no", None),
        ("Have you tried other medications for this condition?", "yes_no", None),
        ("Medication name", "text", None),
        ("Did it work?", "yes_no", None),
        ("Have you been previously diagnosed with migraine by a health professional?", "yes_no", None),
        ("Is your headache throbbing, pulsating or pounding?", "single_choice", "MIGRAINE_HEADACHE_CHARACTER"),
        ("Where is the head pain located?", "multiple_choice", "MIGRAINE_HEAD_PAIN_LOCATION"),
        ("How often does your headache occur?", "single_choice", "FREQUENCY_STANDARD"),
        ("Do you experience symptoms prior to the migraine?", "multiple_choice", "MIGRAINE_PRIOR_SYMPTOMS"),
        ("Are you currently taking any migraine medication(s)?", "yes_no", None),
        ("Current migraine medication name", "text", None),
        ("Do you have a history of hypertension, stroke, or any type of heart disease?", "yes_no", None),
        ("Disease history types", "multiple_choice", "MIGRAINE_DISEASE_HISTORY_TYPES"),
    ],
    "topical_antifungal": [
        ("Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?", "yes_no", None),
        ("Diagnosis", "text", None),
        ("Have you tried other medications for this condition?", "yes_no", None),
        ("Medication name", "text", None),
        ("Did it work?", "yes_no", None),
        ("Location of lesion", "multiple_choice", "PAIN_LOCATIONS_ALL"),
        ("Size of lesion", "text", None),
    ],
    "cough": [
        ("Do you have a cough?", "yes_no", None),
        ("Is your cough dry (no phlegm)?", "yes_no", None),
        ("How would you rate the severity of your cough?", "single_choice", "COUGH_SEVERITY"),
        ("Is your cough due to an allergy?", "single_choice", "YES_NO_DONT_KNOW"),
        ("Allergy to what?", "text", None),
    ],
    "allergy": [
        ("Do you have any type of allergy (food, drug, environment, dust chemical, hay, animal, insect, material, etc)?", "yes_no", None),
        ("Allergy to", "text", None),
        ("Reaction", "text", None),
        ("What have you tried to alleviate your allergy symptoms?", "multiple_choice", "ALLERGY_RELIEF_METHODS"),
        ("Did antihistamines help?", "yes_no", None),
        ("Did allergy shots help?", "yes_no", None),
        ("Did steroids help?", "yes_no", None),
        ("Other method name", "text", None),
        ("Did other method help?", "yes_no", None),
    ],
    "acid_reflux": [
        ("Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?", "yes_no", None),
        ("Diagnosis", "text", None),
        ("Have you tried other medications for this condition?", "yes_no", None),
        ("Medication name", "text", None),
        ("Did it work?", "yes_no", None),
        ("Do you have heartburn?", "yes_no", None),
        ("On a scale of 1 to 10, rate heartburn severity", "single_choice", "SCALE_1_TO_10"),
        ("How frequently does it occur?", "single_choice", "FREQUENCY_STANDARD"),
        ("Do you have bloating or gassy feelings?", "yes_no", None),
    ],
    "scar_wound_actinic": [
        ("Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?", "yes_no", None),
        ("Diagnosis", "text", None),
        ("Have you tried other medications for this condition?", "yes_no", None),
        ("Medication name", "text", None),
        ("Did it work?", "yes_no", None),
        ("Location of lesion", "multiple_choice", "PAIN_LOCATIONS_ALL"),
        ("Size of lesion", "text", None),
        ("Cause of lesion", "text", None),
    ],
    "dermatitis_eczema_psoriasis": [
        ("Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?", "yes_no", None),
        ("Diagnosis", "text", None),
        ("Have you tried other medications for this condition?", "yes_no", None),
        ("Medication name", "text", None),
        ("Did it work?", "yes_no", None),
        ("Location of lesion", "multiple_choice", "PAIN_LOCATIONS_ALL"),
        ("Size of lesion", "text", None),
    ],
    "diabetes": [
        ("Are you currently living with any of the following conditions?", "single_choice", "DIABETES_CURRENT_CONDITIONS"),
        ("Which type of diabetes?", "single_choice", "DIABETES_TYPE"),
        ("What was your most recent A1c result?", "text", None),
        ("What was the approximate date of your most recent A1c results?", "date", None),
        ("Have you ever been diagnosed with any of the following?", "single_choice", "DIABETES_FURTHER_DIAGNOSED"),
    ],
    "acne": [
        ("Where is the location of your acne?", "multiple_choice", "PAIN_LOCATIONS_ALL"),
        ("How many bumps do you have?", "single_choice", "ACNE_BUMPS_COUNT"),
        ("Has this caused scabbing or scaring?", "single_choice", "YES_NO_UNSPECIFIED"),
        ("Do you clean this location regularly?", "single_choice", "YES_NO_UNSPECIFIED"),
        ("How many of these bumps are full of pus or fluid?", "single_choice", "ACNE_PUS_COUNT"),
        ("What previous methods have you used to treat acne?", "single_choice", "ACNE_PREVIOUS_TREATMENTS"),
    ],
    "laser_therapy_pain": [
        ("Where is the pain located?", "multiple_choice", "LASER_PAIN_LOCATIONS"),
        ("What level of pain are you experiencing?", "single_choice", "LASER_PAIN_LEVEL"),
        ("What prior therapeutic interventions have you tried?", "multiple_choice", "THERAPEUTIC_INTERVENTIONS"),
        ("Other prior therapeutic intervention", "text", None),
        ("Do you have difficulty attempting activities/movements with objects > 5lbs?", "multiple_choice", "DIFFICULTY_MOVEMENTS_GT_5LB"),
        ("Date of accident", "date", None),
        ("What activities/movements make the pain worse?", "text", None),
        ("Have you had, or will have, surgery on the affected area?", "single_choice", "SURGERY_HISTORY"),
        ("Date of surgery if applicable", "text", None),
    ],
    "cold_compression": [
        ("Where is the pain located?", "multiple_choice", "CCT_PAIN_LOCATIONS"),
        ("Orientation", "single_choice", "CCT_ORIENTATION"),
        ("Have you had, or will have, surgery on the affected area?", "single_choice", "SURGERY_HISTORY"),
        ("Date of surgery if applicable", "text", None),
    ],
}


def upsert_choice_set(name: str, choices: List[str]) -> ChoiceSet:
    choice_set, _ = ChoiceSet.objects.get_or_create(name=name)
    for order, text in enumerate(choices, start=1):
        Choice.objects.update_or_create(
            choice_set=choice_set,
            text=text,
            defaults={"order": order},
        )
    return choice_set


def run_seed() -> None:
    with transaction.atomic():
        choice_set_map: Dict[str, ChoiceSet] = {}
        for set_name, options in CHOICE_SETS.items():
            choice_set_map[set_name] = upsert_choice_set(set_name, options)

        condition_map: Dict[str, Condition] = {}
        for item in CONDITIONS:
            condition, _ = Condition.objects.update_or_create(
                code=item["code"], defaults={"name": item["name"]}
            )
            condition_map[item["code"]] = condition

        total_questions = 0
        for condition_code, question_rows in QUESTIONS.items():
            condition = condition_map[condition_code]
            for order, (question_text, question_type, choice_set_name) in enumerate(question_rows, start=1):
                choice_set = choice_set_map.get(choice_set_name) if choice_set_name else None
                required = not question_text.lower().startswith(("other ", "diagnosis", "medication name", "allergy to", "reaction", "date of surgery"))

                ConditionQuestion.objects.update_or_create(
                    condition=condition,
                    order=order,
                    defaults={
                        "question": question_text,
                        "question_type": question_type,
                        "choice_set": choice_set,
                        "required": required,
                    },
                )
                total_questions += 1

    print("Seed complete")
    print(f"ChoiceSets: {ChoiceSet.objects.count()}")
    print(f"Choices: {Choice.objects.count()}")
    print(f"Conditions: {Condition.objects.count()}")
    print(f"ConditionQuestions processed: {total_questions}")


if __name__ == "__main__":
    run_seed()
