from django.db import models
from django.core.validators import validate_integer
from django.conf import settings

# Create your models here.


class RequestPhotographyService(models.Model):
    full_name = models.CharField(max_length=255)
    mobile_num = models.CharField(max_length=11, validators=[validate_integer])
    province = models.ForeignKey(settings.PATH_PROVINCE_MODEL, on_delete=models.CASCADE, related_name='request_photography')
    city = models.ForeignKey(settings.PATH_CITY_MODEL, on_delete=models.CASCADE, related_name='request_photography')
    mantaghe = models.ForeignKey(settings.PATH_MANTAGHE_MODEL, on_delete=models.CASCADE, related_name='request_photography')
    address = models.TextField()
    store_name = models.CharField(max_length=255)
    request_text = models.TextField()

    def __str__(self) -> str:
        return f'{self.full_name}: {self.store_name}'
