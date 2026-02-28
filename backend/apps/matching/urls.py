from django.urls import path
from .views import matching_stub

urlpatterns = [
    path("", matching_stub, name="matching"),
]