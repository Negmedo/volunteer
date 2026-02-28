from django.urls import path
from .views import public_events, volunteer_dashboard, org_dashboard

urlpatterns = [
    path("public/", public_events, name="public_events"),
    path("volunteer/", volunteer_dashboard, name="volunteer_dashboard"),
    path("org/", org_dashboard, name="org_dashboard"),
]