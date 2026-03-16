from django.urls import path

from .views import (
    public_events,
    volunteer_dashboard,
    org_dashboard,
    event_create,
    event_update,
    event_delete,
)

urlpatterns = [
    path("public/", public_events, name="public_events"),
    path("volunteer/", volunteer_dashboard, name="volunteer_dashboard"),
    path("org/", org_dashboard, name="org_dashboard"),
    path("org/create/", event_create, name="event_create"),
    path("org/<int:event_id>/edit/", event_update, name="event_update"),
    path("org/<int:event_id>/delete/", event_delete, name="event_delete"),
]