from django.conf import settings
from django.db import models

from apps.accounts.models import ExperienceLevel
from apps.core.models import (
    City,
    District,
    Skill,
    Language,
    VolunteerDirection,
    TaskType,
    AvailabilitySlot,
)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    is_public = models.BooleanField(default=True)

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events"
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events"
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_events"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class EventRequirement(models.Model):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="requirement"
    )

    direction = models.ForeignKey(
        VolunteerDirection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="event_requirements"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="event_requirements"
    )

    required_skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="required_for_events"
    )
    optional_skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="optional_for_events"
    )
    required_languages = models.ManyToManyField(
        Language,
        blank=True,
        related_name="required_for_events"
    )
    preferred_availability_slots = models.ManyToManyField(
        AvailabilitySlot,
        blank=True,
        related_name="preferred_for_events"
    )

    min_experience_level = models.IntegerField(
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.NONE
    )

    requires_car = models.BooleanField(default=False)
    requires_night_shift = models.BooleanField(default=False)
    allows_other_districts = models.BooleanField(default=True)

    volunteers_needed = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Требования к мероприятию"
        verbose_name_plural = "Требования к мероприятиям"

    def __str__(self):
        return f"Требования: {self.event.title}"


class VolunteerHoursManager(models.Manager):
    def aggregate_total_hours(self):
        return float(self.get_queryset().aggregate(models.Sum("hours"))["hours__sum"] or 0)


class VolunteerHours(models.Model):
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    hours = models.FloatField(default=0)

    objects = VolunteerHoursManager()

    def __str__(self):
        return f"{self.volunteer} - {self.event}: {self.hours}h"