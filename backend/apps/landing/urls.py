from django.urls import path
from .views import landing_view, auth_view

urlpatterns = [
    # Твоя текущая главная страница (index.html)
    path("", landing_view, name="landing"),
    
    # Новый путь для страницы входа/регистрации (auth.html)
    path("auth/", auth_view, name="auth"),
]