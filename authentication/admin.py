from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authorization import models as authorization_models


class UserAdmin(UserAdmin):
    model = authorization_models.CustomUserModel
    list_display = (
        "email",
        "phone",
        "is_staff",
        "user_type",
        "date_joined",
        "is_active",
    )
    list_filter = (
        "email",
        "phone",
        "is_staff",
        "user_type",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone",
                    "user_type",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    ordering = ("-date_joined",)


admin.site.register(authorization_models.CustomUserModel, UserAdmin)
