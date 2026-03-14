from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "is_public", "created_by", "created_at")
    list_filter = ("is_public", "city")
    search_fields = ("title", "description")
