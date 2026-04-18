from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from apps.core.models import City, Skill, Language

from apps.applications.models import Application, Assignment
from apps.events.models import EventPosition
from .forms import (
    SignupForm,
    LoginForm,
    ProfileForm,
    UserIdentityForm,
    VolunteerProfileForm,
)
from .models import (
    Profile, Role, VolunteerProfile, VolunteerAvailability, VolunteerSkill, VolunteerLanguage,
    SkillLevel, LanguageLevel,
)


def _collect_form_errors(*forms):
    errors = []
    for item in forms:
        if hasattr(item, 'errors'):
            for field, field_errors in item.errors.items():
                for error in field_errors:
                    errors.append(f"{field}: {error}")
        if hasattr(item, 'non_field_errors'):
            for error in item.non_field_errors():
                errors.append(str(error))
    return errors


def _selected_values_map(post_data, selected_name, level_prefix):
    selected = set(post_data.getlist(selected_name))
    return {int(pk): post_data.get(f'{level_prefix}{pk}') for pk in selected if str(pk).isdigit()}


def _build_skill_catalog(profile=None, post_data=None):
    selected = {}
    if post_data is not None:
        selected = _selected_values_map(post_data, 'skill_selected', 'skill_level_')
    elif profile is not None:
        selected = {item.skill_id: item.level for item in profile.skills.all()}

    catalog = []
    for skill in Skill.objects.select_related('category').all():
        catalog.append({
            'id': skill.id,
            'name': skill.name,
            'category': skill.category.name,
            'checked': skill.id in selected,
            'level': selected.get(skill.id, SkillLevel.BEGINNER),
        })
    return catalog


def _build_language_catalog(profile=None, post_data=None):
    selected = {}
    if post_data is not None:
        selected = _selected_values_map(post_data, 'language_selected', 'language_level_')
    elif profile is not None:
        selected = {item.language_id: item.level for item in profile.languages.all()}

    catalog = []
    for language in Language.objects.all():
        catalog.append({
            'id': language.id,
            'name': language.name,
            'checked': language.id in selected,
            'level': selected.get(language.id, LanguageLevel.CONVERSATIONAL),
        })
    return catalog


def _save_skills_and_languages(profile, post_data):
    skill_levels = _selected_values_map(post_data, 'skill_selected', 'skill_level_')
    language_levels = _selected_values_map(post_data, 'language_selected', 'language_level_')

    VolunteerSkill.objects.filter(volunteer_profile=profile).delete()
    VolunteerLanguage.objects.filter(volunteer_profile=profile).delete()

    VolunteerSkill.objects.bulk_create([
        VolunteerSkill(volunteer_profile=profile, skill_id=skill_id, level=level or SkillLevel.BEGINNER)
        for skill_id, level in skill_levels.items()
    ])
    VolunteerLanguage.objects.bulk_create([
        VolunteerLanguage(volunteer_profile=profile, language_id=language_id, level=level or LanguageLevel.CONVERSATIONAL)
        for language_id, level in language_levels.items()
    ])


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        Profile.objects.get_or_create(user=user)
        VolunteerProfile.objects.get_or_create(user=user)
        login(request, user)
        return redirect("accounts:dashboard")
    return render(request, "accounts/signup.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из аккаунта.")
    return redirect("landing:home")


@login_required
def dashboard_router(request):
    role = getattr(request.user.profile, "role", Role.VOLUNTEER)
    if role == Role.ORG:
        return redirect("events:org_dashboard")
    if role == Role.ADMIN:
        return redirect("admin:index")
    return redirect("accounts:volunteer_dashboard")


