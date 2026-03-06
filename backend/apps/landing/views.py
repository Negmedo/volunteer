from django.shortcuts import render
from django.contrib.auth import get_user_model
from apps.events.models import Event
from apps.events.models import VolunteerHours

User = get_user_model()

def landing_view(request):
    users_count = User.objects.count()
    events_count = Event.objects.count()
    hours_total = VolunteerHours.objects.aggregate_total_hours()

    public_events = Event.objects.filter(is_public=True).order_by("-created_at")[:10]

    return render(request, "landing/main.html", {
        "users_count": users_count,
        "events_count": events_count,
        "hours_total": hours_total,
        "public_events": public_events,
    })

def auth_view(request):
    # ИСПРАВЛЕНИЕ ЗДЕСЬ: мы добавили "accounts/" перед названием файла
    return render(request, 'accounts/auth.html')