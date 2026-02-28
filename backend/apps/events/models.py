from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    is_public = models.BooleanField(default=True)

    # упрощённо, позже расширим (город/район/даты/навыки/языки по docx)
    city = models.CharField(max_length=120, blank=True, default="")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VolunteerHoursQuerySet(models.QuerySet):
    def total_hours(self):
        return sum(x.hours for x in self)

class VolunteerHoursManager(models.Manager):
    def aggregate_total_hours(self):
        # общий счетчик для лендинга
        return float(self.get_queryset().aggregate(models.Sum("hours"))["hours__sum"] or 0)

class VolunteerHours(models.Model):
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    hours = models.FloatField(default=0)

    objects = VolunteerHoursManager()

    def __str__(self):
        return f"{self.volunteer} - {self.event}: {self.hours}h"