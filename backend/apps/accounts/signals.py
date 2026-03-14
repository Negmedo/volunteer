from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile, Role

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    profile, was_created = Profile.objects.get_or_create(
        user=instance,
        defaults={"role": Role.VOLUNTEER}
    )

    if not created and not profile.role:
        profile.role = Role.VOLUNTEER
        profile.save()