from django.contrib import admin
from .models import (
    City,
    District,
    SkillCategory,
    Skill,
    Language,
    VolunteerDirection,
    TaskType,
    AvailabilitySlot,
)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name")


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    search_fields = ("name", "city__name")
    list_display = ("id", "name", "city")
    list_filter = ("city",)


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name", "category")
    list_filter = ("category",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    search_fields = ("name", "code")
    list_display = ("id", "name", "code")


@admin.register(VolunteerDirection)
class VolunteerDirectionAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name")


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name")


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name")