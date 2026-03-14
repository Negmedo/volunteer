from django.urls import path
from .views import UserLoginView, UserLogoutView, dashboard_router, signup_view

app_name = "accounts"

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("dashboard/", dashboard_router, name="dashboard"),
]