from django.urls import path
from .views import signup_view, UserLoginView, logout_view, dashboard_router, volunteer_profile_edit, volunteer_dashboard

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_router, name='dashboard'),
    path('volunteer/', volunteer_dashboard, name='volunteer_dashboard'),
    path('volunteer/profile/', volunteer_profile_edit, name='volunteer_profile'),
]
