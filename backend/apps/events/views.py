from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.models import Role
from apps.core.models import City
from .models import Event, EventPosition, EventPositionAvailabilityRequirement
from .forms import EventForm, EventPositionForm, RequiredSkillFormSetFactory, OptionalSkillFormSetFactory, LanguageReqFormSetFactory


def _require_org(user):
    return getattr(user.profile, 'role', None) == Role.ORG


@login_required
def org_dashboard(request):
    if not _require_org(request.user):
        return redirect('accounts:dashboard')
    events = Event.objects.filter(created_by=request.user).prefetch_related('positions').order_by('-created_at')
    return render(request, 'events/org_dashboard.html', {'events': events})


@login_required
def event_create(request):
    if not _require_org(request.user):
        return redirect('accounts:dashboard')
    form = EventForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.created_by = request.user
        event.save()
        messages.success(request, 'Мероприятие создано')
        return redirect('events:position_create', event_id=event.id)
    district_map = {str(city.id): [{"id": d.id, "name": d.name} for d in city.districts.all()] for city in City.objects.prefetch_related('districts')}
    return render(request, 'events/event_form.html', {'form': form, 'page_title': 'Создать мероприятие', 'district_map': district_map})


@login_required
def event_update(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    form = EventForm(request.POST or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Мероприятие обновлено')
        return redirect('events:event_detail', event_id=event.id)
    district_map = {str(city.id): [{"id": d.id, "name": d.name} for d in city.districts.all()] for city in City.objects.prefetch_related('districts')}
    return render(request, 'events/event_form.html', {'form': form, 'page_title': 'Редактировать мероприятие', 'event': event, 'district_map': district_map})


@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Мероприятие удалено')
        return redirect('events:org_dashboard')
    return render(request, 'events/event_delete.html', {'event': event})


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(
        Event.objects.prefetch_related(
            'positions__required_skill_items__skill',
            'positions__optional_skill_items__skill',
            'positions__language_requirements__language',
            'positions__applications__volunteer_profile__user',
        ),
        id=event_id,
        created_by=request.user,
    )
    return render(request, 'events/event_detail.html', {'event': event})


@login_required
def position_create(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    position = EventPosition(event=event)
    form = EventPositionForm(request.POST or None, instance=position, prefix='position')
    required_formset = RequiredSkillFormSetFactory(request.POST or None, instance=position, prefix='required')
    optional_formset = OptionalSkillFormSetFactory(request.POST or None, instance=position, prefix='optional')
    language_formset = LanguageReqFormSetFactory(request.POST or None, instance=position, prefix='langs')
    if request.method == 'POST' and all([form.is_valid(), required_formset.is_valid(), optional_formset.is_valid(), language_formset.is_valid()]):
        with transaction.atomic():
            position = form.save(commit=False)
            position.event = event
            position.save()
            required_formset.instance = position
            required_formset.save()
            optional_formset.instance = position
            optional_formset.save()
            language_formset.instance = position
            language_formset.save()
            position.availability_requirements.all().delete()
            for item in form.cleaned_data.get('availability_matrix', []):
                weekday, time_of_day = item.split(':', 1)
                EventPositionAvailabilityRequirement.objects.create(position=position, weekday=int(weekday), time_of_day=time_of_day)
        messages.success(request, 'Роль создана')
        return redirect('events:event_detail', event_id=event.id)
    return render(request, 'events/position_form.html', {'event': event, 'form': form, 'required_formset': required_formset, 'optional_formset': optional_formset, 'language_formset': language_formset, 'page_title': 'Создать роль'})


@login_required
def position_update(request, position_id):
    position = get_object_or_404(EventPosition, id=position_id, event__created_by=request.user)
    form = EventPositionForm(request.POST or None, instance=position, prefix='position')
    required_formset = RequiredSkillFormSetFactory(request.POST or None, instance=position, prefix='required')
    optional_formset = OptionalSkillFormSetFactory(request.POST or None, instance=position, prefix='optional')
    language_formset = LanguageReqFormSetFactory(request.POST or None, instance=position, prefix='langs')
    if request.method == 'POST' and all([form.is_valid(), required_formset.is_valid(), optional_formset.is_valid(), language_formset.is_valid()]):
        with transaction.atomic():
            form.save()
            required_formset.save()
            optional_formset.save()
            language_formset.save()
            position.availability_requirements.all().delete()
            for item in form.cleaned_data.get('availability_matrix', []):
                weekday, time_of_day = item.split(':', 1)
                EventPositionAvailabilityRequirement.objects.create(position=position, weekday=int(weekday), time_of_day=time_of_day)
        messages.success(request, 'Роль обновлена')
        return redirect('events:event_detail', event_id=position.event_id)
    return render(request, 'events/position_form.html', {'event': position.event, 'form': form, 'required_formset': required_formset, 'optional_formset': optional_formset, 'language_formset': language_formset, 'page_title': 'Редактировать роль'})


@login_required
def position_delete(request, position_id):
    position = get_object_or_404(EventPosition, id=position_id, event__created_by=request.user)
    event_id = position.event_id
    if request.method == 'POST':
        position.delete()
        messages.success(request, 'Роль удалена')
        return redirect('events:event_detail', event_id=event_id)
    return render(request, 'events/position_delete.html', {'position': position})
