import os
import random
import sys

import django
import requests

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "trucare")
sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trucare.settings")
django.setup()

from accounts.models import AccountProfile, DoctorProfile  # noqa: E402
from intake.models import PatientIntake  # noqa: E402
from prescription.models import *  # noqa: E402,F401,F403
from intake.models import PatientCondition  # noqa: E402
from scriptbuilder.models import PrescribeAbleItem  # noqa: E402

DRUG_FIELDS = [
    "item_type", "name", "generic_name", "ndc", "strength", "dosage_form",
    "usual_sig", "quantity", "refills", "duration", "description",
]


def random_prescription_payload(intake, deny_chance=0.1):
    """Body for POST /api/prescription/save/<intake_id>/ (one entry per requested condition)."""
    payload = []
    for pc in PatientCondition.objects.filter(patient=intake, requested=True):
        items = list(PrescribeAbleItem.objects.filter(category=pc.condition, active=True))
        entry = {
            "category_id": pc.condition_id,
            "category_name": pc.condition.name,
            "isDenied": not items or random.random() < deny_chance,
            "denialReason": "",
            "primaryDrug": None,
            "secondaryDrugs": [],
        }
        if entry["isDenied"]:
            entry["denialReason"] = "Randomly denied for testing"
        else:
            primary = random.choice(items)
            others = [i for i in items if i.id != primary.id]
            entry["primaryDrug"] = {f: getattr(primary, f) for f in DRUG_FIELDS}
            entry["secondaryDrugs"] = [str(i.id) for i in random.sample(others, min(len(others), 2))]
        payload.append(entry)
    return payload

intake_objects = PatientIntake.objects.all()
intake_objects = intake_objects.update(status='ALLOCATED_TO_DOCTOR')
intake_objects = PatientIntake.objects.all()

BASE_URL = "http://127.0.0.1:8000"
DEFAULT_PASSWORD = "defaultpassword"  # same default as seed_intakes.py

# intake_objects.update(status='APPROVED_BY_DOCTOR')

access_tokens = {}


def get_access_token(doctor):
    username = doctor.user.username
    print(f"Getting access token for doctor: {username}")
    if username not in access_tokens:
        response = requests.post(
            f"{BASE_URL}/api/auth/login/",
            json={"username": username, "password": DEFAULT_PASSWORD},
        )
        print(response.status_code, response.text, 'login response')
        response.raise_for_status()
        access_tokens[username] = response.json()["access"]
    return access_tokens[username]


for intake in intake_objects:
    doctor = intake.doctor
    if not doctor:
        continue
    try:
        access_token = get_access_token(doctor)
    except Exception as e:
        print(f"Error getting access token for doctor {doctor.user.username}: {e}")
        continue
    intake_id = intake.id
    # doctor_login = requests.post(
    #     f"{BASE_URL}/api/prescription/soap-notes/?intake_id={intake_id}",
    #     headers={"Authorization": f"Bearer {access_token}"},)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = random_prescription_payload(intake)
    # print(f"Payload for intake {intake_id}: {payload}")
    # break
    response = requests.post(f"{BASE_URL}/api/prescription/save/{intake_id}/", json=payload, headers=headers)
    print(intake_id, response.status_code)




