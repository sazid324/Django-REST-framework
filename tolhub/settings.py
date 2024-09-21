from datetime import timedelta
from pathlib import Path

import environ

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env()
env.read_env(env_file=str(BASE_DIR) + "/.env")

# Security settings
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-@zh*iqxr8km5hy#qti*t+83ky0+s3)n$k%@_5qy5rhfba0g4e*",
)
DEBUG = env("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = ["*"]

# Custom user model
AUTH_USER_MODEL = "authorization.CustomUserModel"


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "generic_relations",
    "sorl.thumbnail",
    "corsheaders",
    "guardian",
    "rest_framework",
    "django_filters",
    "drf_yasg",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_userforeignkey",
    # Custom apps
    "authentication",
    "authorization",
    "filesystem",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_userforeignkey.middleware.UserForeignKeyMiddleware",
]

ROOT_URLCONF = "tolhub.urls"

# Templates configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tolhub.wsgi.application"


# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("MYSQL_DATABASE"),
        "USER": env("MYSQL_USER"),
        "PASSWORD": env("MYSQL_ROOT_PASSWORD"),
        "HOST": env("MYSQL_HOST"),
        "PORT": env("MYSQL_PORT"),
        "OPTIONS": {
            "init_command": "SET time_zone = '+06:00'",
        },
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Authentication backends
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)


# Django REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
}


# Default token lifetimes
ACCESS_TOKEN_LIFETIME_MINUTES = 6
REFRESH_TOKEN_LIFETIME_DAYS = 30


# JWT settings
SIMPLE_JWT = {
    "TOKEN_OBTAIN_SERIALIZER": "authentication.serializers.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "authentication.serializers.serializers.RefreshTokenSerializer",
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS),
    "USER_ID_FIELD": "user_id",
    "USER_ID_CLAIM": "user_id",
}


# OTP verification times
OTP_VERIFICATION_TIME = env("OTP_VERIFICATION_TIME", cast=int, default=2)
USER_PASSWORD_RESET_VERIFICATION_TIME = env(
    "USER_PASSWORD_RESET_VERIFICATION_TIME", cast=int, default=2
)
USER_PASSWORD_RESET_OTP_VERIFICATION_TIME = env(
    "USER_PASSWORD_RESET_OTP_VERIFICATION_TIME", cast=int, default=2
)


# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="smtp.your-email-provider.com")
EMAIL_USE_TLS = env("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_PORT = env("EMAIL_PORT", cast=int, default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="test@example.com")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="testpassword")


# Swagger settings
SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "tolhub.swagger.CustomAutoSchema",
    "SECURITY_DEFINITIONS": {
        "basic": {"type": "basic"},
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "USE_SESSION_AUTH": True,
    "LOGIN_URL": "/api-auth/login/",
    "LOGOUT_URL": "/api-auth/logout/",
}


# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
