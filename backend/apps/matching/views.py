from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.models import Role
from apps.events.models import EventPosition
from apps.applications.models import Assignment, Application, ApplicationStatus
from apps.notifications.models import Notification
from .services import run_position_matching


@login_required
def position_matching(request, position_id):
    position = get_object_or_404(EventPosition, id=position_id, event__created_by=request.user)
    matching_data = run_position_matching(position)
    return render(request, 'matching/position_matching.html', {'position': position, **matching_data})


@login_required
def assign_candidate(request, position_id, volunteer_id):
    if request.user.profile.role != Role.ORG:
        return redirect('accounts:dashboard')
    position = get_object_or_404(EventPosition, id=position_id, event__created_by=request.user)
    application, _ = Application.objects.get_or_create(position=position, volunteer_profile_id=volunteer_id)
    application.status = ApplicationStatus.INVITED
    application.save(update_fields=['status'])

    assignment, _ = Assignment.objects.get_or_create(
        position=position,
        volunteer_profile_id=volunteer_id,
        defaults={'assigned_by': request.user},
    )
    assignment.status = ApplicationStatus.INVITED
    assignment.assigned_by = request.user
    assignment.hours_worked = 0
    assignment.coordinator_rating = None
    assignment.save()

    Notification.objects.create(
        user=assignment.volunteer_profile.user,
        title='Приглашение на роль',
        body=f'Организатор приглашает вас на роль: {position.title}. Подтвердите участие в личном кабинете.',
    )
    messages.success(request, 'Приглашение отправлено. Волонтёр должен подтвердить участие сам.')
    return redirect('matching:position_matching', position_id=position_id)
