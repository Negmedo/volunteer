from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.forms.formsets import DELETION_FIELD_NAME
from apps.core.models import City

from apps.applications.models import Application, Assignment
from apps.events.models import EventPosition
from .forms import (
    SignupForm,
    LoginForm,
    ProfileForm,
    UserIdentityForm,
    VolunteerProfileForm,
    VolunteerLanguageFormSetFactory,
    VolunteerSkillFormSetFactory,
)
from .models import Profile, Role, VolunteerProfile, VolunteerAvailability


def _ensure_minimum_form_rows(formset_factory, instance, prefix, post_data=None, minimum=1):
    formset = formset_factory(post_data or None, instance=instance, prefix=prefix)
    if post_data is None and formset.total_form_count() == 0:
        formset = formset_factory(None, instance=instance, prefix=prefix, queryset=formset.queryset.none())
        formset.extra = minimum
    return formset


def _collect_form_errors(*forms_or_formsets):
    errors = []
    for item in forms_or_formsets:
        if hasattr(item, 'errors'):
            if isinstance(item.errors, list):
                for error_dict in item.errors:
                    if hasattr(error_dict, 'items'):
                        for field, field_errors in error_dict.items():
                            for error in field_errors:
                                errors.append(f"{field}: {error}")
            else:
                for field, field_errors in item.errors.items():
                    for error in field_errors:
                        errors.append(f"{field}: {error}")
        if hasattr(item, 'non_form_errors'):
            for error in item.non_form_errors():
                errors.append(str(error))
    return errors


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
    language_formset = _ensure_minimum_form_rows(VolunteerLanguageFormSetFactory, volunteer_profile, "langs", request.POST, minimum=1)
    skill_formset = _ensure_minimum_form_rows(VolunteerSkillFormSetFactory, volunteer_profile, "skills", request.POST, minimum=1)

    if request.method == "POST":
        forms_valid = all([
            user_form.is_valid(),
            profile_form.is_valid(),
            volunteer_form.is_valid(),
            language_formset.is_valid(),
            skill_formset.is_valid(),
        ])
        if forms_valid:
            with transaction.atomic():
                user_form.save()
                profile_form.save()
                vp = volunteer_form.save()
                language_formset.instance = vp
                language_formset.save()
                skill_formset.instance = vp
                skill_formset.save()
                vp.availability_items.all().delete()
                for item in volunteer_form.cleaned_data.get("availability_matrix", []):
                    weekday, time_of_day = item.split(":", 1)
                    VolunteerAvailability.objects.create(volunteer_profile=vp, weekday=int(weekday), time_of_day=time_of_day)
                vp.recalculate_completion()
                vp.save()
            messages.success(request, "Анкета сохранена")
            return redirect("accounts:volunteer_profile")
        else:
            messages.error(request, "Форма сохранена не была. Исправьте отмеченные поля ниже.")

    district_map = {str(city.id): [{"id": d.id, "name": d.name} for d in city.districts.all()] for city in City.objects.prefetch_related("districts")}
    return render(
        request,
        "accounts/volunteer_profile_form.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "volunteer_form": volunteer_form,
            "language_formset": language_formset,
            "skill_formset": skill_formset,
            "volunteer_profile": volunteer_profile,
            "district_map": district_map,
            "form_errors": _collect_form_errors(user_form, profile_form, volunteer_form, language_formset, skill_formset),
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