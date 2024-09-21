import logging
from uuid import uuid4

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from authentication.utils import generate_otp
from authorization import models as authorization_models
from tolhub.mixins.models import TimeStampMixin


class UserOtpModel(models.Model):
    user = models.ForeignKey(
        authorization_models.CustomUserModel,
        on_delete=models.CASCADE,
        related_name="user_otp",
        blank=False,
        null=False,
    )
    otp = models.CharField(max_length=6, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.email)

    def save(self, *args, **kwargs):
        self.otp = generate_otp()
        context = {
            "user": self.user,
            "otp": self.otp,
        }
        email_html_message = render_to_string("authentication/email.html", context)
        email = EmailMessage(
            subject="Your OTP for TolHub",
            body=email_html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.user.email],
        )
        email.content_subtype = "html"
        try:
            email.send()
        except Exception as e:
            logging.error(f"Failed to send email. Error: {e}")
        super().save(*args, **kwargs)


class UserPasswordResetModel(TimeStampMixin):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE
    )
    secret = models.UUIDField(_("secret key"), default=uuid4)
    otp = models.CharField(max_length=6, blank=False, null=False)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.email)

    def save(self, *args, **kwargs):
        self.otp = generate_otp()
        context = {
            "user": self.user,
            "otp": self.otp,
        }
        email_html_message = render_to_string("authentication/email.html", context)
        email = EmailMessage(
            subject="Your OTP for TolHub",
            body=email_html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.user.email],
        )
        email.content_subtype = "html"
        try:
            email.send()
        except Exception as e:
            logging.error(f"Failed to send email. Error: {e}")
        super().save(*args, **kwargs)
