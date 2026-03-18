from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.models import Role, VolunteerProfile
from .forms import EventForm, EventRequirementForm, ApplicationForm
from .models import (
    Event,
    EventRequirement,
    EventPosition,
    Application,
    Assignment,
    PositionStatus,
    WorkflowStatus,
)


def _get_role(user):
    return getattr(getattr(user, "profile", None), "role", None)


def _get_or_create_volunteer_profile_for_user(user):
    """
    Ленивое создание анкеты волонтёра.
    Используем только в волонтёрских сценариях.
    """
    return VolunteerProfile.objects.get_or_create(user=user)[0]


def _recalculate_position_state(position: EventPosition):
    active_statuses = [
        WorkflowStatus.ASSIGNED,
        WorkflowStatus.CONFIRMED,
        WorkflowStatus.COMPLETED,
    ]
    active_count = position.assignments.filter(status__in=active_statuses).count()
    position.slots_filled = active_count

    if position.status not in {PositionStatus.CANCELLED, PositionStatus.CLOSED}:
        if active_count >= position.slots_total:
            position.status = PositionStatus.FILLED
        else:
            position.status = PositionStatus.OPEN

    position.save(update_fields=["slots_filled", "status"])


def _sync_legacy_default_position(event: Event):
    """
    Совместимость со старым EventRequirement без ломки matching.
    Для legacy-событий держим одну служебную позицию.
    """
    if not hasattr(event, "requirement"):
        return None

    requirement = event.requirement
    position, _ = EventPosition.objects.get_or_create(
        event=event,
        title="Основная позиция",
        sort_order=0,
        defaults={
            "description": event.description or "Автоматически созданная legacy-позиция.",
        },
    )

    position.description = event.description or position.description
    position.direction = requirement.direction
    position.task_type = requirement.task_type
    position.min_experience_level = requirement.min_experience_level
    position.requires_car = requirement.requires_car
    position.requires_night_shift = requirement.requires_night_shift
    position.allows_other_districts = requirement.allows_other_districts
    position.slots_total = max(requirement.volunteers_needed, 1)
    if position.status not in {PositionStatus.CANCELLED, PositionStatus.CLOSED}:
        position.status = PositionStatus.OPEN
    position.save()

    position.required_skills.set(requirement.required_skills.all())
    position.optional_skills.set(requirement.optional_skills.all())
    position.required_languages.set(requirement.required_languages.all())
    position.preferred_availability_slots.set(requirement.preferred_availability_slots.all())

    _recalculate_position_state(position)
    return position


def public_events(request):
    events = Event.objects.filter(is_public=True).select_related("city", "district").order_by("-created_at")
    return render(request, "events/public_list.html", {"events": events})


def event_detail(request, event_id):
    event = get_object_or_404(
        Event.objects.select_related("city", "district", "created_by"),
        id=event_id,
    )

    if not event.is_public:
        if not request.user.is_authenticated or event.created_by_id != request.user.id:
            messages.error(request, "Мероприятие недоступно.")
            return redirect("events:public_events")

    _sync_legacy_default_position(event)

    positions = event.positions.prefetch_related(
        "required_skills",
        "required_languages",
    ).order_by("sort_order", "id")

    volunteer_profile = None
    my_applications = {}
    my_assignments = {}

    if request.user.is_authenticated and _get_role(request.user) == Role.VOLUNTEER:
        volunteer_profile = VolunteerProfile.objects.filter(user=request.user).first()

        if volunteer_profile:
            my_applications = {
                app.position_id: app
                for app in Application.objects.filter(
                    volunteer_profile=volunteer_profile,
                    position__event=event,
                ).select_related("position")
            }

            my_assignments = {
                item.position_id: item
                for item in Assignment.objects.filter(
                    volunteer_profile=volunteer_profile,
                    position__event=event,
                ).select_related("position")
            }

    open_positions = [
        position for position in positions
        if position.status == PositionStatus.OPEN and position.open_slots > 0
    ]
    can_apply_to_event = len(open_positions) == 1

    return render(request, "events/event_detail.html", {
        "event": event,
        "positions": positions,
        "volunteer_profile": volunteer_profile,
        "my_applications": my_applications,
        "my_assignments": my_assignments,
        "can_apply_to_event": can_apply_to_event,
        "application_form": ApplicationForm(),
    })


