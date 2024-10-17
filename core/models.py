from uuid import uuid4
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class User(AbstractUser):
    ...


def get_datetime_now():
    return timezone.localtime(timezone.now()) + timedelta(minutes=3)


class RequestOtp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    email = models.EmailField()
    otp_code = models.CharField(max_length=10)

    valid_from = models.DateTimeField(default=timezone.now, null=True)
    valid_until = models.DateTimeField(default=get_datetime_now, null=True)

    def __str__(self) -> str:
        return f'{self.email}: {self.otp_code}'
