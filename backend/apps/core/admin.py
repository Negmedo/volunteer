from django.contrib import admin
from .models import City, District, Language, SkillCategory, Skill, VolunteerDirection, TaskType
admin.site.register([City, District, Language, SkillCategory, Skill, VolunteerDirection, TaskType])
