"""
Maps a legacy Mongo `Intake` document onto the new Django intake schema.

Pure functions only (no DB access, no Django imports) so the mapping can be
tested on its own. `seed_intakes.py` consumes `parse_intake()` and does the writes.

Condition answers are described declaratively in QUESTION_RULES:
    condition code -> [(question text, kind, source key, [flag mapping])]
Question texts must match `ConditionQuestion.question` as created by
trucare/seed_patient_form_data.py. Kinds:
    yn      "yes"/"no" string        -> bool | None
    text    free text                -> str | None
    date    date string              -> date | None
    choice  string or list of strings -> list[str]
    flags   several "1" flags        -> list[str] (label taken from the mapping)
"""

import re
from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal

# Legacy "is this condition requested" flag -> Condition.code
CONDITION_REQUEST_FIELDS = {
    "member[pain_condition_request]": "pain_request",
    "member[muscle_condition_request]": "muscle_relaxer",
    "member[dermatitis_condition_request]": "dermatitis_eczema_psoriasis",
    "member[scar_condition_request]": "scar_wound_actinic",
    "member[acid_reflux_condition_request]": "acid_reflux",
    "member[allergy_condition_request]": "allergy",
    "member[cough_condition_request]": "cough",
    "member[topical_anti_fungal_condition_request]": "topical_antifungal",
    "member[migraine_condition_request]": "migraine_headache",
    "member[foot_bath_condition_request]": "foot_bath",
    "member[cold_sores_condition_request]": "cold_sores",
    "member[oral_condition_request]": "oral_nsaids",
    "member[acne_condition_request]": "acne",
    "member[diabetes_condition_request]": "diabetes",
    "member[laser_therapy_pain_treatment_request]": "laser_therapy_pain",
    "member[coldcompression_therapy_request]": "cold_compression",
}

# Legacy status text -> PatientIntake.status. Unknown values are upper-snake-cased.
STATUS_MAP = {
    "pending": "PENDING",
    "claimed": "CLAIMED",
    "assigned to doctor": "ASSIGNED_TO_DOCTOR",
    "approved by doctor": "APPROVED_BY_DOCTOR",
    "allocated": "ALLOCATED_TO_PHARMACY",
    "delivered": "DELIVERED",
    "provider decline": "PROVIDER_DECLINE",
    "patient decline": "PATIENT_DECLINE",
    "cant connect": "CANT_CONNECT",
    "transfer unsuccessful": "TRANSFER_UNSUCCESSFUL",
    "patient not interested": "PATIENT_NOT_INTERESTED",
    "invalid insurance": "INVALID_INSURANCE",
    "": "N/A",
}

BILLING_MAP = {
    "billed": "BILLED",
    "paper billed": "PAPER_BILLED",
    "unbillable": "UNBILLABLE",
    "pending": "PENDING",
}

# Legacy family_history[...] key -> PatientFamilyHistory field (anxiety has no new field)
FAMILY_HISTORY_FIELDS = {
    "asthma": "asthama",
    "bleeding_tendency": "bleeding_tendency",
    "cancer": "cancer",
    "colitis": "colitis",
    "depression": "depression",
    "diabetes": "diabetes",
    "epilepsy": "epilepsy",
    "heart_attack": "heart_attack",
    "high_blood_pressure": "high_blood_pressure",
    "kidney_disease": "kidney_disease",
    "leukemia": "leukemia",
    "migraine": "migraine",
    "schizophrenia": "schizophrenia",
    "stomach_ulcers": "stomach_ulcers",
    "stroke": "stroke",
    "suicide": "suicide",
    "tuberculosis": "tuberculosis",
}

# Flag suffix -> label in the THERAPEUTIC_INTERVENTIONS choice set
THERAPEUTIC_FLAGS = {
    "rest": "Rest",
    "exercise": "Exercise",
    "PT": "PT",
    "injections": "injections",
    "anti-inflammatories": "anti-inflammatories",
    "corticosteroids": "corticosteroids",
    "NSAIDs": "NSAIDs",
    "steroids": "steroids",
    "opioids": "opioids",
    "oxycodone": "oxycodone",
    "non-prescription": "non-prescription medications",
    "prescription": "prescription medications",
    "muscle": "muscle relaxants",
    "other": "Other",
}

