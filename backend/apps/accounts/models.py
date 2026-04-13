from django.conf import settings
from django.db import models
from apps.core.models import City, District, Language, Skill, VolunteerDirection, TaskType


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Администратор"
    ORG = "ORG", "Организация"
    VOLUNTEER = "VOLUNTEER", "Волонтёр"
    MODERATOR = "MODERATOR", "Модератор"


class Gender(models.TextChoices):
    MALE = "MALE", "Мужской"
    FEMALE = "FEMALE", "Женский"


class LanguageLevel(models.TextChoices):
    BASIC = "BASIC", "Базовый"
    CONVERSATIONAL = "CONVERSATIONAL", "Разговорный"
    FLUENT = "FLUENT", "Свободный"


class SkillLevel(models.TextChoices):
    BEGINNER = "BEGINNER", "Начальный"
    INTERMEDIATE = "INTERMEDIATE", "Средний"
    ADVANCED = "ADVANCED", "Продвинутый"
    PROFESSIONAL = "PROFESSIONAL", "Профессиональный"


class TimeOfDay(models.TextChoices):
    MORNING = "MORNING", "Утро"
    DAY = "DAY", "День"
    EVENING = "EVENING", "Вечер"


class ParticipationGoal(models.TextChoices):
    RESUME = "RESUME", "Опыт для резюме"
    SOCIAL = "SOCIAL", "Социальная миссия"
    PRACTICE = "PRACTICE", "Практика от вуза"
    CERTIFICATE = "CERTIFICATE", "За сертификат / благодарственное письмо"


