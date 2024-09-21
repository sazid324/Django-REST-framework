from datetime import timedelta

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication import models as authentication_models
from authentication import serializers as authentication_serializers
from authorization import choices as authorization_choices
from authorization import models as authorization_models


class UserRegistrationView(generics.CreateAPIView):
    queryset = authorization_models.CustomUserModel.objects.all()
    serializer_class = authentication_serializers.UserRegistrationSerializer
    lookup_field = "email"

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        authentication_models.UserOtpModel.objects.create(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GoogleOAuthSignupView(generics.CreateAPIView):
    queryset = authorization_models.CustomUserModel.objects.all()
    serializer_class = authentication_serializers.GoogleOAuthSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["id_token"]
        try:
            id_info = id_token.verify_oauth2_token(token, google_requests.Request())
            email = id_info["email"]
            user, created = authorization_models.CustomUserModel.objects.get_or_create(
                email=email
            )
            if created:
                user.first_name = id_info["given_name"]
                user.last_name = id_info["family_name"]
                user.email = email
                user.user_type = authorization_choices.UserChoices.USER
                user.verified = id_info["email_verified"]
                user.agree_terms = True
                user.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response_data = {
                "refreshToken": str(refresh),
                "accessToken": access_token,
                "user": {
                    "user_id": str(user.user_id),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "user_type": user.user_type,
                },
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResendOtpView(generics.CreateAPIView):
    serializer_class = authentication_serializers.ResendOtpSaveSerializer
    queryset = authentication_models.UserOtpModel.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            authorization_models.CustomUserModel, pk=serializer.data["user_id"]
        )
        if not user.verified:
            authentication_models.UserOtpModel.objects.filter(user=user).delete()
            authentication_models.UserOtpModel.objects.create(user=user)
            return Response({"detail": "OK"}, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": "User has already been verified"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class OtpVerificationView(generics.CreateAPIView):
    serializer_class = authentication_serializers.OtpSaveSerializer
    queryset = authentication_models.UserOtpModel.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_otp = get_object_or_404(
            authentication_models.UserOtpModel, user_id=serializer.data["user_id"]
        )
        if user_otp.otp == serializer.data["otp"]:
            verification_time_limit = timedelta(minutes=settings.OTP_VERIFICATION_TIME)
            time_difference = timezone.now() - user_otp.created_at
            user_otp.delete()
            if time_difference <= verification_time_limit:
                user = get_object_or_404(
                    authorization_models.CustomUserModel, pk=serializer.data["user_id"]
                )
                user.is_active = True
                user.verified = True
                user.save()
                return Response(
                    {"detail": "OTP verified successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"message": "Invalid OTP"}, status=status.HTTP_406_NOT_ACCEPTABLE
        )


class PasswordResetView(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = authorization_models.CustomUserModel.objects.all()
    serializer_class = authentication_serializers.ResetPasswordSerializer
    http_method_names = ["post", "put"]
    lookup_field = "email"
    lookup_value_regex = "[^/]+"

    def get_serializer_class(self):
        if self.action == "create":
            return authentication_serializers.EmailFieldSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            authorization_models.CustomUserModel,
            email=serializer.validated_data["email"],
        )
        old_otp = authentication_models.UserPasswordResetModel.objects.filter(
            user=user
        ).first()
        if old_otp:
            old_otp.delete()
        if user.verified:
            authentication_models.UserPasswordResetModel.objects.create(user=user)
            return Response(
                {
                    "user_id": user.user_id,
                    "detail": "The OTP has been sent to the email address",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"detail": "The user has not been verified"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            authorization_models.CustomUserModel, email=kwargs["email"]
        )
        otp_instance = get_object_or_404(
            authentication_models.UserPasswordResetModel, user=user
        )

        if otp_instance.verified:
            if otp_instance.secret != serializer.validated_data["secret"]:
                return Response(
                    {"detail": "Verification of the secret failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            verification_time_limit = timedelta(
                minutes=settings.USER_PASSWORD_RESET_VERIFICATION_TIME
            )
            time_difference = timezone.now() - otp_instance.updated_at
            if time_difference <= verification_time_limit:
                super().update(request, *args, **kwargs)
                otp_instance.delete()
                return Response(
                    {"detail": "Password reset successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "The password reset has timed out"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"detail": "The OTP verification was unsuccessful"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendResetPassOtpView(generics.CreateAPIView):
    serializer_class = authentication_serializers.ResendResetPassOtpSerializer
    queryset = authentication_models.UserPasswordResetModel.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get("user_id")
        instance = get_object_or_404(
            authentication_models.UserPasswordResetModel, user_id=user_id
        )

        if not instance.verified:
            authentication_models.UserPasswordResetModel.objects.filter(
                user_id=user_id
            ).delete()
            authentication_models.UserPasswordResetModel.objects.create(user_id=user_id)
            return Response({"detail": "OK"}, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": "The OTP has already been verified"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PassRestOtpVerificationView(generics.CreateAPIView):
    serializer_class = authentication_serializers.UserPasswordOtpSerializer
    queryset = authentication_models.UserPasswordResetModel.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_pass_reset = get_object_or_404(
            authentication_models.UserPasswordResetModel,
            user__email=serializer.validated_data["email"],
            otp=serializer.validated_data["otp"],
        )
        if user_pass_reset.otp == serializer.data["otp"]:
            verification_time_limit = timedelta(
                minutes=settings.USER_PASSWORD_RESET_OTP_VERIFICATION_TIME
            )
            time_difference = timezone.now() - user_pass_reset.created_at
            if time_difference <= verification_time_limit:
                authentication_models.UserPasswordResetModel.objects.filter(
                    pk=user_pass_reset.pk
                ).update(verified=True)
                return Response(
                    {
                        "detail": "OTP verified successfully",
                        "secret": user_pass_reset.secret,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "The OTP verification has timed out"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        return Response(
            {"message": "Invalid OTP"}, status=status.HTTP_406_NOT_ACCEPTABLE
        )
