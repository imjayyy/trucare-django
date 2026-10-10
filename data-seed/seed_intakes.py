"""
Imports the latest legacy Mongo intakes into the Django schema.

Needs Django to be set up already (database-connection.py does this before calling
`seed_intakes`). Field-level mapping lives in legacy_intake_mapper.py.

Legacy -> Django links are stored two-way in accounts.LegacyIdMap:
    Doctor     Mongo _id        -> DoctorProfile.id
    Cordinator Mongo _id        -> User.id
    Pharmacy   Mongo _id        -> AccountProfile.id
    Patient    legacy PatientID -> PatientInfo.id
    Intake     Mongo _id        -> PatientIntake.id
Clients need no map: AccountProfile.id == legacy clientId.
"""

import collections
import datetime
import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from accounts.models import AccountProfile, DoctorProfile, LegacyIdMap, PharmacyProfile
from intake.models import (
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
    states,
)
from prescription.models import Soap_notes
from scriptbuilder.models import Script, ScriptIntakeRelationship

from legacy_intake_mapper import QUESTION_RULES, parse_intake, yn

User = get_user_model()
DEFAULT_PASSWORD = "defaultpassword"  # same default as database-connection.py
STATE_CODES = {name: code for code, name in states}


def _norm(text):
    """Case/underscore/apostrophe-insensitive key: 'getting__worse' == 'Getting worse'."""
    text = str(text).replace("_", " ").replace("'", "")
    return " ".join(text.split()).lower()


def _link(collection, mongo_id, object_id):
    LegacyIdMap.objects.update_or_create(
        collection=collection, mongo_id=str(mongo_id), defaults={"object_id": object_id}
    )


def _lookup(collection, mongo_id):
    row = LegacyIdMap.objects.filter(collection=collection, mongo_id=str(mongo_id)).first()
    return row.object_id if row else None


def _ensure_user(username, first_name="", last_name="", email=""):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"first_name": first_name[:150], "last_name": last_name[:150], "email": email or ""},
    )
    if created:
        user.set_password(DEFAULT_PASSWORD)
        user.save()
    return user


class LegacyResolver:
    """Resolves legacy client / agent / coordinator / pharmacy / doctor references."""

    def __init__(self, mongo_db):
        self.people = {}
        for doc in mongo_db["Clients"].find():
            name = _norm(f"{doc.get('First Name', '')} {doc.get('Last Name', '')}")
            if doc.get("IMS Username") and name:
                self.people.setdefault((str(doc.get("clientId")), name), doc)
        self.coordinators = {str(d["_id"]): d for d in mongo_db["Cordinator"].find()}
        self.pharmacies = {str(d["_id"]): d for d in mongo_db["Pharmacy"].find()}

    def client(self, client_id):
        if not client_id or not client_id.isdigit():
            return None
        profile = AccountProfile.objects.select_related("user").filter(
            id=int(client_id), role=AccountProfile.ROLE_ORGANIZATION
        ).first()
        return profile.user if profile else None

    def agent(self, client_id, agent_name, client_user):
        doc = self.people.get((client_id, _norm(agent_name or "")))
        user = User.objects.filter(username=doc["IMS Username"]).first() if doc else None
        if user is None:
            return None
        if client_user and user != client_user:
            AccountProfile.objects.get_or_create(
                user=user,
                defaults={"role": AccountProfile.ROLE_INTAKE_AGENT, "parent_organization": client_user},
            )
        return user

    def coordinator(self, mongo_id):
        doc = self.coordinators.get(mongo_id or "")
        if not doc or not doc.get("IMS Username"):
            return None
        user = _ensure_user(doc["IMS Username"], doc.get("First Name", ""), doc.get("Last Name", ""), doc.get("Email", ""))
        AccountProfile.objects.get_or_create(user=user, defaults={"role": AccountProfile.ROLE_MANAGER})
        _link("Cordinator", mongo_id, user.id)
        return user

    def pharmacy(self, mongo_id):
        doc = self.pharmacies.get(mongo_id or "")
        if not doc or not doc.get("IMS Username"):
            return None
        user = _ensure_user(doc["IMS Username"], doc.get("Pharmacy Name", ""), "", doc.get("Email", ""))
        profile, _ = AccountProfile.objects.get_or_create(user=user, defaults={"role": AccountProfile.ROLE_PHARMACY})
        PharmacyProfile.objects.get_or_create(
            user=user,
            defaults={"phone_number": re.sub(r"\D", "", doc.get("Phone", ""))[:20], "email": doc.get("Email", "")},
        )
        _link("Pharmacy", mongo_id, profile.id)
        return profile

    def doctor(self, mongo_id):
        profile_id = _lookup("Doctor", mongo_id) if mongo_id else None
        return DoctorProfile.objects.filter(id=profile_id).first() if profile_id else None


