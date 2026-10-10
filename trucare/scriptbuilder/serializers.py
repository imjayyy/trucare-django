from rest_framework import serializers

from accounts.models import AccountProfile
from intake.models import Condition

from .models import PrescribeAbleItem, Script, ScriptClientRelationship, ScriptItem


class PrescribeAbleItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
        help_text="Resolved category name from intake.Condition.",
    )

    class Meta:
        model = PrescribeAbleItem
        fields = [
            "id",
            "category",
            "category_name",
            "item_type",
            "name",
            "ndc",
            "generic_name",
            "strength",
            "dosage_form",
            "usual_sig",
            "quantity",
            "refills",
            "duration",
            "description",
            "active",
        ]
        extra_kwargs = {
            "category": {"help_text": "Condition ID from intake.Condition."},
            "item_type": {"help_text": "Type of item: medication, therapy, device, or supplement."},
            "name": {"help_text": "Display name of the prescribeable item."},
            "generic_name": {"help_text": "Generic or non-brand name."},
            "ndc": {"help_text": "National Drug Code (NDC) for medications."},
            "strength": {"help_text": "Strength or concentration, e.g., 3% or 500mg."},
            "dosage_form": {"help_text": "Dosage form, e.g., tablet, capsule, gel."},
            "usual_sig": {"help_text": "Typical instructions for use (SIG)."},
            "quantity": {"help_text": "Recommended quantity for dispensing."},
            "refills": {"help_text": "Number of refills allowed."},
            "duration": {"help_text": "Typical duration, e.g., 30 days."},
            "description": {"help_text": "Additional metadata, notes, or source details."},
            "active": {"help_text": "Whether the item is currently active and selectable."},
        }


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ["id", "name"]
        extra_kwargs = {
            "name": {"help_text": "Human-readable script name."},
        }


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ["id", "name", "code", "icd_code"]
        extra_kwargs = {
            "name": {"help_text": "Condition category display name."},
            "code": {"help_text": "Internal unique condition code."},
            "icd_code": {"help_text": "Optional ICD code for this condition."},
        }


class ScriptItemReadSerializer(serializers.ModelSerializer):
    script_name = serializers.CharField(source="script.name", read_only=True)
    prescribeable_item_name = serializers.CharField(source="prescribeable_item.name", read_only=True)
    category = serializers.IntegerField(source="prescribeable_item.category_id", read_only=True)
    category_name = serializers.CharField(source="prescribeable_item.category.name", read_only=True)
    item_type = serializers.CharField(source="prescribeable_item.item_type", read_only=True)
    generic_name = serializers.CharField(source="prescribeable_item.generic_name", read_only=True)
    strength = serializers.CharField(source="prescribeable_item.strength", read_only=True)
    dosage_form = serializers.CharField(source="prescribeable_item.dosage_form", read_only=True)
    usual_sig = serializers.CharField(source="prescribeable_item.usual_sig", read_only=True)
    quantity = serializers.CharField(source="prescribeable_item.quantity", read_only=True)
    refills = serializers.IntegerField(source="prescribeable_item.refills", read_only=True)
    duration = serializers.CharField(source="prescribeable_item.duration", read_only=True)
    description = serializers.CharField(source="prescribeable_item.description", read_only=True)
    active = serializers.BooleanField(source="prescribeable_item.active", read_only=True)

    class Meta:
        model = ScriptItem
        fields = [
            "id",
            "script",
            "script_name",
            "prescribeable_item",
            "prescribeable_item_name",
            "category",
            "category_name",
            "item_type",
            "generic_name",
            "strength",
            "dosage_form",
            "usual_sig",
            "quantity",
            "refills",
            "duration",
            "description",
            "active",
        ]


class ScriptItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptItem
        fields = ["id", "script", "prescribeable_item"]
        extra_kwargs = {
            "script": {"help_text": "Script ID receiving the prescribed item."},
            "prescribeable_item": {"help_text": "PrescribeAbleItem ID being assigned to the script."},
        }

    def validate(self, attrs):
        script = attrs.get("script")
        prescribeable_item = attrs.get("prescribeable_item")
        existing = ScriptItem.objects.filter(script=script, prescribeable_item=prescribeable_item)
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise serializers.ValidationError("This prescribeable item is already assigned to the selected script.")
        return attrs


class ScriptCategoryItemsSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(help_text="Condition category ID.")
    category_name = serializers.CharField(help_text="Condition category name.")
    items = ScriptItemReadSerializer(many=True, help_text="Drugs/prescribeable items under this category.")


class OrganizationProfileSearchSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = AccountProfile
        fields = [
            "id",
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "organization_type",
        ]


class ScriptAssignmentReadSerializer(serializers.ModelSerializer):
    script_name = serializers.CharField(source="script.name", read_only=True)
    client_username = serializers.CharField(source="client.user.username", read_only=True)
    client_email = serializers.EmailField(source="client.user.email", read_only=True)
    client_organization_type = serializers.CharField(source="client.organization_type", read_only=True)

    class Meta:
        model = ScriptClientRelationship
        fields = [
            "id",
            "script",
            "script_name",
            "client",
            "client_username",
            "client_email",
            "client_organization_type",
        ]


class ScriptAssignmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptClientRelationship
        fields = ["id", "script", "client"]
        extra_kwargs = {
            "script": {"help_text": "Script ID to assign."},
            "client": {"help_text": "AccountProfile ID. Must have role ORGANIZATION."},
        }

    def validate_client(self, value):
        if value.role != AccountProfile.ROLE_ORGANIZATION:
            raise serializers.ValidationError("Selected profile must have role ORGANIZATION.")
        return value

   