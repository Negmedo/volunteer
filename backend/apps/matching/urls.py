from django.urls import path

from .views import matching_stub, event_matching_results

app_name = "matching"

urlpatterns = [
    path("", matching_stub, name="matching"),
    path("event/<int:event_id>/", event_matching_results, name="event_matching_results"),
]