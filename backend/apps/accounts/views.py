from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import SignupForm, LoginForm, VolunteerProfileForm
from .models import Role


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    form = SignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Аккаунт успешно создан.")
        return redirect("accounts:dashboard")

    return render(request, "accounts/signup.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    pass


@login_required
def dashboard_router(request):
    role = getattr(getattr(request.user, "profile", None), "role", None)

    if role == Role.ORG:
        return redirect("events:org_dashboard")
    if role == Role.ADMIN:
        return redirect("admin:index")

    return redirect("events:volunteer_dashboard")


@login_required
def volunteer_profile_edit(request):
    role = getattr(getattr(request.user, "profile", None), "role", None)

    if role == Role.ORG:
        return redirect("events:org_dashboard")
    if role == Role.ADMIN:
        return redirect("admin:index")

    volunteer_profile = request.user.volunteer_profile
    form = VolunteerProfileForm(request.POST or None, instance=volunteer_profile)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Анкета волонтёра сохранена.")
        return redirect("events:volunteer_dashboard")

    return render(request, "accounts/volunteer_profile_form.html", {
        "form": form,
        "volunteer_profile": volunteer_profile,
    })