@login_required
def volunteer_dashboard(request):
    role = _get_role(request.user)

    if role == Role.ORG:
        return redirect("events:org_dashboard")
    if role == Role.ADMIN:
        return redirect("admin:index")

    volunteer_profile = _get_or_create_volunteer_profile_for_user(request.user)

    public_events_qs = Event.objects.filter(is_public=True).select_related(
        "city", "district"
    ).order_by("-created_at")[:20]

    applications = volunteer_profile.applications.select_related(
        "position",
        "position__event",
        "position__event__city",
    ).order_by("-applied_at")

    assignments = volunteer_profile.assignments.select_related(
        "position",
        "position__event",
        "position__event__city",
    ).order_by("-assigned_at")

    return render(request, "events/volunteer_dashboard.html", {
        "events": public_events_qs,
        "volunteer_profile": volunteer_profile,
        "applications": applications,
        "assignments": assignments,
    })


@login_required
def org_dashboard(request):
    role = _get_role(request.user)

    if role != Role.ORG:
        return redirect("accounts:dashboard")

    my_events = list(
        Event.objects.filter(created_by=request.user).select_related(
            "city", "district"
        ).prefetch_related("positions").order_by("-created_at")
    )

    for event in my_events:
        _sync_legacy_default_position(event)

    return render(request, "events/org_dashboard.html", {"events": my_events})


@login_required
def event_create(request):
    role = _get_role(request.user)
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

            _sync_legacy_default_position(event)

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
    role = _get_role(request.user)
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

            _sync_legacy_default_position(event)

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
    role = _get_role(request.user)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == "POST":
        event.delete()
        messages.success(request, "Мероприятие удалено.")
        return redirect("events:org_dashboard")

    return render(request, "events/event_confirm_delete.html", {"event": event})


@login_required
def apply_to_event(request, event_id):
    role = _get_role(request.user)
    if role != Role.VOLUNTEER:
        return redirect("accounts:dashboard")

    event = get_object_or_404(Event, id=event_id, is_public=True)
    _sync_legacy_default_position(event)

    open_positions = list(
        event.positions.filter(status=PositionStatus.OPEN).order_by("sort_order", "id")
    )
    open_positions = [position for position in open_positions if position.open_slots > 0]

    if not open_positions:
        messages.error(request, "У этого мероприятия сейчас нет открытых позиций для отклика.")
        return redirect("events:event_detail", event_id=event.id)

    if len(open_positions) > 1:
        messages.info(request, "У мероприятия несколько ролей. Выберите конкретную позицию.")
        return redirect("events:event_detail", event_id=event.id)

    return _apply_to_position_impl(request, open_positions[0])


@login_required
def apply_to_position(request, position_id):
    role = _get_role(request.user)
    if role != Role.VOLUNTEER:
        return redirect("accounts:dashboard")

    position = get_object_or_404(
        EventPosition.objects.select_related("event"),
        id=position_id,
    )

    if not position.event.is_public:
        messages.error(request, "Нельзя откликнуться на скрытое мероприятие.")
        return redirect("events:volunteer_dashboard")

    return _apply_to_position_impl(request, position)


def _apply_to_position_impl(request, position: EventPosition):
    if request.method != "POST":
        return redirect("events:event_detail", event_id=position.event_id)

    volunteer_profile = _get_or_create_volunteer_profile_for_user(request.user)

    if position.status != PositionStatus.OPEN or position.open_slots <= 0:
        messages.error(request, "Позиция уже закрыта или мест больше нет.")
        return redirect("events:event_detail", event_id=position.event_id)

    existing_application = Application.objects.filter(
        position=position,
        volunteer_profile=volunteer_profile,
    ).first()
    if existing_application:
        messages.info(request, "Вы уже откликались на эту позицию.")
        return redirect("events:event_detail", event_id=position.event_id)

    existing_assignment = Assignment.objects.filter(
        position=position,
        volunteer_profile=volunteer_profile,
        status__in=[WorkflowStatus.ASSIGNED, WorkflowStatus.CONFIRMED, WorkflowStatus.COMPLETED],
    ).exists()
    if existing_assignment:
        messages.info(request, "У вас уже есть назначение на эту позицию.")
        return redirect("events:event_detail", event_id=position.event_id)

    form = ApplicationForm(request.POST or None)
    if not form.is_valid():
        messages.error(request, "Не удалось отправить отклик.")
        return redirect("events:event_detail", event_id=position.event_id)

    application = form.save(commit=False)
    application.position = position
    application.volunteer_profile = volunteer_profile
    application.status = WorkflowStatus.APPLIED
    application.source = "SELF"
    application.save()

    messages.success(request, "Отклик отправлен.")
    return redirect("events:volunteer_dashboard")


