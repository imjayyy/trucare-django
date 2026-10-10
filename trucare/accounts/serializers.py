from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AccountProfile, DoctorLicense, DoctorProfile


User = get_user_model()


class DoctorLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorLicense
        fields = ["license_number", "state"]



class AccountProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountProfile
        fields = ["role", "organization_type", "parent_organization"]


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]

    def get_profile(self, obj):
        if not hasattr(obj, "account_profile"):
            return None
        return AccountProfileSerializer(obj.account_profile).data



class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = DoctorProfile
        fields = "__all__"

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=[choice[0] for choice in AccountProfile.ROLE_CHOICES])
    organization_type = serializers.ChoiceField(
        choices=[choice[0] for choice in AccountProfile.ORGANIZATION_TYPE_CHOICES],
        required=False,
        allow_null=True,
    )
    parent_organization_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_username(self, value):
        user_qs = User.objects.all()
        if self.instance:
            user_qs = user_qs.exclude(pk=self.instance.pk)
        if user_qs.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        user_qs = User.objects.all()
        if self.instance:
            user_qs = user_qs.exclude(pk=self.instance.pk)
        if user_qs.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate(self, attrs):
        role = attrs.get("role")
        organization_type = attrs.get("organization_type")
        parent_org_id = attrs.get("parent_organization_id")

        if role == AccountProfile.ROLE_ORGANIZATION and not organization_type:
            raise serializers.ValidationError(
                {"organization_type": "organization_type is required for organization accounts."}
            )

        if role != AccountProfile.ROLE_ORGANIZATION and organization_type:
            raise serializers.ValidationError(
                {"organization_type": "organization_type is only valid for organization accounts."}
            )

        if role == AccountProfile.ROLE_INTAKE_AGENT and not parent_org_id:
            raise serializers.ValidationError(
                {"parent_organization_id": "parent_organization_id is required for intake agents."}
            )

        if role != AccountProfile.ROLE_INTAKE_AGENT and parent_org_id:
            raise serializers.ValidationError(
                {"parent_organization_id": "parent_organization_id is only valid for intake agents."}
            )

        if parent_org_id:
            try:
                parent_org_user = User.objects.get(id=parent_org_id)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"parent_organization_id": "Parent organization user not found."}
                )

            profile = getattr(parent_org_user, "account_profile", None)
            if not profile or profile.role != AccountProfile.ROLE_ORGANIZATION:
                raise serializers.ValidationError(
                    {"parent_organization_id": "Parent user must be an organization account."}
                )

        return attrs

    def create(self, validated_data):
        role = validated_data.pop("role")
        organization_type = validated_data.pop("organization_type", None)
        parent_org_id = validated_data.pop("parent_organization_id", None)

        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)

        parent_organization = None
        if parent_org_id:
            parent_organization = User.objects.get(id=parent_org_id)

        AccountProfile.objects.create(
            user=user,
            role=role,
            organization_type=organization_type,
            parent_organization=parent_organization,
        )
        return user

    def update(self, instance, validated_data):
        role = validated_data.pop("role", None)
        organization_type = validated_data.pop("organization_type", None)
        parent_org_id = validated_data.pop("parent_organization_id", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        profile = getattr(instance, "account_profile", None)
        if profile:
            if role:
                profile.role = role
            if organization_type is not None:
                profile.organization_type = organization_type
            if parent_org_id is not None:
                profile.parent_organization = User.objects.get(id=parent_org_id) if parent_org_id else None
            profile.save()

        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)


class JWTLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        profile = getattr(user, "account_profile", None)
        token["role"] = profile.role if profile else None
        token["organization_type"] = profile.organization_type if profile else None
        return token


class JWTRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = RefreshToken(attrs["refresh"])
        access_token = refresh.access_token

        user = None
        user_id = refresh.get("user_id")
        if user_id:
            user = User.objects.filter(id=user_id).select_related("account_profile").first()

        profile = getattr(user, "account_profile", None) if user else None
        access_token["role"] = profile.role if profile else None
        access_token["organization_type"] = profile.organization_type if profile else None

        data["access"] = str(access_token)
        return data