MIGRAINE_LOCATION_FLAGS = {
    "left": "Left",
    "right": "Right",
    "both": "Both Sides",
    "front": "Front",
    "back": "Back",
}
MIGRAINE_SYMPTOM_FLAGS = {
    "light": "Light Sensitivity",
    "visual": "Visual Symptoms",
    "dizziness": "Dizziness",
    "nausea": "Nausea",
    "vomiting": "Vomiting",
}
MIGRAINE_HISTORY_FLAGS = {"hypertension": "Hypertension", "stroke": "Stroke"}
ALLERGY_RELIEF_FLAGS = {
    "antihistamines": "Antihistamines",
    "allergy__shots": "allergy shots",
    "steroids": "Steroids",
    "other": "Other",
    "none": "None",
}


def M(key):
    return f"member[{key}]"


CONSULT = "Have you consulted other medical professionals for your problem? If yes, what was the diagnosis?"
TRIED_OTHER = "Have you tried other medications for this condition?"


def _medication_block(consult, diagnosis, other, name, work):
    return [
        (CONSULT, "yn", M(consult)),
        ("Diagnosis", "text", M(diagnosis)),
        (TRIED_OTHER, "yn", M(other)),
        ("Medication name", "text", M(name)),
        ("Did it work?", "yn", M(work)),
    ]


