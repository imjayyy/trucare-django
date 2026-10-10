
import pymongo


myclient = pymongo.MongoClient("mongodb://admin:adminASD789@3.139.75.141:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")

mydb = myclient["InteractiveMeds"]
client = mydb["Clients"]
admin = mydb["Admin"]
scripts = mydb["scripts"]
intake = mydb["Intake"]
cordinator = mydb["Cordinator"]
doctor = mydb["Doctor"]
pharma = mydb["Pharmacy"]
drugs = mydb['Drugs']
allocatedpharmacies = mydb['allocatedpharmacies']
prescription = mydb["prescription"]
chats = mydb['chat']
clientFinancial = mydb['clientFinancial']
transaction = mydb['transaction']
biller = mydb['biller']


import os
import sys

import django

# Make the Django project importable and load its settings
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "trucare")
sys.path.insert(0, PROJECT_ROOT)
# Adjust the default to your project's settings module (the folder containing settings.py)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("DJANGO_SETTINGS_MODULE", "trucare.settings"))
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.db import transaction as db_transaction  # noqa: E402
from accounts.models import AccountProfile, DoctorProfile, DoctorLicense, LegacyIdMap  # noqa: E402
from intake.models import states as STATE_CHOICES  # noqa: E402
import datetime  # noqa: E402

STATE_CODES = {name: code for code, name in STATE_CHOICES}
# Mongo has no license expiry; placeholder to satisfy the required field.
DEFAULT_LICENSE_EXPIRATION = datetime.date(2030, 12, 31)

User = get_user_model()
# Import your own models here, e.g.:
# from clients.models import Client
password = "defaultpassword"

@db_transaction.atomic
def seed_clients():
    created_count = 0
    for doc in client.find():
        email = doc.get("Email")
        print("ID", doc.get("clientId"), "Type", doc.get("Type"), "IMS Username", doc.get("IMS Username"))
        if doc.get("IMS Username") is None:
            continue
        # Adjust field mapping to match your Django models
        user, created = User.objects.update_or_create(
            username = doc.get("IMS Username"),
            defaults={
                "username": doc.get("IMS Username"),
                "email": email,
                "first_name": doc.get("First Name", ""),
                "last_name": doc.get("Last Name", ""),
            },
        )
        if doc.get('Type') == "Client":
            account_profile = AccountProfile(id=doc.get("clientId"))
            account_profile.user = user
            account_profile.role = "ORGANIZATION"
            account_profile.id = doc.get("clientId")
            account_profile.save()

        elif doc.get('Type') == None:
            account_profile.user = user
            account_profile.role = "INTAKE_AGENT"
            account_profile.parent_organization = doc.get("clientId")
            account_profile.save()

        if created:
            user.set_password(password)
            user.save()
            created_count += 1
        # Example for a related model:
        # Client.objects.update_or_create(user=user, defaults={"phone": doc.get("phone")})
    print(f"Seeded clients. New users created: {created_count}")



@db_transaction.atomic
def seed_doctors():
    created_count = 0
    for doc in doctor.find():
        username = doc.get("IMS Username")
        if not username:
            continue

        user, created = User.objects.update_or_create(
            username=username,
            defaults={
                "email": doc.get("Email", ""),
                "first_name": (doc.get("First Name") or "").strip(),
                "last_name": (doc.get("Last Name") or "").strip(),
            },
        )
        if created:
            user.set_password(password)
            user.save()
            created_count += 1

        AccountProfile.objects.update_or_create(
            user=user, defaults={"role": AccountProfile.ROLE_DOCTOR}
        )

        profile, _ = DoctorProfile.objects.update_or_create(
            user=user,
            defaults={
                "phone_number": doc.get("Phone") or "",
                "email": doc.get("Email") or "",
                "address": doc.get("Address") or "",
                "state": STATE_CODES.get(doc.get("State"), ""),
                "postal_code": doc.get("Organization Zip") or "",
                "npi": doc.get("NPI") or "",
            },
        )

        # Mongo-side link: Mongo _id -> Django DoctorProfile id
        LegacyIdMap.objects.update_or_create(
            collection="Doctor",
            mongo_id=str(doc["_id"]),
            defaults={"object_id": profile.id},
        )
        doctor.update_one({"_id": doc["_id"]}, {"$set": {"django_doctor_profile_id": profile.id}})

        # licenses[i] pairs with states[i]
        licenses = doc.get("licenses") or []
        lic_states = doc.get("states") or []
        for i, number in enumerate(licenses):
            state_name = lic_states[i] if i < len(lic_states) else None
            code = STATE_CODES.get(state_name)
            if not code:
                print(f"Skipping license {number} for {username}: unknown state {state_name!r}")
                continue
            DoctorLicense.objects.update_or_create(
                doctor=profile,
                license_number=str(number),
                license_state=code,
                defaults={"expiration_date": DEFAULT_LICENSE_EXPIRATION},
            )
    print(f"Seeded doctors. New users created: {created_count}")

def run():
    # seed_clients()
    # seed_doctors()

    from seed_intakes import seed_intakes  # imported late: needs django.setup() above
    seed_intakes(mydb, limit=100)

if __name__ == "__main__":
    run()


