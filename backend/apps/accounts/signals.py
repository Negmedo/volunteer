from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Role

User = get_user_model()


def _resolve_default_role_for_user(user):

    if user.is_superuser or user.is_staff:
        return Role.ADMIN
    return Role.VOLUNTEER


@receiver(post_save, sender=User)
def create_user_related_profiles(sender, instance, created, **kwargs):

    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={"role": _resolve_default_role_for_user(instance)}
        )