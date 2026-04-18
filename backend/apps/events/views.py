from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.models import Role, SkillLevel, LanguageLevel
from apps.core.models import City, Skill, Language
from .models import (
    Event, EventPosition, EventPositionAvailabilityRequirement,
    EventPositionRequiredSkill, EventPositionOptionalSkill, EventPositionLanguageRequirement,
)
from .forms import EventForm, EventPositionForm


def _require_org(user):
    return getattr(user.profile, 'role', None) == Role.ORG


def _selected_values_map(post_data, selected_name, level_prefix):
    selected = set(post_data.getlist(selected_name))
    return {int(pk): post_data.get(f'{level_prefix}{pk}') for pk in selected if str(pk).isdigit()}


def _build_skill_catalog(position=None, post_data=None):
    required_selected = {}
    optional_selected = {}
    if post_data is not None:
        required_selected = _selected_values_map(post_data, 'required_skills', 'req_skill_level_')
        optional_selected = _selected_values_map(post_data, 'optional_skills', 'opt_skill_level_')
        for skill_id, level in required_selected.items():
            optional_selected.setdefault(skill_id, level)
    elif position is not None and position.pk:
        required_selected = {item.skill_id: item.min_level for item in position.required_skill_items.all()}
        optional_selected = {item.skill_id: item.min_level for item in position.optional_skill_items.all()}

    catalog = []
    for skill in Skill.objects.select_related('category').all():
        catalog.append({
            'id': skill.id,
            'name': skill.name,
            'category': skill.category.name,
            'required_checked': skill.id in required_selected,
            'optional_checked': skill.id in optional_selected,
            'required_level': required_selected.get(skill.id, SkillLevel.BEGINNER),
            'optional_level': optional_selected.get(skill.id, SkillLevel.BEGINNER),
        })
    return catalog


def _build_language_catalog(position=None, post_data=None):
    selected = {}
    if post_data is not None:
        selected = _selected_values_map(post_data, 'required_languages', 'lang_level_')
    elif position is not None and position.pk:
        selected = {item.language_id: item.min_level for item in position.language_requirements.all()}

    catalog = []
    for language in Language.objects.all():
        catalog.append({
            'id': language.id,
            'name': language.name,
            'checked': language.id in selected,
            'level': selected.get(language.id, LanguageLevel.CONVERSATIONAL),
        })
    return catalog


def _save_position_requirements(position, post_data):
    required_skills = _selected_values_map(post_data, 'required_skills', 'req_skill_level_')
    optional_skills = _selected_values_map(post_data, 'optional_skills', 'opt_skill_level_')
    languages = _selected_values_map(post_data, 'required_languages', 'lang_level_')

    for skill_id, level in required_skills.items():
        optional_skills.setdefault(skill_id, level)

    EventPositionRequiredSkill.objects.filter(position=position).delete()
    EventPositionOptionalSkill.objects.filter(position=position).delete()
    EventPositionLanguageRequirement.objects.filter(position=position).delete()

    EventPositionRequiredSkill.objects.bulk_create([
        EventPositionRequiredSkill(position=position, skill_id=skill_id, min_level=level or SkillLevel.BEGINNER)
        for skill_id, level in required_skills.items()
    ])
    EventPositionOptionalSkill.objects.bulk_create([
        EventPositionOptionalSkill(position=position, skill_id=skill_id, min_level=level or SkillLevel.BEGINNER)
        for skill_id, level in optional_skills.items()
    ])
    EventPositionLanguageRequirement.objects.bulk_create([
        EventPositionLanguageRequirement(position=position, language_id=language_id, min_level=level or LanguageLevel.CONVERSATIONAL)
        for language_id, level in languages.items()
    ])


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
            'positions__assignments__volunteer_profile__user',
            'positions__assignments__volunteer_profile',
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
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            position = form.save(commit=False)
            position.event = event
            position.save()
            _save_position_requirements(position, request.POST)
            position.availability_requirements.all().delete()
            for item in form.cleaned_data.get('availability_matrix', []):
                weekday, time_of_day = item.split(':', 1)
                EventPositionAvailabilityRequirement.objects.create(position=position, weekday=int(weekday), time_of_day=time_of_day)
        messages.success(request, 'Роль создана')
        return redirect('events:event_detail', event_id=event.id)
    return render(request, 'events/position_form.html', {
        'event': event, 'form': form, 'page_title': 'Создать роль',
        'skill_catalog': _build_skill_catalog(position, request.POST if request.method == 'POST' else None),
        'language_catalog': _build_language_catalog(position, request.POST if request.method == 'POST' else None),
        'skill_level_choices': SkillLevel.choices, 'language_level_choices': LanguageLevel.choices,
    })


@login_required
def position_update(request, position_id):
    position = get_object_or_404(EventPosition, id=position_id, event__created_by=request.user)
    event = position.event
    form = EventPositionForm(request.POST or None, instance=position, prefix='position')
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            position = form.save()
            _save_position_requirements(position, request.POST)
            position.availability_requirements.all().delete()
            for item in form.cleaned_data.get('availability_matrix', []):
                weekday, time_of_day = item.split(':', 1)
                EventPositionAvailabilityRequirement.objects.create(position=position, weekday=int(weekday), time_of_day=time_of_day)
        messages.success(request, 'Роль обновлена')
        return redirect('events:event_detail', event_id=event.id)
    return render(request, 'events/position_form.html', {
        'event': event, 'form': form, 'page_title': 'Редактировать роль',
        'skill_catalog': _build_skill_catalog(position, request.POST if request.method == 'POST' else None),
        'language_catalog': _build_language_catalog(position, request.POST if request.method == 'POST' else None),
        'skill_level_choices': SkillLevel.choices, 'language_level_choices': LanguageLevel.choices,
    })


@login_required
def position_delete(request, position_id):
    position = get_object_or_404(EventPosition, id=position_id, event__created_by=request.user)
    event_id = position.event_id
    if request.method == 'POST':
        position.delete()
        messages.success(request, 'Роль удалена')
        return redirect('events:event_detail', event_id=event_id)
    return render(request, 'events/position_delete.html', {'position': position})
