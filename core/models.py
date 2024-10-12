from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_integer
# Create your models here.


class User(AbstractUser):
    ...


class RequestOtp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    mobile = models.CharField(max_length=11, validators=[validate_integer])
    otp_code = models.CharField(max_length=10)

    valid_from = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.mobile}: {self.otp_code}'
