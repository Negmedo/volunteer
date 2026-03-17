from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import Role
from .forms import EventForm, EventRequirementForm
from .models import Event


def public_events(request):
    events = Event.objects.filter(is_public=True).order_by("-created_at")
    return render(request, "events/public_list.html", {"events": events})


@login_required
def volunteer_dashboard(request):
    role = getattr(getattr(request.user, "profile", None), "role", None)

    if role == Role.ORG:
        return redirect("events:org_dashboard")
    if role == Role.ADMIN:
        return redirect("admin:index")

    volunteer_profile = request.user.volunteer_profile
    public_events_qs = Event.objects.filter(is_public=True).order_by("-created_at")[:20]

    return render(request, "events/volunteer_dashboard.html", {
        "events": public_events_qs,
        "volunteer_profile": volunteer_profile,
    })


@login_required
def org_dashboard(request):
    role = getattr(getattr(request.user, "profile", None), "role", None)

    if role != Role.ORG:
        return redirect("accounts:dashboard")

    my_events = Event.objects.filter(created_by=request.user).select_related(
        "city", "district"
    ).order_by("-created_at")

    return render(request, "events/org_dashboard.html", {"events": my_events})


@login_required
def event_create(request):
    role = getattr(getattr(request.user, "profile", None), "role", None)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    event_form = EventForm(request.POST or None)
    requirement_form = EventRequirementForm(request.POST or None)

    if request.method == "POST":
        if event_form.is_valid() and requirement_form.is_valid():
            event = event_form.save(commit=False)
            event.created_by = request.user
            event.save()

            requirement = requirement_form.save(commit=False)
            requirement.event = event
            requirement.save()
            requirement_form.save_m2m()

            messages.success(request, "Мероприятие и требования успешно созданы.")
            return redirect("events:org_dashboard")

    return render(request, "events/org_event_form.html", {
        "event_form": event_form,
        "requirement_form": requirement_form,
        "page_title": "Создание мероприятия",
        "submit_text": "Создать мероприятие",
    })


@login_required
def event_update(request, event_id):
    role = getattr(getattr(request.user, "profile", None), "role", None)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    requirement = getattr(event, "requirement", None)

    event_form = EventForm(request.POST or None, instance=event)
    requirement_form = EventRequirementForm(request.POST or None, instance=requirement)

    if request.method == "POST":
        if event_form.is_valid() and requirement_form.is_valid():
            event = event_form.save()

            requirement = requirement_form.save(commit=False)
            requirement.event = event
            requirement.save()
            requirement_form.save_m2m()

            messages.success(request, "Мероприятие и требования обновлены.")
            return redirect("events:org_dashboard")

    return render(request, "events/org_event_form.html", {
        "event_form": event_form,
        "requirement_form": requirement_form,
        "page_title": "Редактирование мероприятия",
        "submit_text": "Сохранить изменения",
    })


@login_required
def event_delete(request, event_id):
    role = getattr(getattr(request.user, "profile", None), "role", None)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == "POST":
        event.delete()
        messages.success(request, "Мероприятие удалено.")
        return redirect("events:org_dashboard")

    return render(request, "events/event_confirm_delete.html", {"event": event})