from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from authentication import views as authentication_views

router = routers.DefaultRouter()
router.register(
    r"reset-password", authentication_views.PasswordResetView, basename="reset-password"
)

urlpatterns = [
    path("api/signup/", authentication_views.UserRegistrationView.as_view()),
    path(
        "api/google-oauth-signup/", authentication_views.GoogleOAuthSignupView.as_view()
    ),
    path("api/signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path(r"api/", include(router.urls)),
    path(
        "api/password-reset/otp-verify/",
        authentication_views.PassRestOtpVerificationView.as_view(),
        name="reset-password-otp-verify",
    ),
    path(
        "api/password-reset/otp-resend/",
        authentication_views.ResendResetPassOtpView.as_view(),
        name="password-reset-otp-resend",
    ),
    path(
        "api/otp-verification/",
        authentication_views.OtpVerificationView.as_view(),
        name="otp-verification",
    ),
    path(
        "api/otp-create/",
        authentication_views.ResendOtpView.as_view(),
        name="otp-create",
    ),
]