@login_required
def org_event_workflow(request, event_id):
    role = _get_role(request.user)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    event = get_object_or_404(
        Event.objects.select_related("city", "district"),
        id=event_id,
        created_by=request.user,
    )

    _sync_legacy_default_position(event)

    event = Event.objects.select_related("city", "district").prefetch_related(
        Prefetch(
            "positions",
            queryset=EventPosition.objects.prefetch_related(
                "required_skills",
                "required_languages",
                Prefetch(
                    "applications",
                    queryset=Application.objects.select_related(
                        "volunteer_profile",
                        "volunteer_profile__user",
                    ).order_by("-applied_at"),
                ),
                Prefetch(
                    "assignments",
                    queryset=Assignment.objects.select_related(
                        "volunteer_profile",
                        "volunteer_profile__user",
                        "application",
                    ).order_by("-assigned_at"),
                ),
            ).order_by("sort_order", "id"),
        )
    ).get(id=event_id)

    return render(request, "events/org_event_workflow.html", {"event": event})


@login_required
def application_review(request, application_id):
    role = _get_role(request.user)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    application = get_object_or_404(
        Application.objects.select_related("position", "position__event"),
        id=application_id,
        position__event__created_by=request.user,
    )

    if request.method == "POST":
        application.status = WorkflowStatus.REVIEWED
        application.review_comment = request.POST.get("review_comment", "").strip()
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save(update_fields=["status", "review_comment", "reviewed_by", "reviewed_at"])
        messages.success(request, "Отклик переведён в статус reviewed.")

    return redirect("events:org_event_workflow", event_id=application.position.event_id)


@login_required
def application_decline(request, application_id):
    role = _get_role(request.user)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    application = get_object_or_404(
        Application.objects.select_related("position", "position__event"),
        id=application_id,
        position__event__created_by=request.user,
    )

    if request.method == "POST":
        application.status = WorkflowStatus.DECLINED
        application.review_comment = request.POST.get("review_comment", "").strip()
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save(update_fields=["status", "review_comment", "reviewed_by", "reviewed_at"])
        messages.success(request, "Отклик отклонён.")

    return redirect("events:org_event_workflow", event_id=application.position.event_id)


@login_required
def application_assign(request, application_id):
    role = _get_role(request.user)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    application = get_object_or_404(
        Application.objects.select_related(
            "position",
            "position__event",
            "volunteer_profile",
        ),
        id=application_id,
        position__event__created_by=request.user,
    )

    if request.method == "POST":
        position = application.position
        _recalculate_position_state(position)

        if position.status != PositionStatus.OPEN or position.open_slots <= 0:
            messages.error(request, "Назначение невозможно: позиция уже закрыта или мест нет.")
            return redirect("events:org_event_workflow", event_id=position.event_id)

        assignment, created = Assignment.objects.get_or_create(
            position=position,
            volunteer_profile=application.volunteer_profile,
            defaults={
                "application": application,
                "assigned_by": request.user,
                "reliability_snapshot": application.volunteer_profile.reliability_score,
                "notes": request.POST.get("notes", "").strip(),
                "status": WorkflowStatus.ASSIGNED,
            },
        )

        if not created:
            assignment.application = application
            assignment.assigned_by = request.user
            assignment.reliability_snapshot = application.volunteer_profile.reliability_score
            assignment.notes = request.POST.get("notes", "").strip()
            assignment.status = WorkflowStatus.ASSIGNED
            assignment.save()

        application.status = WorkflowStatus.ASSIGNED
        application.reviewed_by = request.user
        application.reviewed_at = timezone.now()
        application.save(update_fields=["status", "reviewed_by", "reviewed_at"])

        _recalculate_position_state(position)
        messages.success(request, "Волонтёр назначен на позицию.")

    return redirect("events:org_event_workflow", event_id=application.position.event_id)


