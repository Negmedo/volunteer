from django.conf import settings
from django.db import models
from apps.events.models import EventPosition
from apps.accounts.models import VolunteerProfile

class ApplicationStatus(models.TextChoices):
    NEW = 'new', 'Новая'
    REVIEWED = 'reviewed', 'Рассмотрена'
    ASSIGNED = 'assigned', 'Назначен'
    CONFIRMED = 'confirmed', 'Подтверждено'
    COMPLETED = 'completed', 'Завершено'
    FAILED = 'failed', 'Не выполнено'
    DECLINED = 'declined', 'Отклонено'

class Application(models.Model):
    position = models.ForeignKey(EventPosition, on_delete=models.CASCADE, related_name='applications')
    volunteer_profile = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.NEW)
    motivation_text = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [('position', 'volunteer_profile')]

class Assignment(models.Model):
    position = models.ForeignKey(EventPosition, on_delete=models.CASCADE, related_name='assignments')
    volunteer_profile = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='assignments')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.ASSIGNED)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = [('position', 'volunteer_profile')]
