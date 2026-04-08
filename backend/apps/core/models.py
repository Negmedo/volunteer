from django.db import models

class City(models.Model):
    name = models.CharField(max_length=120, unique=True)
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name

class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="districts")
    name = models.CharField(max_length=120)
    class Meta:
        ordering = ["city__name", "name"]
        unique_together = [("city", "name")]
    def __str__(self):
        return f"{self.city.name} — {self.name}"

class Language(models.Model):
    name = models.CharField(max_length=60, unique=True)
    code = models.CharField(max_length=10, unique=True)
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name

class SkillCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ["sort_order", "name"]
    def __str__(self):
        return self.name

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=120, unique=True)
    class Meta:
        ordering = ["category__sort_order", "name"]
    def __str__(self):
        return self.name

class VolunteerDirection(models.Model):
    name = models.CharField(max_length=120, unique=True)
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name

class TaskType(models.Model):
    name = models.CharField(max_length=120, unique=True)
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name
