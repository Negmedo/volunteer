from django.urls import path
from .views import notification_list, mark_all_read, delete_notification, clear_notifications

app_name = 'notifications'

urlpatterns = [
    path('', notification_list, name='list'),
    path('read-all/', mark_all_read, name='mark_all_read'),
    path('delete/<int:notification_id>/', delete_notification, name='delete'),
    path('clear/', clear_notifications, name='clear'),
]