class AnswerWriter:
    """Writes mapped values into PatientAnswer / PatientAnswerChoice."""

    def __init__(self):
        self.questions = {(q.condition.code, q.question): q for q in ConditionQuestion.objects.select_related("condition")}
        self.conditions = {c.code: c for c in Condition.objects.all()}
        self._choices = {}
        self.unmatched = collections.Counter()

    def missing_questions(self):
        return [(code, rule[0]) for code, rules in QUESTION_RULES.items() for rule in rules if (code, rule[0]) not in self.questions]

    def _choice(self, question, value):
        if question.choice_set_id not in self._choices:
            self._choices[question.choice_set_id] = {
                _norm(c.text): c for c in Choice.objects.filter(choice_set_id=question.choice_set_id)
            }
        return self._choices[question.choice_set_id].get(_norm(value))

    def write(self, intake, code, question_text, value):
        question = self.questions.get((code, question_text))
        if question is None or value in (None, "", []):
            return
        kind = question.question_type
        answer = PatientAnswer(patient=intake, question=question)

        if kind == ConditionQuestion.YES_NO:
            flag = value if isinstance(value, bool) else yn(value[0] if isinstance(value, list) else value)
            if flag is None:
                return
            answer.boolean_answer = flag
            answer.text_answer = "Yes" if flag else "No"
            answer.save()
        elif kind == ConditionQuestion.DATE:
            if not isinstance(value, datetime.date):
                return
            answer.date_answer = value
            answer.save()
        elif kind in (ConditionQuestion.SINGLE_CHOICE, ConditionQuestion.MULTIPLE_CHOICE):
            values = value if isinstance(value, list) else [str(value)]
            if kind == ConditionQuestion.SINGLE_CHOICE:
                values = values[:1]
            matched = []
            for item in values:
                choice = self._choice(question, item)
                if choice:
                    matched.append(choice)
                else:
                    self.unmatched[(code, question_text, item)] += 1
            if kind == ConditionQuestion.SINGLE_CHOICE:
                # Single-choice answers are read from text_answer by the PDF/SOAP builders.
                answer.text_answer = matched[0].text if matched else values[0]
            elif not matched:
                return
            answer.save()
            for choice in matched:
                PatientAnswerChoice.objects.get_or_create(answer=answer, choice=choice)
        else:
            if isinstance(value, list):
                value = ", ".join(value)
            answer.text_answer = str(value)
            answer.save()


def _aware(value):
    return timezone.make_aware(value, datetime.timezone.utc) if value and timezone.is_naive(value) else value


def _get_or_create_patient(data, legacy, legacy_intake_id):
    key = legacy["patient_id"] or legacy_intake_id
    existing_id = _lookup("Patient", key)
    if existing_id:
        return PatientInfo.objects.get(id=existing_id), False

    fields = dict(data["patient"])
    if not fields["email"] or PatientInfo.objects.filter(email__iexact=fields["email"]).exists():
        fields["email"] = f"legacy-{key}@legacy.invalid"
    patient = PatientInfo.objects.create(**fields)
    _link("Patient", key, patient.id)
    return patient, True


