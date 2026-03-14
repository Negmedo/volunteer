from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.accounts.models import Role
from .models import Event

def public_events(request):
    events = Event.objects.filter(is_public=True).order_by("-created_at")
    return render(request, "events/public_list.html", {"events": events})

@login_required
def volunteer_dashboard(request):
    # любой не-ORG будет видеть “волонтерский” кабинет для MVP
    events = Event.objects.filter(is_public=True).order_by("-created_at")[:20]
    return render(request, "events/volunteer_dashboard.html", {"events": events})

@login_required
def org_dashboard(request):
    role = getattr(getattr(request.user, "profile", None), "role", None)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    my_events = Event.objects.filter(created_by=request.user).order_by("-created_at")
    return render(request, "events/org_dashboard.html", {"events": my_events})