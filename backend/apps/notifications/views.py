from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Notification


@login_required
def notification_list(request):
    items = Notification.objects.filter(user=request.user)
    return render(request, 'accounts/notifications.html', {'notifications': items})


@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:list')


@login_required
def delete_notification(request, notification_id):
    item = get_object_or_404(Notification, id=notification_id, user=request.user)
    if request.method == 'POST':
        item.delete()
    return redirect('notifications:list')


@login_required
def clear_notifications(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user).delete()
    return redirect('notifications:list')