"""
Seed script for ICD code mappings on Condition and Choice records.

Run from /Telemed-Django/trucare:
    python seed_condition_choice_icd_codes.py

or:
    python manage.py shell < seed_condition_choice_icd_codes.py
"""

import os
import re
from typing import Dict, Iterable, List, Tuple, Union

import django
from django.db import transaction


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trucare.settings")
django.setup()

from intake.models import Choice, Condition  # noqa: E402


CodeValue = Union[str, List[str], Tuple[str, ...]]


# Pain Condition Request
pain_condition_codes = {
    "default_code": "M06.4",
    "locations": {
        "Face": "G50.1",
        "Head": "M06.4",
        "Neck": "M54.2",
        "Right Shoulder": "M25.511",
        "Left Shoulder": "M25.512",
        "Right Arm": "M79.601",
        "Left Arm": "M79.602",
        "Right elbow": "M25.521",
        "Left elbow": "M25.522",
        "Right wrist": "M25.531",
        "Left Wrist": "M25.532",
        "Right hand": "M79.641",
        "Left hand": "M79.642",
        "Right fingers": "M79.644",
        "Left fingers": "M79.645",
        "Lower Back": "M54.5",
        "Upper back": "M54.9",
        "Chest": "R07.89",
        "Stomach": "R10.9",
        "Right hip": "M25.551",
        "Left Hip": "M25.552",
        "Right thigh": "M79.651",
        "Left thigh": "M79.652",
        "Right knee": "M25.561",
        "Left knee": "M25.562",
        "Right Leg": "M79.604",
        "Left Leg": "M79.605",
        "Right foot & ankle": "M25.571",
        "Left foot & ankle": "M25.572",
        "Right toes": "M79.674",
        "Left toes": "M79.675",
        "Other": "G89.11",
    },
}

# Muscle Spasms Request
muscle_spasms_codes = {
    "default_code": "M62.838",
    "locations": {
        "Face": "M62.838",
        "Head": "M62.838",
        "Neck": "M62.838",
        "Right Shoulder": "M62.411",
        "Left Shoulder": "M62.412",
        "Right Arm": "M62.421",
        "Left Arm": "M62.422",
        "Right elbow": "M62.838",
        "Left Elbow": "M62.838",
        "Right wrist": "M62.838",
        "Left Wrist": "M62.838",
        "Right hand": "M62.441",
        "Left hand": "M62.442",
        "Right fingers": "M62.838",
        "Left fingers": "M62.838",
        "Lower Back": "M62.830",
        "Upper back": "M62.830",
        "Chest": "M62.838",
        "Stomach": "R10.9",
        "Right hip": "M62.838",
        "Left Hip": "M62.838",
        "Right thigh": "M62.451",
        "Left thigh": "M62.452",
        "Right knee": "M62.838",
        "Left knee": "M62.838",
        "Right Leg": "M62.461",
        "Left Leg": "M62.462",
        "Right foot & ankle": "M62.471",
        "Left foot & ankle": "M62.472",
        "Right toes": "M62.838",
        "Left toes": "M62.838",
        "Other": "M62.838",
    },
}

# Condition request mappings (key = Condition.code)
condition_code_map: Dict[str, CodeValue] = {
    "pain_request": pain_condition_codes["default_code"],
    "muscle_relaxer": muscle_spasms_codes["default_code"],
    "dermatitis_eczema_psoriasis": ["L30.9", "L40.9", "L20.83"],
    "scar_wound_actinic": ["L90.5", "L57.0", "S81.009A"],
    "acid_reflux": "K21.9",
    "metabolic_dietary_supplement": "E63.9",
    "cough": ["R68.89", "R05"],
    "allergy": ["T78.40XA", "J30.9"],
    "oral_nsaids": "M06.4",
    "topical_antifungal": "B37.9",
    "migraine_headache": ["G43.909", "R51.9"],
    "acne": "L70.0",
}


def normalize_label(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def to_code_list(value: CodeValue) -> List[str]:
    if isinstance(value, str):
        raw = [part.strip() for part in value.split(",")]
    else:
        raw = [str(part).strip() for part in value]
    return [code for code in raw if code]


def merge_codes(existing_value: str, new_codes: Iterable[str]) -> str:
    merged: List[str] = []
    seen = set()

    existing_codes = []
    if existing_value:
        existing_codes = [part.strip() for part in existing_value.split(",") if part.strip()]

    for code in list(existing_codes) + list(new_codes):
        if code not in seen:
            seen.add(code)
            merged.append(code)

    return ", ".join(merged)


def set_condition_icd_codes() -> Tuple[int, int, List[str]]:
    updated = 0
    created = 0
    missing_names: List[str] = []

    for condition_code, icd_value in condition_code_map.items():
        icd_codes = to_code_list(icd_value)
        icd_payload = ", ".join(icd_codes)

        condition, was_created = Condition.objects.get_or_create(
            code=condition_code,
            defaults={
                "name": condition_code.replace("_", " ").title(),
                "icd_code": icd_payload,
            },
        )

        if was_created:
            created += 1
        if not condition.name:
            missing_names.append(condition_code)

        if condition.icd_code != icd_payload:
            condition.icd_code = icd_payload
            condition.save(update_fields=["icd_code"])
            updated += 1

    return updated, created, missing_names


def set_location_choice_icd_codes() -> Tuple[int, int, int]:
    """
    Store location-level ICD mappings on shared location choices.

    Because location choices are reused by multiple conditions, we merge codes
    so a single choice can retain both pain and muscle-spasm ICD values.
    """

    target_choice_sets = ["PAIN_LOCATIONS_ALL", "LASER_PAIN_LOCATIONS", "CCT_PAIN_LOCATIONS"]
    choices = Choice.objects.filter(choice_set__name__in=target_choice_sets).select_related("choice_set")

    choice_by_key = {
        (choice.choice_set.name, normalize_label(choice.text)): choice
        for choice in choices
    }

    location_maps = [
        ("PAIN_LOCATIONS_ALL", pain_condition_codes["locations"]),
        ("PAIN_LOCATIONS_ALL", muscle_spasms_codes["locations"]),
        ("LASER_PAIN_LOCATIONS", pain_condition_codes["locations"]),
        ("CCT_PAIN_LOCATIONS", pain_condition_codes["locations"]),
    ]

    updated = 0
    unchanged = 0
    missing = 0

    for choice_set_name, locations_map in location_maps:
        for location_label, icd_code in locations_map.items():
            key = (choice_set_name, normalize_label(location_label))
            choice = choice_by_key.get(key)
            if not choice:
                missing += 1
                continue

            merged_value = merge_codes(choice.icd_code or "", [icd_code])
            if (choice.icd_code or "") == merged_value:
                unchanged += 1
                continue

            choice.icd_code = merged_value
            choice.save(update_fields=["icd_code"])
            updated += 1

    return updated, unchanged, missing


def run_seed() -> None:
    with transaction.atomic():
        conditions_updated, conditions_created, conditions_without_name = set_condition_icd_codes()
        choices_updated, choices_unchanged, choices_missing = set_location_choice_icd_codes()

    print("ICD mapping seed complete")
    print(f"Conditions created: {conditions_created}")
    print(f"Conditions updated: {conditions_updated}")
    print(f"Choices updated: {choices_updated}")
    print(f"Choices unchanged: {choices_unchanged}")
    print(f"Choice labels not found in target sets: {choices_missing}")

    if conditions_without_name:
        print("Conditions with empty names (please verify):")
        for code in conditions_without_name:
            print(f" - {code}")


if __name__ == "__main__":
    run_seed()