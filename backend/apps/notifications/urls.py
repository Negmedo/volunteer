from django.urls import path
from .views import notification_list, mark_all_read
app_name = 'notifications'
urlpatterns = [
    path('', notification_list, name='list'),
    path('read-all/', mark_all_read, name='mark_all_read'),
]
