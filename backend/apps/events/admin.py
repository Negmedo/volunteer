from django.contrib import admin

from .models import Event, EventRequirement, VolunteerHours


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "city",
        "district",
        "is_public",
        "created_by",
        "created_at",
    )
    list_filter = ("is_public", "city", "district", "created_at")
    search_fields = ("title", "description")


@admin.register(EventRequirement)
class EventRequirementAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "direction",
        "task_type",
        "min_experience_level",
        "requires_car",
        "requires_night_shift",
        "volunteers_needed",
    )
    list_filter = (
        "direction",
        "task_type",
        "min_experience_level",
        "requires_car",
        "requires_night_shift",
    )
    filter_horizontal = (
        "required_skills",
        "optional_skills",
        "required_languages",
        "preferred_availability_slots",
    )


@admin.register(VolunteerHours)
class VolunteerHoursAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "event", "hours")
    search_fields = ("volunteer__username", "event__title")