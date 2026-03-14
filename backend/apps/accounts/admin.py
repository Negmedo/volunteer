from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    verbose_name = "Профиль"
    verbose_name_plural = "Профиль"


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "city", "phone")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")

    def delete_model(self, request, obj):
        """
        Если удаляют профиль из админки, удаляем связанного пользователя целиком.
        Тогда профиль тоже исчезнет каскадно.
        """
        user = obj.user
        user.delete()

    def delete_queryset(self, request, queryset):
        """
        Массовое удаление профилей в админке тоже должно удалять пользователей,
        а не только строки profile.
        """
        user_ids = list(queryset.values_list("user_id", flat=True))
        User.objects.filter(id__in=user_ids).delete()