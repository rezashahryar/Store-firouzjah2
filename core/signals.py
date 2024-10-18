from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from .models import User


@receiver(post_save, sender=User)
def create_token_for_each_user_when_registered(instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
    