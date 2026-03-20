from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Role

User = get_user_model()


def _resolve_default_role_for_user(user):
    if user.is_superuser or user.is_staff:
        return Role.ADMIN
    return Role.VOLUNTEER


def _sync_volunteer_profile_state(profile: Profile):
    """
    Мягкая синхронизация VolunteerProfile с системной ролью пользователя.

    Правила:
    - роль VOLUNTEER:
        если VolunteerProfile уже существует, включаем его обратно в matching
        ничего автоматически не создаём
    - роль ORG / ADMIN:
        VolunteerProfile НЕ удаляем
        но выключаем из matching, чтобы не попадал в подбор
    """
    user = profile.user

    try:
        volunteer_profile = user.volunteer_profile
    except Exception:
        volunteer_profile = None

    if not volunteer_profile:
        return

    if profile.role == Role.VOLUNTEER:
        if volunteer_profile.is_available_for_matching is False:
            volunteer_profile.is_available_for_matching = True
            volunteer_profile.save(update_fields=["is_available_for_matching"])
    else:
        if volunteer_profile.is_available_for_matching is True:
            volunteer_profile.is_available_for_matching = False
            volunteer_profile.save(update_fields=["is_available_for_matching"])


@receiver(post_save, sender=User)
def create_user_related_profiles(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={"role": _resolve_default_role_for_user(instance)}
        )


@receiver(post_save, sender=Profile)
def sync_role_dependent_entities(sender, instance, **kwargs):
    _sync_volunteer_profile_state(instance)