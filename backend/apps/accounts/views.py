from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from .forms import SignupForm, LoginForm
from .models import Role


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("landing")

    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
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
        return redirect("/admin/")
    # по умолчанию volunteer
    return redirect("events:volunteer_dashboard")