QUESTION_RULES = {
    "pain_request": [
        (CONSULT, "yn", M("medical__professional__consult")),
        ("Diagnosis", "text", M("medical__professional__diagnosis")),
        (TRIED_OTHER, "yn", M("medical__professional__medications")),
        ("Medications", "text", M("medical__professional__medications__what__from")),
        ("Have you ever used Lidocaine for pain?", "yn", M("lidocaine__for__pain")),
        ("For what pain", "text", M("lidocaine__for__pain__what__from")),
        ("What type of pain are you experiencing?", "choice", "pain__experienced"),
        ("On a scale of 1 to 10, rate severity of your pain", "choice", "severity__of__pain"),
        ("Where is the pain located?", "choice", M("pain__located")),
        ("How long have you had this problem (days, weeks, months etc.)?", "text", M("pain__time")),
        ("How often do you experience the symptoms?", "choice", "symptoms__experienced__threshold"),
        ("How are your symptoms changing with time?", "choice", "symptoms__experienced__changing"),
        ("How do you think your problem began?", "text", M("beginning__of__problem")),
        ("What activities make the pain worse?", "text", M("activities__affecting__the__problem")),
        ("What activities reduce the pain?", "text", M("activties__reducing__the__pain")),
        ("What prior therapeutic interventions have you tried?", "flags", "tried__therapeutic__", THERAPEUTIC_FLAGS),
        ("Other prior therapeutic intervention", "text", M("other__tried__therapeutic__input")),
        ("Which therapeutic interventions afforded improvement of symptoms?", "flags", "afforded__therapeutic__", THERAPEUTIC_FLAGS),
        ("Other intervention that afforded improvement", "text", M("other__afforded__therapeutic__input")),
        ("Do you have a history of seizures, heart arrhythmias, or pacemaker use?", "yn", M("patient__history")),
    ],
    "muscle_relaxer": [
        ("Do you have muscle spasms?", "yn", M("muscle__spasms")),
        ("Location of muscle spasms", "choice", M("muscle__spasms__part")),
        ("Do you have any cramping or tightening in any muscle?", "yn", M("muscle__cramping")),
        ("Location of cramping/tightening", "choice", M("muscle__cramping__part")),
    ],
    "oral_nsaids": [
        ("What areas are affected by muscle or joint inflammation?", "choice", "oral__affected__area__inflamation"),
        ("How long have you experienced inflammation?", "text", M("oral__experienced__inflammation")),
        ("Past inflammation treatments", "flags", "past__inflammation_treatment__", THERAPEUTIC_FLAGS),
        ("Other past inflammation treatment", "text", M("other__past__inflammation_treatment__input")),
    ],
    "cold_sores": [
        ("Do you currently have blisters?", "yn", M("isBlisters")),
        ("Location of blisters", "choice", M("location__of__blisters")),
        *_medication_block(
            "medical__professional__cold__sores__consult",
            "medical__professional__cold__sores__diagnosis",
            "cold__sores__other__medications",
            "cold__sores__medication__name",
            "cold__sores__medication__work",
        ),
        ("Have you had previous cold sore episodes?", "yn", M("previous__cold__sores__episodes")),
        ("Were the previous episodes similar to the current episode?", "yn", "severity__of__previos__cold__sores__episode"),
        ("Do you concurrently have eye symptoms, ear symptoms, or severe headaches?", "yn", M("cold__sore__symptoms")),
    ],
    "foot_bath": [
        *_medication_block(
            "medical__professional__foot__bath__consult",
            "medical__professional__foot__bath__diagnosis",
            "foot__bath__other__medications",
            "foot__bath__medication__name",
            "foot__bath__medication__work",
        ),
        ("Location of lesion", "choice", M("foot__bath__location__of__lession")),
        ("Size of lesion", "text", M("foot__bath__size__of__lession")),
    ],
    "migraine_headache": [
        (CONSULT, "yn", M("medical__professional__migraine__consult")),
        ("Diagnosis", "text", M("medical__professional__migraine__diagnosis")),
        ("Do you have migraines 15 or more times a month?", "yn", M("medical__professional__migraine__times_a_month")),
        (TRIED_OTHER, "yn", M("migraine__other__medications")),
        ("Medication name", "text", M("migraine__medication__name")),
        ("Did it work?", "yn", M("migraine__medication__work")),
        ("Have you been previously diagnosed with migraine by a health professional?", "yn", M("diagnosed__with__migraine")),
        ("Is your headache throbbing, pulsating or pounding?", "choice", "migraine__heart__condition"),
        ("Where is the head pain located?", "flags", "migraine__head__pain__", MIGRAINE_LOCATION_FLAGS),
        ("How often does your headache occur?", "choice", "migraine__head__pain__frequency"),
        ("Do you experience symptoms prior to the migraine?", "flags", "migraine__symptoms__", MIGRAINE_SYMPTOM_FLAGS),
        ("Are you currently taking any migraine medication(s)?", "yn", M("migraine__medications__intake")),
        ("Current migraine medication name", "text", M("migraine_current_medication__name")),
        ("Do you have a history of hypertension, stroke, or any type of heart disease?", "yn", M("migraine__disease__history")),
        ("Disease history types", "flags", "migraine__history__", MIGRAINE_HISTORY_FLAGS),
    ],
    "topical_antifungal": [
        *_medication_block(
            "medical__professional__fungal__consult",
            "medical__professional__fungal__diagnosis",
            "fungal__other__medications",
            "fungal__medication__name",
            "fungal__medication__work",
        ),
        ("Location of lesion", "choice", M("fungal__location__of__lession")),
        ("Size of lesion", "text", M("fungal__size__of__lession")),
    ],
    "cough": [
        ("Do you have a cough?", "yn", M("isCough")),
        ("Is your cough dry (no phlegm)?", "yn", M("isCough__dry")),
        ("How would you rate the severity of your cough?", "choice", M("cough__severity")),
        ("Is your cough due to an allergy?", "choice", M("cough__allergy")),
        ("Allergy to what?", "text", M("cough__allergy__name")),
    ],
    "allergy": [
        ("Do you have any type of allergy (food, drug, environment, dust chemical, hay, animal, insect, material, etc)?", "yn", M("isAllergy")),
        ("Allergy to", "text", M("allergy__to__input")),
        ("Reaction", "text", M("allergy__reaction__to")),
        ("What have you tried to alleviate your allergy symptoms?", "flags", "tried__allergy__symptoms__", ALLERGY_RELIEF_FLAGS),
        ("Other method name", "text", "tried__other__name"),
    ],
    "acid_reflux": [
        *_medication_block(
            "medical__professional__acid__reflux__consult",
            "medical__professional__acid__reflux__diagnosis",
            "acid__reflux__other__medications",
            "acid__reflux__medication__name",
            "acid__reflux__medication__work",
        ),
        ("Do you have heartburn?", "yn", M("isAcidHeartBurn")),
        ("On a scale of 1 to 10, rate heartburn severity", "choice", "heart__burn__severity"),
        ("How frequently does it occur?", "choice", "acid__reflux__frequency"),
        ("Do you have bloating or gassy feelings?", "yn", M("acid__reflux__isBloating")),
    ],
    "scar_wound_actinic": [
        *_medication_block(
            "medical__professional__scar__consult",
            "medical__professional__scar__diagnosis",
            "scar__other__medications",
            "scar__medication__name",
            "scar__medication__work",
        ),
        ("Location of lesion", "choice", M("location__of__lession")),
        ("Size of lesion", "text", M("size__of__lession")),
        ("Cause of lesion", "text", M("cause__of__lession")),
    ],
    "dermatitis_eczema_psoriasis": [
        *_medication_block(
            "medical__professional__psoriasis__consult",
            "medical__professional__psoriasis__diagnosis",
            "psoriasis__other__medications",
            "psoriasis__medication__name",
            "psoriasis__medication__work",
        ),
        ("Location of lesion", "choice", M("psoriasis__location__of__lession")),
        ("Size of lesion", "text", M("psoriasis__size__of__lession")),
    ],
    "diabetes": [
        ("Are you currently living with any of the following conditions?", "choice", "diabetes__conditions"),
        ("Which type of diabetes?", "choice", "diabetes__type"),
        ("What was your most recent A1c result?", "text", "diabetes__a1c__result"),
        ("What was the approximate date of your most recent A1c results?", "date", "diabetes__a1c__result__test__date"),
        ("Have you ever been diagnosed with any of the following?", "choice", "diabetes__further__diagnosed"),
    ],
    "acne": [
        ("Where is the location of your acne?", "choice", "acne__location"),
        ("How many bumps do you have?", "choice", "acne__bumps"),
        ("Has this caused scabbing or scaring?", "choice", "acne__scabbing"),
        ("Do you clean this location regularly?", "choice", "acne__regular__cleaning"),
        ("How many of these bumps are full of pus or fluid?", "choice", "acne__bumps__pus"),
        ("What previous methods have you used to treat acne?", "choice", "acne__previous__treatment"),
    ],
    "laser_therapy_pain": [
        ("Where is the pain located?", "choice", "laser__thereapy__pain__location"),
        ("What level of pain are you experiencing?", "choice", "laser__therapy__pain__level"),
        ("What prior therapeutic interventions have you tried?", "flags", "laser__therapeutic__", THERAPEUTIC_FLAGS),
        ("Other prior therapeutic intervention", "text", M("other__laser__therapeutic__input")),
        ("Do you have difficulty attempting activities/movements with objects > 5lbs?", "choice", "laser__therapy__pain__difficulty__movements"),
        ("Date of accident", "date", "laser__therapy__accident__date"),
        ("What activities/movements make the pain worse?", "text", "laser__therapy__pain__increasing__actvities"),
        ("Have you had, or will have, surgery on the affected area?", "choice", "laser__therapy__surgery__history"),
        ("Date of surgery if applicable", "text", "laser__therapy__date__of__surgery"),
    ],
    "cold_compression": [
        ("Where is the pain located?", "choice", "cold__compression__pain__location"),
        ("Orientation", "choice", "cold__compression__therapy__orientation"),
        ("Have you had, or will have, surgery on the affected area?", "choice", "cold__compression__therapy__surgery__history"),
        ("Date of surgery if applicable", "text", "cct__date__of__surgery"),
    ],
}


