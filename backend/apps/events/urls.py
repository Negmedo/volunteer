from django.urls import path
from .views import org_dashboard, event_create, event_update, event_delete, event_detail, position_create, position_update, position_delete
app_name = 'events'
urlpatterns = [
    path('org/', org_dashboard, name='org_dashboard'),
    path('org/events/new/', event_create, name='event_create'),
    path('org/events/<int:event_id>/', event_detail, name='event_detail'),
    path('org/events/<int:event_id>/edit/', event_update, name='event_update'),
    path('org/events/<int:event_id>/delete/', event_delete, name='event_delete'),
    path('org/events/<int:event_id>/positions/new/', position_create, name='position_create'),
    path('org/positions/<int:position_id>/edit/', position_update, name='position_update'),
    path('org/positions/<int:position_id>/delete/', position_delete, name='position_delete'),
]
