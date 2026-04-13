from django.shortcuts import render
from django.contrib.auth.models import User
from apps.events.models import Event
from apps.accounts.models import VolunteerProfile


def home(request):
    # volunteer_hours теперь считается по реальным завершённым назначениям
    # через recalculate_stats() — просто суммируем актуальные значения
    hours_count = sum(
        VolunteerProfile.objects.values_list('volunteer_hours', flat=True)
    ) if VolunteerProfile.objects.exists() else 0

    stats = {
        'users_count': User.objects.filter(profile__role='VOLUNTEER').count(),
        'events_count': Event.objects.filter(is_public=True).count(),
        'hours_count': hours_count,
    }
    return render(request, 'landing/home.html', {'stats': stats})