WEEKDAY_CHOICES = [
    (1, "Понедельник"),
    (2, "Вторник"),
    (3, "Среда"),
    (4, "Четверг"),
    (5, "Пятница"),
    (6, "Суббота"),
    (7, "Воскресенье"),
]


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VOLUNTEER)
    phone = models.CharField(max_length=50, blank=True, default="")
    organization_name = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class VolunteerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="volunteer_profile"
    )
    gender = models.CharField(max_length=24, choices=Gender.choices, blank=True, default="")
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, related_name="volunteers"
    )
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, blank=True, related_name="volunteers"
    )
    availability_start_date = models.DateField(null=True, blank=True)
    availability_end_date = models.DateField(null=True, blank=True)
    ready_for_night_shifts = models.BooleanField(default=False)
    can_travel = models.BooleanField(default=False)
    has_car = models.BooleanField(default=False)
    physical_work_ok = models.BooleanField(default=True)
    carry_heavy_ok = models.BooleanField(default=True)
    restrictions_note = models.TextField(blank=True, default="")
    avoid_night_shifts = models.BooleanField(default=False)
    avoid_outdoor_winter_work = models.BooleanField(default=False)
    avoid_large_crowds = models.BooleanField(default=False)
    participation_goal = models.CharField(
        max_length=32, choices=ParticipationGoal.choices, blank=True, default=""
    )
    motivation_text = models.TextField(blank=True, default="")
    preferred_directions = models.ManyToManyField(
        VolunteerDirection, blank=True, related_name="preferred_by_volunteers"
    )
    preferred_task_types = models.ManyToManyField(
        TaskType, blank=True, related_name="preferred_by_volunteers"
    )

    # ── Статистика (автоматически пересчитывается) ──────────
    completed_events_count = models.PositiveIntegerField(default=0)
    volunteer_hours = models.PositiveIntegerField(default=0)

    # attendance_rate: пришёл / (пришёл + не явился) * 100
    # Считается автоматически по статусам completed/failed назначений
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # coordinator_rating: среднее всех оценок координаторов (1–5)
    coordinator_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    # response_speed_hours: среднее время ответа на назначение (не автоматизировано пока)
    response_speed_hours = models.PositiveIntegerField(default=0)

    profile_completion_percent = models.PositiveSmallIntegerField(default=0)
    is_profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Анкета: {self.user.get_full_name() or self.user.username}"

    def recalculate_completion(self):
        """Пересчёт процента заполненности профиля."""
        checks = [
            bool(self.user.first_name.strip()),
            bool(self.user.last_name.strip()),
            bool(self.user.email.strip()),
            bool(getattr(self.user, "profile", None) and self.user.profile.phone.strip()),
            bool(self.gender),
            bool(self.birth_year),
            bool(self.city_id),
            bool(self.district_id),
            self.languages.exists(),
            self.skills.exists(),
            self.availability_items.exists(),
            bool(self.availability_start_date and self.availability_end_date),
            self.preferred_directions.exists(),
            self.preferred_task_types.exists(),
            bool(self.participation_goal),
            bool(self.motivation_text.strip()),
        ]
        filled = sum(1 for c in checks if c)
        self.profile_completion_percent = int((filled / len(checks)) * 100)
        self.is_profile_completed = self.profile_completion_percent >= 75

    def recalculate_stats(self):
        """
        Автоматический пересчёт показателей надёжности по истории назначений.

        attendance_rate:
          = completed / (completed + failed) * 100
          Организатор фиксирует факт (пришёл/не пришёл), система считает процент.

        coordinator_rating:
          = среднее всех оценок по завершённым назначениям (только те, где оценка выставлена).

        volunteer_hours:
          = сумма hours_worked по всем completed-назначениям.

        completed_events_count:
          = количество completed-назначений.
        """
        from apps.applications.models import Assignment, ApplicationStatus

        all_assignments = Assignment.objects.filter(volunteer_profile=self)

        completed = all_assignments.filter(status=ApplicationStatus.COMPLETED)
        failed = all_assignments.filter(status=ApplicationStatus.FAILED)

        completed_count = completed.count()
        failed_count = failed.count()
        total_resolved = completed_count + failed_count

        # attendance_rate
        if total_resolved > 0:
            self.attendance_rate = round(completed_count / total_resolved * 100, 2)
        else:
            self.attendance_rate = 0

        # coordinator_rating — среднее только по назначениям с оценкой
        rated = completed.filter(coordinator_rating__isnull=False)
        if rated.exists():
            total_rating = sum(a.coordinator_rating for a in rated)
            self.coordinator_rating = round(total_rating / rated.count(), 2)
        else:
            self.coordinator_rating = 0

        # volunteer_hours
        hours_qs = completed.values_list('hours_worked', flat=True)
        self.volunteer_hours = sum(h for h in hours_qs if h)

        # completed_events_count
        self.completed_events_count = completed_count

        self.save(update_fields=[
            'attendance_rate',
            'coordinator_rating',
            'volunteer_hours',
            'completed_events_count',
        ])


class VolunteerLanguage(models.Model):
    volunteer_profile = models.ForeignKey(
        VolunteerProfile, on_delete=models.CASCADE, related_name="languages"
    )
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="volunteer_profiles")
    level = models.CharField(
        max_length=20, choices=LanguageLevel.choices, default=LanguageLevel.CONVERSATIONAL
    )

    class Meta:
        unique_together = [("volunteer_profile", "language")]

    def __str__(self):
        return f"{self.volunteer_profile.user.username}: {self.language} {self.level}"


class VolunteerSkill(models.Model):
    volunteer_profile = models.ForeignKey(
        VolunteerProfile, on_delete=models.CASCADE, related_name="skills"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="volunteer_profiles")
    level = models.CharField(
        max_length=20, choices=SkillLevel.choices, default=SkillLevel.BEGINNER
    )

    class Meta:
        unique_together = [("volunteer_profile", "skill")]

    def __str__(self):
        return f"{self.volunteer_profile.user.username}: {self.skill}"


class VolunteerAvailability(models.Model):
    volunteer_profile = models.ForeignKey(
        VolunteerProfile, on_delete=models.CASCADE, related_name="availability_items"
    )
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    time_of_day = models.CharField(max_length=16, choices=TimeOfDay.choices)

    class Meta:
        unique_together = [("volunteer_profile", "weekday", "time_of_day")]
        ordering = ["weekday", "time_of_day"]

    def __str__(self):
        return f"{self.volunteer_profile.user.username}: {self.weekday}/{self.time_of_day}"