# ---------------------------------------------------------------- value helpers

_EMPTY = {"", "none", "n/a", "na", "null"}


def s(value):
    """Whitespace-collapsed string, or None when empty."""
    if value is None:
        return None
    text = " ".join(str(value).split())
    return text or None


def clean(value):
    """Like s() but also treats 'None' / 'N/A' placeholders as empty."""
    text = s(value)
    return None if text is None or text.lower() in _EMPTY else text


def yn(value):
    text = (s(value) or "").lower()
    if text in ("yes", "y", "true", "1"):
        return True
    if text in ("no", "n", "false", "0"):
        return False
    return None


def parse_date(value):
    text = re.sub(r"\s+", "", s(value) or "")
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%m/%d/%y"):
        try:
            parsed = datetime.strptime(text[:10] if fmt == "%Y-%m-%d" else text, fmt).date()
        except ValueError:
            continue
        return parsed if parsed.year >= 1900 else None
    return None


def digits(value, limit):
    return re.sub(r"\D", "", str(value or ""))[:limit] or None


def height_inches(value):
    """5'7\" -> 67, 6' -> 72, '70' -> 70."""
    text = s(value)
    if not text:
        return None
    match = re.match(r"^(\d+)\s*(?:'|ft|feet|’)\s*(?:(\d+(?:\.\d+)?))?", text, re.I)
    if match:
        return Decimal(int(match.group(1)) * 12) + Decimal(match.group(2) or 0)
    match = re.match(r"^\d+(?:\.\d+)?$", text)
    return Decimal(text) if match else None


