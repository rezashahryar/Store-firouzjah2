from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def profile_when_register_new_user(instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )
