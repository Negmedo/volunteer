from django.db import models


class City(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ["name"]

    def __str__(self):
        return self.name


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="districts")
    name = models.CharField(max_length=120)

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"
        unique_together = ("city", "name")
        ordering = ["city__name", "name"]

    def __str__(self):
        return f"{self.city.name} / {self.name}"


class SkillCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Категория навыка"
        verbose_name_plural = "Категории навыков"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=120, unique=True)
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="skills"
    )

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class VolunteerDirection(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Направление волонтёрства"
        verbose_name_plural = "Направления волонтёрства"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Тип задачи"
        verbose_name_plural = "Типы задач"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AvailabilitySlot(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Слот доступности"
        verbose_name_plural = "Слоты доступности"
        ordering = ["name"]

    def __str__(self):
        return self.name