@login_required
def volunteer_profile_edit(request):
    Profile.objects.get_or_create(user=request.user)
    volunteer_profile, _ = VolunteerProfile.objects.get_or_create(user=request.user)

    user_form = UserIdentityForm(request.POST or None, instance=request.user, prefix="user")
    profile_form = ProfileForm(request.POST or None, instance=request.user.profile, prefix="contact")
    volunteer_form = VolunteerProfileForm(request.POST or None, instance=volunteer_profile, prefix="volunteer")

    if request.method == "POST":
        forms_valid = all([user_form.is_valid(), profile_form.is_valid(), volunteer_form.is_valid()])
        if forms_valid:
            with transaction.atomic():
                user_form.save()
                profile_form.save()
                vp = volunteer_form.save(commit=False)
                vp.ready_for_night_shifts = not bool(volunteer_form.cleaned_data.get("avoid_night_shifts"))
                vp.save()
                volunteer_form.save_m2m()
                _save_skills_and_languages(vp, request.POST)
                vp.availability_items.all().delete()
                for item in volunteer_form.cleaned_data.get("availability_matrix", []):
                    weekday, time_of_day = item.split(":", 1)
                    VolunteerAvailability.objects.create(volunteer_profile=vp, weekday=int(weekday), time_of_day=time_of_day)
                vp.recalculate_completion()
                vp.save()
            messages.success(request, "Анкета сохранена")
            return redirect("accounts:volunteer_profile")
        messages.error(request, "Форма сохранена не была. Исправьте отмеченные поля ниже.")

    district_map = {str(city.id): [{"id": d.id, "name": d.name} for d in city.districts.all()] for city in City.objects.prefetch_related("districts")}
    return render(
        request,
        "accounts/volunteer_profile_form.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "volunteer_form": volunteer_form,
            "volunteer_profile": volunteer_profile,
            "district_map": district_map,
            "form_errors": _collect_form_errors(user_form, profile_form, volunteer_form),
            "skill_catalog": _build_skill_catalog(volunteer_profile, request.POST if request.method == 'POST' else None),
            "language_catalog": _build_language_catalog(volunteer_profile, request.POST if request.method == 'POST' else None),
            "skill_level_choices": SkillLevel.choices,
            "language_level_choices": LanguageLevel.choices,
        },
    )


@login_required
def volunteer_dashboard(request):
    if getattr(request.user.profile, "role", Role.VOLUNTEER) != Role.VOLUNTEER:
        return redirect("accounts:dashboard")
    volunteer_profile, _ = VolunteerProfile.objects.get_or_create(user=request.user)
    available_positions = (
        EventPosition.objects.select_related("event", "event__city", "event__district", "direction", "task_type")
        .prefetch_related("required_skill_items__skill")
        .filter(event__is_public=True)
        .exclude(applications__volunteer_profile=volunteer_profile)
        .exclude(assignments__volunteer_profile=volunteer_profile)
        .order_by("event__start_date", "event__title", "title")
    )
    my_applications = (
        Application.objects.select_related("position", "position__event")
        .filter(volunteer_profile=volunteer_profile)
        .order_by("-created_at")
    )
    my_assignments = (
        Assignment.objects.select_related("position", "position__event")
        .filter(volunteer_profile=volunteer_profile)
        .order_by("-created_at")
    )
    return render(
        request,
        "accounts/volunteer_dashboard.html",
        {
            "volunteer_profile": volunteer_profile,
            "available_positions": available_positions,
            "my_applications": my_applications,
            "my_assignments": my_assignments,
        },
    )


@login_required
def volunteer_profile_detail(request, profile_id):
    role = getattr(request.user.profile, "role", Role.VOLUNTEER)
    if role not in [Role.ORG, Role.ADMIN]:
        messages.error(request, "Просмотр анкеты доступен только организатору.")
        return redirect("accounts:dashboard")

    volunteer_profile = get_object_or_404(
        VolunteerProfile.objects.select_related("user", "city", "district", "user__profile")
        .prefetch_related(
            "languages__language",
            "skills__skill",
            "availability_items",
            "preferred_directions",
            "preferred_task_types",
            "applications__position__event",
            "assignments__position__event",
        ),
        id=profile_id,
    )

    recent_applications = volunteer_profile.applications.select_related("position", "position__event").order_by("-created_at")[:10]
    recent_assignments = volunteer_profile.assignments.select_related("position", "position__event").order_by("-created_at")[:10]

    return render(
        request,
        "accounts/volunteer_profile_detail.html",
        {
            "volunteer_profile": volunteer_profile,
            "recent_applications": recent_applications,
            "recent_assignments": recent_assignments,
        },
    )
