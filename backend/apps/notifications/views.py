from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Notification

@login_required
def notification_list(request):
    items = Notification.objects.filter(user=request.user)
    return render(request, 'accounts/notifications.html', {'notifications': items})

@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:list')
