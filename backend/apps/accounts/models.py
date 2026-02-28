from django.conf import settings
from django.db import models

class Role(models.TextChoices):
    VOLUNTEER = "VOLUNTEER", "Волонтёр"
    ORG = "ORG", "Организация"
    ADMIN = "ADMIN", "Администратор"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VOLUNTEER)

    # базовые поля анкеты можно расширять позже (из docx)
    city = models.CharField(max_length=120, blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return f"{self.user.username} ({self.role})"