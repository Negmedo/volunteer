from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
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

    # Текстовая локация + точные координаты
    venue_name = models.CharField(max_length=255, blank=True, default="")
    address_text = models.CharField(max_length=255, blank=True, default="")
    venue_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    venue_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
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
    """
    Legacy/fallback-модель для текущего MVP.
    Оставляем её, чтобы не ломать текущие формы и matching-заглушки.
    Финальная workflow-схема должна постепенно переходить на EventPosition.
    """
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


class PositionStatus(models.TextChoices):
    DRAFT = "DRAFT", "Черновик"
    OPEN = "OPEN", "Открыта"
    FILLED = "FILLED", "Укомплектована"
    CLOSED = "CLOSED", "Закрыта"
    CANCELLED = "CANCELLED", "Отменена"


class WorkflowStatus(models.TextChoices):
    NEW = "new", "Новая"
    APPLIED = "applied", "Отклик отправлен"
    REVIEWED = "reviewed", "Рассмотрена"
    ASSIGNED = "assigned", "Назначен"
    CONFIRMED = "confirmed", "Подтверждено"
    DECLINED = "declined", "Отклонено"
    COMPLETED = "completed", "Завершено"
    FAILED = "failed", "Не выполнено"


class ApplicationSource(models.TextChoices):
    SELF = "SELF", "Самоотклик"
    MANUAL = "MANUAL", "Добавлено вручную"
    MATCHING = "MATCHING", "Подобрано системой"


class EventPosition(models.Model):
    """
    Финальная сущность для matching/workflow:
    требования живут на уровне позиции, а не на уровне Event.
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="positions"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    direction = models.ForeignKey(
        VolunteerDirection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="event_positions"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="event_positions"
    )

    required_skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="required_for_positions"
    )
    optional_skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="optional_for_positions"
    )
    required_languages = models.ManyToManyField(
        Language,
        blank=True,
        related_name="required_languages_for_positions"
    )
    preferred_availability_slots = models.ManyToManyField(
        AvailabilitySlot,
        blank=True,
        related_name="preferred_slots_for_positions"
    )

    min_experience_level = models.IntegerField(
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.NONE
    )

    requires_car = models.BooleanField(default=False)
    requires_night_shift = models.BooleanField(default=False)
    allows_other_districts = models.BooleanField(default=True)

    slots_total = models.PositiveIntegerField(default=1)
    slots_filled = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=PositionStatus.choices,
        default=PositionStatus.OPEN
    )

    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Позиция мероприятия"
        verbose_name_plural = "Позиции мероприятий"
        ordering = ["event_id", "sort_order", "id"]

    def __str__(self):
        return f"{self.event.title} / {self.title}"

    @property
    def open_slots(self):
        remaining = self.slots_total - self.slots_filled
        return max(remaining, 0)


class Application(models.Model):
    position = models.ForeignKey(
        EventPosition,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    volunteer_profile = models.ForeignKey(
        "accounts.VolunteerProfile",
        on_delete=models.CASCADE,
        related_name="applications"
    )

    status = models.CharField(
        max_length=20,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.NEW
    )
    source = models.CharField(
        max_length=20,
        choices=ApplicationSource.choices,
        default=ApplicationSource.SELF
    )

    match_score = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True
    )
    motivation_text = models.TextField(blank=True, default="")
    review_comment = models.TextField(blank=True, default="")

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_applications"
    )

    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Заявка на позицию"
        verbose_name_plural = "Заявки на позиции"
        ordering = ["-applied_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["position", "volunteer_profile"],
                name="uniq_application_per_position_and_volunteer"
            )
        ]

    def __str__(self):
        return f"{self.volunteer_profile.user.username} → {self.position.title}"


class Assignment(models.Model):
    position = models.ForeignKey(
        EventPosition,
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    volunteer_profile = models.ForeignKey(
        "accounts.VolunteerProfile",
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    application = models.OneToOneField(
        Application,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assignment"
    )

    status = models.CharField(
        max_length=20,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.ASSIGNED
    )

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_assignments"
    )

    reliability_snapshot = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    notes = models.TextField(blank=True, default="")

    assigned_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Назначение на позицию"
        verbose_name_plural = "Назначения на позиции"
        ordering = ["-assigned_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["position", "volunteer_profile"],
                name="uniq_assignment_per_position_and_volunteer"
            )
        ]

    def __str__(self):
        return f"{self.volunteer_profile.user.username} → {self.position.title} ({self.status})"