def weight_lbs(value):
    match = re.search(r"\d+(?:\.\d+)?", s(value) or "")
    return Decimal(match.group()) if match else None


def as_list(value):
    if isinstance(value, (list, tuple)):
        return [t for t in (s(v) for v in value) if t]
    text = s(value)
    return [text] if text else []


def _flags(doc, prefix, mapping):
    return [label for suffix, label in mapping.items() if doc.get(prefix + suffix) not in (None, "", "0", 0, False)]


def extract_answer(doc, rule):
    kind, source = rule[1], rule[2]
    if kind == "yn":
        return yn(doc.get(source))
    if kind == "text":
        return s(doc.get(source))
    if kind == "date":
        return parse_date(doc.get(source))
    if kind == "choice":
        return as_list(doc.get(source))
    if kind == "flags":
        return _flags(doc, source, rule[3])
    raise ValueError(f"Unknown rule kind: {kind}")


# ------------------------------------------------------------- section mappers

def _requested_conditions(doc):
    return [code for key, code in CONDITION_REQUEST_FIELDS.items() if yn(doc.get(key))]


def _patient(doc, state_codes):
    state = s(doc.get("State"))
    return {
        "first_name": (s(doc.get("First Name")) or "Unknown")[:30],
        "last_name": (s(doc.get("Last Name")) or "Unknown")[:30],
        "date_of_birth": parse_date(doc.get("Date of birth")) or date(1900, 1, 1),
        "email": (s(doc.get("Email")) or "").lower() or None,
        "phone_number": digits(doc.get("Phone"), 15),
        "address": ", ".join(p for p in (s(doc.get("Address")), s(doc.get("City")), s(doc.get("Zip"))) if p) or None,
        "state": state_codes.get(state, state if state and len(state) == 2 else None),
    }


def _insurance(doc):
    kind = (s(doc.get("Insurance type")) or "").lower()
    if "workmen" in kind:
        return {
            "insurance_type": "WC",
            "primary_insured": bool(yn(doc.get("Primary Insured"))),
            "payer_name": s(doc.get("Payer Name")),
            "claim_number": s(doc.get("Claim Number")),
            "date_of_injury": parse_date(doc.get("Date of Injury")),
            "adjuster_name": s(doc.get("Adjuster Name")),
            "adjuster_phone": digits(doc.get("Adjuster Number"), 15),
            "employer_name": s(doc.get("Employers Name")),
        }
    if "pip" in kind:
        return {
            "insurance_type": "PIP",
            "primary_insured": bool(yn(doc.get("PIP Primary Insured"))),
            "insurance_carrier": s(doc.get("PIP Insurance carrier")),
            "carrier_phone": digits(doc.get("Carrier Phone"), 15),
            "adjuster_name": s(doc.get("PIP Adjuster name")),
            "adjuster_phone": digits(doc.get("PIP Adjuster phone number"), 15),
            "policy_number": s(doc.get("PIP Policy number")),
            "claim_number": s(doc.get("PIP Claim number")),
            "date_of_accident": parse_date(doc.get("Date of accident")),
        }
    if "rx" in kind:
        return {
            "insurance_type": "RX",
            "primary_insured": bool(yn(doc.get("Primary Insured"))),
            "insurance_carrier": s(doc.get("Insurance carrier")),
            "carrier_phone": digits(doc.get("Carrier Phone"), 15),
            "group_id": s(doc.get("Group ID")),
            "patient_id_rx": s(doc.get("Patient ID")),
            "bin": s(doc.get("BIN")),
            "pcn": s(doc.get("PCN")),
        }
    return None


def _family_history(doc):
    result = {}
    for legacy_key, field in FAMILY_HISTORY_FIELDS.items():
        value = (s(doc.get(f"family_history[{legacy_key}]")) or "").upper()
        result[field] = "Yes" if value == "YES" else "None" if value in ("NO", "NONE") else "Unknown"
    return result


_HEALTH_KEY = re.compile(r"^health_record\[(\w+)\]\[(\d+)\]\[(\w+)\]$")


