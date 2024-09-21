from typing import Any, Dict

from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from authentication import models as authentication_models
from authorization import models as authorization_models
from authorization import serializers as authorization_serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = authorization_models.CustomUserModel
        fields = [
            "user_id",
            "email",
            "first_name",
            "last_name",
            "password",
            "user_type",
        ]

    def create(self, validated_data):
        email = validated_data.pop("email", None)
        user = authorization_models.CustomUserModel.objects.create_user(
            email=email, **validated_data
        )
        authorization_models.AddressModel.objects.create(user=user)
        if user.user_type == 1:
            user.verified = True
            user.save()
        return user


class GoogleOAuthSignupSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class EmailFieldSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    secret = serializers.UUIDField(write_only=True)

    class Meta:
        model = authorization_models.CustomUserModel
        fields = ["password", "confirm_password", "secret"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"error": "Passwords and confirm password do not match"}
            )
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class OtpSaveSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.user_id")

    class Meta:
        model = authentication_models.UserOtpModel
        fields = ["user_id", "otp"]


class ResendOtpSaveSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()


class OtpFieldSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)


class UserPasswordOtpSerializer(EmailFieldSerializer, OtpFieldSerializer):
    pass


class ResendResetPassOtpSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        user = authorization_serializers.UserSerializer(self.user).data
        data["refreshToken"] = str(data["refresh"])
        data["accessToken"] = str(data["access"])
        data["user"] = user
        data["user"]["user_id"] = str(self.user.user_id)
        data["user"]["user_type"] = self.user.user_type

        del data["refresh"]
        del data["access"]
        return data

    @classmethod
    def get_token(cls, user):
        if not user.verified:
            raise NotAcceptable(detail="user Not verified")
        token = super().get_token(user)
        token["name"] = user.email
        token["user_id"] = str(user.user_id)
        token["user_type"] = user.user_type
        return token


class RefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data["refreshToken"] = str(data["refresh"])
        data["accessToken"] = str(data["access"])
        del data["refresh"]
        del data["access"]
        return data
