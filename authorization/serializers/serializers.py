from rest_framework import serializers

from authorization import models as authorization_models
from authorization.serializers import (
    generic_serializers as authorization_generic_serializers,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = authorization_models.CustomUserModel
        fields = ["user_id", "email"]


class UserProfileSerializer(authorization_generic_serializers.ProfileSerializer):
    class Meta:
        model = authorization_models.CustomUserModel
        fields = authorization_generic_serializers.ProfileSerializer.Meta.fields
        read_only_fields = (
            authorization_generic_serializers.ProfileSerializer.Meta.read_only_fields
        )


class AdminProfileSerializer(authorization_generic_serializers.ProfileSerializer):
    class Meta:
        model = authorization_models.CustomUserModel
        fields = authorization_generic_serializers.ProfileSerializer.Meta.fields
        read_only_fields = (
            authorization_generic_serializers.ProfileSerializer.Meta.read_only_fields
        )


class ProfileManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = authorization_models.CustomUserModel
        fields = [
            "is_active",
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = authorization_models.AddressModel
        fields = [
            "country",
            "region",
            "city",
            "area",
            "zip_code",
            "street_address",
            "landmark",
        ]
