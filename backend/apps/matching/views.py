from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import Role
from apps.events.models import Event
from .services import run_matching_for_event


@login_required
def matching_stub(request):
    return render(request, "matching/index.html")


@login_required
def event_matching_results(request, event_id):
    role = getattr(getattr(request.user, "profile", None), "role", None)

    if role != Role.ORG:
        return redirect("/accounts/dashboard/")

    event = get_object_or_404(
        Event.objects.select_related(
            "city",
            "district",
            "created_by",
            "requirement",
            "requirement__direction",
            "requirement__task_type",
        ),
        id=event_id,
        created_by=request.user,
    )

    if not hasattr(event, "requirement"):
        return render(request, "matching/results.html", {
            "event": event,
            "results": [],
            "warning": "Для мероприятия пока не заполнены требования.",
        })

    results = run_matching_for_event(event)

    return render(request, "matching/results.html", {
        "event": event,
        "results": results,
        "warning": None,
    })