def _write_patient_level_data(patient, data, stats):
    if data["insurance"]:
        insurance = Insurance(patient=patient, **data["insurance"])
        try:
            insurance.save()
        except ValidationError:
            # Legacy data often lacks fields the new model requires; keep the row anyway.
            Insurance.objects.bulk_create([insurance])
            stats["insurance_incomplete"] += 1
    PatientFamilyHistory.objects.create(patient=patient, **data["family_history"])
    HealthRecord.objects.bulk_create([HealthRecord(patient=patient, **row) for row in data["health_records"]])
    MedicalHistory.objects.bulk_create([MedicalHistory(patient=patient, **row) for row in data["medical_history"]])


def _import_one(doc, resolver, writer, stats):
    legacy_id = str(doc["_id"])
    if _lookup("Intake", legacy_id):
        stats["skipped_existing"] += 1
        return

    data = parse_intake(doc, STATE_CODES)
    legacy = data["legacy"]

    patient, is_new_patient = _get_or_create_patient(data, legacy, legacy_id)
    if is_new_patient:
        _write_patient_level_data(patient, data, stats)

    client = resolver.client(legacy["client_id"])
    agent = resolver.agent(legacy["client_id"], legacy["agent_name"], client)
    coordinator = resolver.coordinator(legacy["coordinator_id"])
    pharmacy = resolver.pharmacy(legacy["pharmacy_id"])
    doctor = resolver.doctor(legacy["doctor_id"])
    for label, found, ref in (
        ("client", client, legacy["client_id"]),
        ("agent", agent, legacy["agent_name"]),
        ("coordinator", coordinator, legacy["coordinator_id"]),
        ("doctor", doctor, legacy["doctor_id"]),
    ):
        if ref and not found:
            stats[f"unresolved_{label}"] += 1

    fields = data["intake"]
    intake = PatientIntake.objects.create(
        patient=patient,
        height=fields["height"],
        weight=fields["weight"],
        client=client,
        intake_agent=agent,
        cordinator=coordinator,
        doctor=doctor,
        allocated_pharmacy=pharmacy,
        status=fields["status"],
        billing_status=fields["billing_status"],
        internal_notes=fields["internal_notes"],
    )
    # created_at/updated_at are auto fields; restore the legacy timestamps.
    PatientIntake.objects.filter(pk=intake.pk).update(
        created_at=_aware(fields["created_at"]), updated_at=_aware(fields["updated_at"])
    )
    if is_new_patient:
        PatientInfo.objects.filter(pk=patient.pk).update(created_at=_aware(fields["created_at"]))
    _link("Intake", legacy_id, intake.id)

    for code in data["conditions"]:
        PatientCondition.objects.create(patient=intake, condition=writer.conditions[code], requested=True)
    for code, question_text, value in data["answers"]:
        writer.write(intake, code, question_text, value)

    if data["soap"]:
        Soap_notes.objects.update_or_create(patient_intake=intake, defaults=data["soap"])

    script = Script.objects.filter(name__iexact=legacy["script_name"] or "").first()
    if script:
        ScriptIntakeRelationship.objects.get_or_create(script=script, intake=intake)

    stats["imported"] += 1


def seed_intakes(mongo_db, limit=100):
    """Import the `limit` most recent legacy intakes (oldest first so new ids follow legacy order)."""
    resolver = LegacyResolver(mongo_db)
    writer = AnswerWriter()
    stats = collections.Counter()

    missing = writer.missing_questions()
    if missing:
        print(f"WARNING: {len(missing)} mapped questions not found in the DB (run seed_patient_form_data.py):")
        for code, text in missing:
            print(f"  {code}: {text}")

    docs = list(mongo_db["Intake"].find().sort("Date", -1).limit(limit))[::-1]
    for doc in docs:
        try:
            with transaction.atomic():
                _import_one(doc, resolver, writer, stats)
        except Exception as exc:  # keep going; one bad document should not stop the batch
            stats["failed"] += 1
            print(f"FAILED intake {doc['_id']} (patient {doc.get('PatientID')}): {exc!r}")

    print(f"Seeded intakes: {dict(stats)}")
    for (code, question, value), count in writer.unmatched.most_common(20):
        print(f"  unmatched choice x{count}: [{code}] {question!r} -> {value!r}")
