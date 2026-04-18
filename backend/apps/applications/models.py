from django.conf import settings
from django.db import models
from apps.events.models import EventPosition
from apps.accounts.models import VolunteerProfile


class ApplicationStatus(models.TextChoices):
    NEW = 'new', 'Новая'
    REVIEWED = 'reviewed', 'Рассмотрена'
    INVITED = 'invited', 'Приглашение отправлено'
    ASSIGNED = 'assigned', 'Назначен'
    CONFIRMED = 'confirmed', 'Подтверждено'
    COMPLETED = 'completed', 'Завершено'
    FAILED = 'failed', 'Не выполнено'
    DECLINED = 'declined', 'Отклонено'


class Application(models.Model):
    position = models.ForeignKey(
        EventPosition, on_delete=models.CASCADE, related_name='applications'
    )
    volunteer_profile = models.ForeignKey(
        VolunteerProfile, on_delete=models.CASCADE, related_name='applications'
    )
    status = models.CharField(
        max_length=20, choices=ApplicationStatus.choices,
        default=ApplicationStatus.NEW
    )
    motivation_text = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('position', 'volunteer_profile')]

    def __str__(self):
        return f"{self.volunteer_profile} → {self.position.title} [{self.status}]"


class Assignment(models.Model):
    position = models.ForeignKey(
        EventPosition, on_delete=models.CASCADE, related_name='assignments'
    )
    volunteer_profile = models.ForeignKey(
        VolunteerProfile, on_delete=models.CASCADE, related_name='assignments'
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='created_assignments'
    )
    status = models.CharField(
        max_length=20, choices=ApplicationStatus.choices,
        default=ApplicationStatus.ASSIGNED
    )

    coordinator_rating = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text='Оценка координатора от 1 до 5'
    )
    hours_worked = models.PositiveSmallIntegerField(
        default=0,
        help_text='Фактическое количество часов участия'
    )
    coordinator_note = models.TextField(
        blank=True, default='',
        help_text='Комментарий координатора'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('position', 'volunteer_profile')]

    def __str__(self):
        return f"{self.volunteer_profile} → {self.position.title} [{self.status}]"
