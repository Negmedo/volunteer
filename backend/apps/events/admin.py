from django.contrib import admin

from .models import (
    Event,
    EventRequirement,
    EventPosition,
    Application,
    Assignment,
)


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
    search_fields = ("title", "description", "venue_name", "address_text")


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


@admin.register(EventPosition)
class EventPositionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "event",
        "title",
        "status",
        "slots_total",
        "slots_filled",
        "min_experience_level",
        "requires_car",
        "requires_night_shift",
    )
    list_filter = (
        "status",
        "direction",
        "task_type",
        "min_experience_level",
        "requires_car",
        "requires_night_shift",
    )
    search_fields = ("title", "description", "event__title")
    filter_horizontal = (
        "required_skills",
        "optional_skills",
        "required_languages",
        "preferred_availability_slots",
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "position",
        "volunteer_profile",
        "status",
        "source",
        "match_score",
        "reviewed_by",
        "applied_at",
    )
    list_filter = ("status", "source", "position__event")
    search_fields = (
        "position__title",
        "position__event__title",
        "volunteer_profile__user__username",
        "volunteer_profile__user__email",
    )


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "position",
        "volunteer_profile",
        "status",
        "assigned_by",
        "assigned_at",
        "completed_at",
    )
    list_filter = ("status", "position__event")
    search_fields = (
        "position__title",
        "position__event__title",
        "volunteer_profile__user__username",
        "volunteer_profile__user__email",
    )