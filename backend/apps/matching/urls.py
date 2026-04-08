from django.urls import path
from .views import position_matching, assign_candidate

app_name = 'matching'

urlpatterns = [
    path('positions/<int:position_id>/', position_matching, name='position_matching'),
    path('positions/<int:position_id>/assign/<int:volunteer_id>/', assign_candidate, name='assign_candidate'),
]
