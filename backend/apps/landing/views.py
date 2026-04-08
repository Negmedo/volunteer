from django.shortcuts import render
from django.contrib.auth.models import User
from apps.events.models import Event
from apps.accounts.models import VolunteerProfile

def home(request):
    stats = {
        'users_count': User.objects.count(),
        'events_count': Event.objects.count(),
        'public_events_count': Event.objects.filter(is_public=True).count(),
        'hours_count': sum(
            VolunteerProfile.objects.values_list('volunteer_hours', flat=True)
        ) if VolunteerProfile.objects.exists() else 0,
    }
    public_events = Event.objects.filter(is_public=True).order_by('-start_date')[:5]
    return render(request, 'landing/home.html', {
        'stats': stats,
        'public_events': public_events,
    })