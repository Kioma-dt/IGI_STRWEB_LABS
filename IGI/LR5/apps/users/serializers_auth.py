from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.constants import GROUP_CUSTOMER
from apps.users.models import CustomerProfile

User = get_user_model()


class ZoomShopTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT claims include group membership for clients."""

    @classmethod
    def get_token(cls, user: User) -> object:
        token = super().get_token(user)
        token["groups"] = list(user.groups.values_list("name", flat=True))
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser
        return token


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    birth_date = serializers.DateField(required=False, allow_null=True)

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        if User.objects.filter(email__iexact=attrs["email"].strip()).exists():
            raise serializers.ValidationError({"email": "User with this email already exists."})
        if CustomerProfile.objects.filter(phone=attrs["phone"], is_deleted=False).exists():
            raise serializers.ValidationError({"phone": "Phone already registered."})
        return attrs

    @transaction.atomic
    def create(self, validated_data: dict) -> User:
        data = validated_data.copy()
        data.pop("password_confirm", None)
        email = data["email"].strip().lower()
        user = User.objects.create_user(
            username=email,
            email=email,
            password=data["password"],
        )
        CustomerProfile.objects.create(
            user=user,
            full_name=data["full_name"].strip(),
            phone=data["phone"].strip(),
            birth_date=data.get("birth_date"),
        )
        group, _ = Group.objects.get_or_create(name=GROUP_CUSTOMER)
        user.groups.add(group)
        return user


class SessionLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)
