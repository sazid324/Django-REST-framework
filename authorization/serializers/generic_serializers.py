from rest_framework import serializers

from authorization import models as authorization_models


class GetAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = authorization_models.AddressModel
        fields = [
            "address_id",
            "country",
            "region",
            "city",
            "area",
            "street_address",
            "landmark",
            "zip_code",
        ]
        read_only_fields = [
            "address_id",
            "country",
            "region",
            "city",
            "area",
            "zip_code",
            "street_address",
            "landmark",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user_addresses = GetAddressSerializer(many=True, read_only=True)

    class Meta:
        model = None
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "gender",
            "is_active",
            "date_joined",
            "image",
            "user_addresses",
        ]
        read_only_fields = [
            "user_id",
            "email",
            "date_joined",
            "is_active",
            "user_addresses",
        ]
