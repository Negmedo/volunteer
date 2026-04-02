from django.urls import path
from .views import apply_to_position, assign_application, assignment_confirm, assignment_decline
app_name = 'applications'
urlpatterns = [
    path('positions/<int:position_id>/apply/', apply_to_position, name='apply_to_position'),
    path('applications/<int:application_id>/assign/', assign_application, name='assign_application'),
    path('assignments/<int:assignment_id>/confirm/', assignment_confirm, name='assignment_confirm'),
    path('assignments/<int:assignment_id>/decline/', assignment_decline, name='assignment_decline'),
]
