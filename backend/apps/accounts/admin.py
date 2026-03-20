from django.contrib import admin

from .models import Profile, VolunteerProfile, Role


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "city", "phone")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email", "phone")


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "get_user_role",
        "get_matching_state",
        "city",
        "district",
        "experience_level",
        "has_car",
        "ready_for_night_shifts",
        "profile_completion_percent",
        "is_profile_completed",
    )
    list_filter = (
        "is_available_for_matching",
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

    @admin.display(description="Роль пользователя")
    def get_user_role(self, obj):
        profile = getattr(obj.user, "profile", None)
        if not profile:
            return "—"
        return profile.get_role_display()

    @admin.display(description="Состояние для matching")
    def get_matching_state(self, obj):
        profile = getattr(obj.user, "profile", None)
        role = getattr(profile, "role", None)

        if role != Role.VOLUNTEER:
            return "Отключён (не волонтёр)"

        if not obj.is_available_for_matching:
            return "Отключён"

        if not obj.is_profile_completed:
            return "Не заполнен"

        return "Активен"