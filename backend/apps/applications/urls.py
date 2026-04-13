from django.urls import path
from .views import (
    position_detail,
    apply_to_position,
    assign_application,
    assignment_confirm,
    assignment_decline,
    mark_completed,
    mark_failed,
    export_assignments_csv,
    import_volunteers_csv,
)

app_name = 'applications'

urlpatterns = [
    # Волонтёр
    path('positions/<int:position_id>/', position_detail, name='position_detail'),
    path('positions/<int:position_id>/apply/', apply_to_position, name='apply_to_position'),
    path('assignments/<int:assignment_id>/confirm/', assignment_confirm, name='assignment_confirm'),
    path('assignments/<int:assignment_id>/decline/', assignment_decline, name='assignment_decline'),

    # Организатор — управление откликами
    path('applications/<int:application_id>/assign/', assign_application, name='assign_application'),
    path('assignments/<int:assignment_id>/completed/', mark_completed, name='mark_completed'),
    path('assignments/<int:assignment_id>/failed/', mark_failed, name='mark_failed'),

    # Экспорт / импорт CSV
    path('events/<int:event_id>/export-csv/', export_assignments_csv, name='export_assignments_csv'),
    path('events/<int:event_id>/import-csv/', import_volunteers_csv, name='import_volunteers_csv'),
]