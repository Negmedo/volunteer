from django.conf import settings
from django.db import models

from apps.core.models import (
    City,
    District,
    Skill,
    Language,
    VolunteerDirection,
    TaskType,
    AvailabilitySlot,
)


class Role(models.TextChoices):
    VOLUNTEER = "VOLUNTEER", "Волонтёр"
    ORG = "ORG", "Организация"
    ADMIN = "ADMIN", "Администратор"


class ExperienceLevel(models.IntegerChoices):
    NONE = 0, "Нет опыта"
    BASIC = 1, "Базовый"
    MEDIUM = 2, "Средний"
    ADVANCED = 3, "Продвинутый"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VOLUNTEER
    )
    phone = models.CharField(max_length=50, blank=True, default="")
    city = models.CharField(max_length=120, blank=True, default="")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class VolunteerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="volunteer_profile"
    )

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="volunteers"
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="volunteers"
    )

    languages = models.ManyToManyField(
        Language,
        blank=True,
        related_name="volunteers"
    )
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="volunteers"
    )
    preferred_directions = models.ManyToManyField(
        VolunteerDirection,
        blank=True,
        related_name="volunteers"
    )
    preferred_task_types = models.ManyToManyField(
        TaskType,
        blank=True,
        related_name="preferred_by_volunteers"
    )
    availability_slots = models.ManyToManyField(
        AvailabilitySlot,
        blank=True,
        related_name="volunteers"
    )

    experience_level = models.IntegerField(
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.NONE
    )

    has_car = models.BooleanField(default=False)
    ready_for_night_shifts = models.BooleanField(default=False)
    can_travel_to_other_districts = models.BooleanField(default=False)

    short_bio = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Не используется в matching, только для интерфейса"
    )

    is_profile_completed = models.BooleanField(default=False)
    profile_completion_percent = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Анкета волонтёра"
        verbose_name_plural = "Анкеты волонтёров"

    def __str__(self):
        return f"Анкета: {self.user.username}"

    def calculate_completion_percent(self):
        total_checks = 8
        score = 0

        if self.city:
            score += 1
        if self.district:
            score += 1
        if self.languages.exists():
            score += 1
        if self.skills.exists():
            score += 1
        if self.preferred_directions.exists():
            score += 1
        if self.preferred_task_types.exists():
            score += 1
        if self.availability_slots.exists():
            score += 1
        if self.experience_level is not None:
            score += 1

        percent = int((score / total_checks) * 100)
        self.profile_completion_percent = percent
        self.is_profile_completed = percent >= 50
        return percent