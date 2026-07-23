from rest_framework import serializers

from accounts.models import AccountProfile

from .models import PrescribeAbleItem, Script, ScriptClientRelationship


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
