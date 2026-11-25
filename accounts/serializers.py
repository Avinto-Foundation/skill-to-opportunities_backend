"""Serializers for registration and the current user."""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Role, User


class RegisterSerializer(serializers.ModelSerializer):
    """Creates a candidate or employer account. Admins cannot self-register."""

    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    role = serializers.ChoiceField(choices=[Role.CANDIDATE, Role.EMPLOYER])

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role", "password"]
        read_only_fields = ["id"]

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """The logged-in user's own details."""

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role"]
        read_only_fields = fields
