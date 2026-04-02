from django.conf import settings
from django.db import models
from apps.core.models import City, District, VolunteerDirection, TaskType, Skill, Language
from apps.accounts.models import SkillLevel, LanguageLevel, TimeOfDay, WEEKDAY_CHOICES


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    address_text = models.CharField(max_length=255, blank=True, default="")
    start_date = models.DateField()
    end_date = models.DateField()
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_events")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class EventPosition(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="positions")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    direction = models.ForeignKey(VolunteerDirection, on_delete=models.SET_NULL, null=True, blank=True)
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True, blank=True)
    slots_total = models.PositiveIntegerField(default=1)
    requires_car = models.BooleanField(default=False)
    requires_night_shift = models.BooleanField(default=False)
    requires_physical_work = models.BooleanField(default=False)
    requires_heavy_lifting = models.BooleanField(default=False)
    avoid_large_crowds_sensitive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.title} / {self.title}"


class EventPositionRequiredSkill(models.Model):
    position = models.ForeignKey(EventPosition, on_delete=models.CASCADE, related_name="required_skill_items")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    min_level = models.CharField(max_length=20, choices=SkillLevel.choices, default=SkillLevel.BEGINNER)

    class Meta:
        unique_together = [("position", "skill")]


class EventPositionOptionalSkill(models.Model):
    position = models.ForeignKey(EventPosition, on_delete=models.CASCADE, related_name="optional_skill_items")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    min_level = models.CharField(max_length=20, choices=SkillLevel.choices, default=SkillLevel.BEGINNER)

    class Meta:
        unique_together = [("position", "skill")]


class EventPositionLanguageRequirement(models.Model):
    position = models.ForeignKey(EventPosition, on_delete=models.CASCADE, related_name="language_requirements")
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    min_level = models.CharField(max_length=20, choices=LanguageLevel.choices, default=LanguageLevel.CONVERSATIONAL)

    class Meta:
        unique_together = [("position", "language")]


class EventPositionAvailabilityRequirement(models.Model):
    position = models.ForeignKey(EventPosition, on_delete=models.CASCADE, related_name="availability_requirements")
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    time_of_day = models.CharField(max_length=16, choices=TimeOfDay.choices)

    class Meta:
        unique_together = [("position", "weekday", "time_of_day")]
        ordering = ["weekday", "time_of_day"]
