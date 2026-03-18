from django.urls import path

from .views import (
    public_events,
    event_detail,
    volunteer_dashboard,
    org_dashboard,
    event_create,
    event_update,
    event_delete,
    apply_to_event,
    apply_to_position,
    org_event_workflow,
    application_review,
    application_decline,
    application_assign,
    assignment_confirm,
    assignment_decline,
    assignment_complete,
    assignment_failed,
)

app_name = "events"

urlpatterns = [
    path("public/", public_events, name="public_events"),
    path("public/<int:event_id>/", event_detail, name="event_detail"),

    path("volunteer/", volunteer_dashboard, name="volunteer_dashboard"),
    path("volunteer/events/<int:event_id>/apply/", apply_to_event, name="apply_to_event"),
    path("volunteer/positions/<int:position_id>/apply/", apply_to_position, name="apply_to_position"),
    path("volunteer/assignments/<int:assignment_id>/confirm/", assignment_confirm, name="assignment_confirm"),
    path("volunteer/assignments/<int:assignment_id>/decline/", assignment_decline, name="assignment_decline"),

    path("org/", org_dashboard, name="org_dashboard"),
    path("org/create/", event_create, name="event_create"),
    path("org/<int:event_id>/edit/", event_update, name="event_update"),
    path("org/<int:event_id>/delete/", event_delete, name="event_delete"),
    path("org/<int:event_id>/workflow/", org_event_workflow, name="org_event_workflow"),

    path("org/applications/<int:application_id>/review/", application_review, name="application_review"),
    path("org/applications/<int:application_id>/decline/", application_decline, name="application_decline"),
    path("org/applications/<int:application_id>/assign/", application_assign, name="application_assign"),

    path("org/assignments/<int:assignment_id>/complete/", assignment_complete, name="assignment_complete"),
    path("org/assignments/<int:assignment_id>/failed/", assignment_failed, name="assignment_failed"),
]