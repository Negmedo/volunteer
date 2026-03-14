from django.shortcuts import render
from django.contrib.auth import get_user_model
from apps.events.models import Event

User = get_user_model()


def landing_view(request):
    users_count = User.objects.count()
    events_count = Event.objects.count()

    public_events = Event.objects.filter(is_public=True).order_by("-created_at")[:10]

    return render(request, "landing/index.html", {
        "users_count": users_count,
        "events_count": events_count,
        "public_events": public_events,
    })