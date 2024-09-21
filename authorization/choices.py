from django.db import models


class UserChoices(models.IntegerChoices):
    ADMIN = 1
    USER = 2

STATUS_CHOICES = (
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("freezed", "Freezed"),
)