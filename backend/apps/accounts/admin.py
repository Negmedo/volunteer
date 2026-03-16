from django.contrib import admin

from .models import Profile, VolunteerProfile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "city", "phone")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email", "phone")


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "city",
        "district",
        "experience_level",
        "has_car",
        "ready_for_night_shifts",
        "profile_completion_percent",
        "is_profile_completed",
    )
    list_filter = (
        "city",
        "district",
        "experience_level",
        "has_car",
        "ready_for_night_shifts",
        "is_profile_completed",
    )
    search_fields = ("user__username", "user__email")
    filter_horizontal = (
        "languages",
        "skills",
        "preferred_directions",
        "preferred_task_types",
        "availability_slots",
    )