def _health_groups(doc):
    groups = defaultdict(lambda: defaultdict(dict))
    for key, value in doc.items():
        match = _HEALTH_KEY.match(key)
        if match:
            groups[match.group(1)][int(match.group(2))][match.group(3)] = value
    return {name: [rows[i] for i in sorted(rows)] for name, rows in groups.items()}


def _health_and_medical_history(doc):
    groups = _health_groups(doc)
    records, history = [], []

    for row in groups.get("medical_condition", []):
        name = clean(row.get("name"))
        if name:
            history.append({"condition": name[:100], "diagnosis_date": None, "notes": clean(row.get("comments"))})

    seen = set()
    for section in ("allergies", "patient_allergies"):
        for row in groups.get(section, []):
            name, reaction = clean(row.get("name")), clean(row.get("reaction"))
            if name and (name.lower(), reaction) not in seen:
                seen.add((name.lower(), reaction))
                records.append({
                    "record_type": "Allergies",
                    "record_date": None,
                    "description": f"{name} (reaction: {reaction})" if reaction else name,
                })

    for row in groups.get("surgeries", []):
        name = clean(row.get("name"))
        if name:
            comments = clean(row.get("comments"))
            records.append({
                "record_type": "Surgeries",
                "record_date": parse_date(row.get("date_started")),
                "description": f"{name} ({comments})" if comments else name,
            })

    for row in groups.get("medications", []):
        name = clean(row.get("name"))
        if name:
            records.append({"record_type": "Medications", "record_date": None, "description": name})

    lifestyle = [
        f"{label}: {value}"
        for label, key in (("Smoking", "do_you_smoke"), ("Alcohol", "do_you_drink"), ("Exercise", "do_you_exercise"))
        if (value := s(doc.get(f"lifestyle_info[{key}]")))
    ]
    if lifestyle:
        records.append({"record_type": "Other", "record_date": None, "description": "Lifestyle - " + "; ".join(lifestyle)})
    for n in (1, 2, 3):
        extra = clean(doc.get(f"additional_info[miscellaneos{n}]"))
        if extra:
            records.append({"record_type": "Other", "record_date": None, "description": extra})

    return records, history


def _slug_status(value):
    text = (s(value) or "").lower()
    return STATUS_MAP.get(text) or re.sub(r"\W+", "_", text).strip("_").upper()


def _internal_notes(doc):
    parts = [clean(doc.get("notes")), f"Reason: {clean(doc.get('reason'))}" if clean(doc.get("reason")) else None]
    return " | ".join(p for p in parts if p)[:255] or None


# ------------------------------------------------------------------- entrypoint

def parse_intake(doc, state_codes):
    """Convert one legacy Intake document into plain data for the Django models."""
    conditions = _requested_conditions(doc)
    answers = [
        (code, rule[0], extract_answer(doc, rule))
        for code in conditions
        for rule in QUESTION_RULES.get(code, [])
    ]
    health_records, medical_history = _health_and_medical_history(doc)
    billing = (s(doc.get("billing_status")) or "").lower()
    soap = {name: s(doc.get(legacy)) or "" for name, legacy in (
        ("subjective", "Subjective"), ("objective", "Objective"), ("assessment", "Assessment"), ("plan", "Plan"),
    )}

    return {
        "patient": _patient(doc, state_codes),
        "intake": {
            "height": height_inches(doc.get("Height")),
            "weight": weight_lbs(doc.get("Weight")),
            "status": _slug_status(doc.get("Status")),
            "billing_status": BILLING_MAP.get(billing) or (re.sub(r"\W+", "_", billing).upper() or None),
            "internal_notes": _internal_notes(doc),
            "created_at": doc.get("Date"),
            "updated_at": doc.get("StatusDate") or doc.get("Date"),
        },
        "insurance": _insurance(doc),
        "family_history": _family_history(doc),
        "health_records": health_records,
        "medical_history": medical_history,
        "conditions": conditions,
        "answers": answers,
        "soap": soap if any(soap.values()) else None,
        "legacy": {
            "patient_id": s(doc.get("PatientID")),
            "client_id": s(doc.get("ClientID")),
            "agent_name": s(doc.get("AgentName")),
            "coordinator_id": s(doc.get("cordinatorID")),
            "doctor_id": s(doc.get("doctorID")),
            "pharmacy_id": s(doc.get("PharmacyID")),
            "script_name": s(doc.get("scriptname")),
        },
    }
