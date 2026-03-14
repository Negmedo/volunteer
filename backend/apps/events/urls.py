from django.urls import path
from .views import org_dashboard, public_events, volunteer_dashboard

app_name = "events"

urlpatterns = [
    path("public/", public_events, name="public_events"),
    path("volunteer/", volunteer_dashboard, name="volunteer_dashboard"),
    path("org/", org_dashboard, name="org_dashboard"),
]