from django.shortcuts import render
from django.contrib.auth.models import User
from apps.events.models import Event
from apps.accounts.models import VolunteerProfile

def home(request):
    stats = {
        'users_count': User.objects.count(),
        'events_count': Event.objects.count(),
        'hours_count': sum(VolunteerProfile.objects.values_list('volunteer_hours', flat=True)) if VolunteerProfile.objects.exists() else 0,
    }
    return render(request, 'landing/home.html', {'stats': stats})
