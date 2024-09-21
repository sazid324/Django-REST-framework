from uuid import uuid4

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication import choices as authentication_choices
from authorization import choices as authorization_choices
from authorization import managres as authorization_managers
from filesystem import models as filesystem_models


class CustomUserModel(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    image = models.ForeignKey(
        filesystem_models.ImageModel,
        on_delete=models.DO_NOTHING,
        related_name="user_image",
        blank=True,
        null=True,
    )
    username = None
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    user_type = models.IntegerField(
        default=authorization_choices.UserChoices.USER,
        choices=authorization_choices.UserChoices.choices,
    )
    email = models.EmailField(blank=False, null=False, unique=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=50,
        choices=authentication_choices.GENDER_CHOICES,
        blank=True,
        null=True,
    )
    agree_terms = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    objects = authorization_managers.CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_type"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        is_user = (
            True
            if self.user_type in [authorization_choices.UserChoices.USER]
            else False
        )
        self.is_staff = not is_user
        super().save(*args, **kwargs)
        group_name = self.get_user_type_display().lower()
        group, created = Group.objects.get_or_create(name=group_name)
        if not self.groups.filter(name=group_name).exists():
            self.groups.add(group)

    @property
    def is_admin(self):
        return self.user_type == authorization_choices.UserChoices.ADMIN

    @property
    def is_user(self):
        return self.user_type == authorization_choices.UserChoices.USER

    class Meta:
        unique_together = [["email", "user_id"]]


class AddressModel(models.Model):
    address_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        CustomUserModel, on_delete=models.DO_NOTHING, related_name="user_addresses"
    )
    country = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(
        max_length=100, blank=True, null=True
    )  # state / province / division
    city = models.CharField(max_length=100, blank=True, null=True)  # town
    area = models.CharField(
        max_length=255, blank=True, null=True
    )  # district / neighborhood
    street_address = models.CharField(max_length=255, blank=True, null=True)  # road
    landmark = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.country}"
