"""
Seed script for PrescribeAbleItem records from InteractiveMeds.Drugs.json.

Run from /Telemed-Django/trucare:
    python seed_prescribeable_items.py

Optional custom path:
    python seed_prescribeable_items.py --file ../InteractiveMeds.Drugs.json

or:
    python manage.py shell < seed_prescribeable_items.py
"""

import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import django
from django.db import transaction


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trucare.settings")
django.setup()

from intake.models import Condition  # noqa: E402
from scriptbuilder.models import PrescribeAbleItem  # noqa: E402


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (value or "").lower())


# Map source JSON category names to existing Condition.name values.
# Add/update entries here if source labels change.
CATEGORY_TO_CONDITION_NAME = {
    "pain condition": "Pain condition request?",
    "muscle relaxer": "Muscle relaxer condition request?",
    "dermatitis/eczema/psoriasis": "Dermatitis/Eczema/Psoriasis condition request?",
    "scar/wound/actinic keratosis": "Scar/wound/actinic keratosis condition request?",
    "acid reflux": "Acid reflux condition request?",
    "allergy": "Allergy condition request?",
    "cough": "Cough condition request?",
    "topical anti-fungal": "Topical anti-fungal condition request?",
    "migraine and headache": "Migraine and Headache condition request?",
    "foot bath": "Foot bath condition request?",
    "cold sores": "Cold sores condition request?",
    "oral nsaids": "Oral NSAIDs condition request?",
    "acne": "Acne condition request?",
    "diabetes": "Diabetes condition request?",
    "laser therapy pain treatment": "Laser Therapy Pain treatment request?",
    "cold compression therapy": "Cold Compression Therapy request?",
    "coldcompression therapy": "Cold Compression Therapy request?",
}


def resolve_condition(category_name: str, cache: Dict[str, Optional[Condition]]) -> Optional[Condition]:
    name = normalize_text(category_name)
    key = normalize_key(name)
    if key in cache:
        return cache[key]

    mapped_condition_name = CATEGORY_TO_CONDITION_NAME.get(name.lower(), name)

    # 1) direct mapped name match (case-insensitive)
    condition = Condition.objects.filter(name__iexact=mapped_condition_name).first()
    if condition:
        cache[key] = condition
        return condition

    # 2) normalized name match across existing rows
    for existing in Condition.objects.all().only("id", "name", "code"):
        if normalize_key(existing.name) == normalize_key(mapped_condition_name):
            cache[key] = existing
            return existing

    # Explicitly do not create conditions.
    cache[key] = None
    return None


def build_description(row: Dict) -> str:
    chunks: List[str] = []

    ndc = normalize_text(str(row.get("NDC", "")))
    if ndc:
        chunks.append(f"NDC: {ndc}")

    unit = normalize_text(str(row.get("Unit", "")))
    if unit:
        chunks.append(f"Unit: {unit}")

    fax_quantity = normalize_text(str(row.get("FaxQuantity", "")))
    fax_unit = normalize_text(str(row.get("FaxUnit", "")))
    if fax_quantity or fax_unit:
        chunks.append(f"Fax: {fax_quantity} {fax_unit}".strip())

    source_id = row.get("_id", {}).get("$oid", "") if isinstance(row.get("_id"), dict) else ""
    source_id = normalize_text(str(source_id))
    if source_id:
        chunks.append(f"Source ID: {source_id}")

    return " | ".join(chunks)


def load_json_records(file_path: Path) -> List[Dict]:
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected a JSON array of drug records.")

    return data


def upsert_items(records: List[Dict]) -> Tuple[int, int, int, int]:
    created = 0
    updated = 0
    skipped = 0
    missing_category = 0

    condition_cache: Dict[str, Optional[Condition]] = {}

    for row in records:
        drug_name = normalize_text(str(row.get("DrugName", "")))
        category_name = normalize_text(str(row.get("Category Name", "")))

        if not drug_name or not category_name:
            skipped += 1
            continue

        condition = resolve_condition(category_name, condition_cache)
        if not condition:
            missing_category += 1
            skipped += 1
            continue

        quantity = normalize_text(str(row.get("Quantity", "")))
        days_supply = normalize_text(str(row.get("DaysSupply", "")))
        sig = normalize_text(str(row.get("Sig", "")))
        unit = normalize_text(str(row.get("Unit", "")))

        duration = f"{days_supply} days" if days_supply else ""
        description = build_description(row)

        existing = (
            PrescribeAbleItem.objects.filter(
                category=condition,
                item_type=PrescribeAbleItem.MEDICATION,
                name__iexact=drug_name,
            )
            .order_by("id")
            .first()
        )

        payload = {
            "category": condition,
            "item_type": PrescribeAbleItem.MEDICATION,
            "name": drug_name,
            "generic_name": "",
            "strength": "",
            "dosage_form": unit,
            "usual_sig": sig,
            "quantity": quantity,
            "refills": 0,
            "duration": duration,
            "description": description,
            "active": True,
        }

        if existing:
            changed_fields = []
            for field, value in payload.items():
                if getattr(existing, field) != value:
                    setattr(existing, field, value)
                    changed_fields.append(field)

            if changed_fields:
                existing.save(update_fields=changed_fields)
                updated += 1
        else:
            PrescribeAbleItem.objects.create(**payload)
            created += 1

    return created, updated, skipped, missing_category


def default_json_path() -> Path:
    # file expected at /Telemed-Django/InteractiveMeds.Drugs.json
    # while this script lives at /Telemed-Django/trucare/seed_prescribeable_items.py
    return Path(__file__).resolve().parent.parent / "InteractiveMeds.Drugs.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed PrescribeAbleItem from drug JSON.")
    parser.add_argument(
        "--file",
        dest="file",
        default=str(default_json_path()),
        help="Path to InteractiveMeds.Drugs.json",
    )
    args = parser.parse_args()

    file_path = Path(args.file).expanduser().resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")

    records = load_json_records(file_path)

    with transaction.atomic():
        created, updated, skipped, missing_category = upsert_items(records)

    print(f"Processed: {len(records)}")
    print(f"Created PrescribeAbleItem: {created}")
    print(f"Updated PrescribeAbleItem: {updated}")
    print(f"Skipped rows: {skipped}")
    print(f"Skipped due to missing category mapping/condition: {missing_category}")


if __name__ == "__main__":
    main()
