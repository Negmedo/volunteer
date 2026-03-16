from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Role, VolunteerProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_related_profiles(sender, instance, created, **kwargs):
    if created:
        profile, _ = Profile.objects.get_or_create(
            user=instance,
            defaults={"role": Role.VOLUNTEER}
        )
        VolunteerProfile.objects.get_or_create(user=instance)