@login_required
def assignment_confirm(request, assignment_id):
    role = _get_role(request.user)
    if role != Role.VOLUNTEER:
        return redirect("accounts:dashboard")

    assignment = get_object_or_404(
        Assignment.objects.select_related("position", "position__event", "application"),
        id=assignment_id,
        volunteer_profile=request.user.volunteer_profile,
    )

    if request.method == "POST":
        assignment.status = WorkflowStatus.CONFIRMED
        assignment.confirmed_at = timezone.now()
        assignment.save(update_fields=["status", "confirmed_at"])

        if assignment.application:
            assignment.application.status = WorkflowStatus.CONFIRMED
            assignment.application.save(update_fields=["status"])

        _recalculate_position_state(assignment.position)
        messages.success(request, "Назначение подтверждено.")

    return redirect("events:volunteer_dashboard")


@login_required
def assignment_decline(request, assignment_id):
    role = _get_role(request.user)
    if role != Role.VOLUNTEER:
        return redirect("accounts:dashboard")

    assignment = get_object_or_404(
        Assignment.objects.select_related("position", "position__event", "application"),
        id=assignment_id,
        volunteer_profile=request.user.volunteer_profile,
    )

    if request.method == "POST":
        assignment.status = WorkflowStatus.DECLINED
        assignment.cancelled_at = timezone.now()
        assignment.save(update_fields=["status", "cancelled_at"])

        if assignment.application:
            assignment.application.status = WorkflowStatus.DECLINED
            assignment.application.save(update_fields=["status"])

        volunteer_profile = assignment.volunteer_profile
        volunteer_profile.cancelled_assignments_count += 1
        volunteer_profile.save(update_fields=["cancelled_assignments_count"])

        _recalculate_position_state(assignment.position)
        messages.success(request, "Назначение отклонено.")

    return redirect("events:volunteer_dashboard")


@login_required
def assignment_complete(request, assignment_id):
    role = _get_role(request.user)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    assignment = get_object_or_404(
        Assignment.objects.select_related("position", "position__event", "application", "volunteer_profile"),
        id=assignment_id,
        position__event__created_by=request.user,
    )

    if request.method == "POST":
        if assignment.status != WorkflowStatus.COMPLETED:
            assignment.status = WorkflowStatus.COMPLETED
            assignment.completed_at = timezone.now()
            assignment.save(update_fields=["status", "completed_at"])

            volunteer_profile = assignment.volunteer_profile
            volunteer_profile.completed_assignments_count += 1
            volunteer_profile.last_assignment_at = assignment.assigned_at
            volunteer_profile.last_completed_assignment_at = timezone.now()
            volunteer_profile.reliability_score = min(float(volunteer_profile.reliability_score) + 5, 100)
            volunteer_profile.save(update_fields=[
                "completed_assignments_count",
                "last_assignment_at",
                "last_completed_assignment_at",
                "reliability_score",
            ])

            if assignment.application:
                assignment.application.status = WorkflowStatus.COMPLETED
                assignment.application.save(update_fields=["status"])

            _recalculate_position_state(assignment.position)
            messages.success(request, "Назначение отмечено как completed.")

    return redirect("events:org_event_workflow", event_id=assignment.position.event_id)


@login_required
def assignment_failed(request, assignment_id):
    role = _get_role(request.user)
    if role != Role.ORG:
        return redirect("accounts:dashboard")

    assignment = get_object_or_404(
        Assignment.objects.select_related("position", "position__event", "application", "volunteer_profile"),
        id=assignment_id,
        position__event__created_by=request.user,
    )

    if request.method == "POST":
        if assignment.status != WorkflowStatus.FAILED:
            assignment.status = WorkflowStatus.FAILED
            assignment.cancelled_at = timezone.now()
            assignment.save(update_fields=["status", "cancelled_at"])

            volunteer_profile = assignment.volunteer_profile
            volunteer_profile.no_show_count += 1
            volunteer_profile.last_assignment_at = assignment.assigned_at
            volunteer_profile.reliability_score = max(float(volunteer_profile.reliability_score) - 10, 0)
            volunteer_profile.save(update_fields=[
                "no_show_count",
                "last_assignment_at",
                "reliability_score",
            ])

            if assignment.application:
                assignment.application.status = WorkflowStatus.FAILED
                assignment.application.save(update_fields=["status"])

            _recalculate_position_state(assignment.position)
            messages.success(request, "Назначение отмечено как failed.")

    return redirect("events:org_event_workflow", event_id=assignment.position.event_id)