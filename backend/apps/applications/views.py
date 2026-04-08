from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Application, Assignment, ApplicationStatus
from apps.events.models import EventPosition
from apps.accounts.models import VolunteerProfile, Role
from apps.notifications.models import Notification

@login_required
def apply_to_position(request, position_id):
    if request.user.profile.role != Role.VOLUNTEER:
        return redirect('accounts:dashboard')
    position = get_object_or_404(EventPosition, id=position_id)
    volunteer_profile, _ = VolunteerProfile.objects.get_or_create(user=request.user)
    application, created = Application.objects.get_or_create(position=position, volunteer_profile=volunteer_profile)
    if created:
        Notification.objects.create(user=position.event.created_by, title='Новый отклик', body=f'На роль «{position.title}» откликнулся {request.user.get_full_name() or request.user.username}.')
        messages.success(request, 'Отклик отправлен')
    else:
        messages.info(request, 'Вы уже откликались на эту роль')
    return redirect('accounts:dashboard')

@login_required
def assign_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, position__event__created_by=request.user)
    assignment, _ = Assignment.objects.get_or_create(position=application.position, volunteer_profile=application.volunteer_profile, defaults={'assigned_by': request.user})
    application.status = ApplicationStatus.ASSIGNED
    application.save(update_fields=['status'])
    Notification.objects.create(user=application.volunteer_profile.user, title='Новое назначение', body=f'Вас назначили на роль: {application.position.title}')
    messages.success(request, 'Волонтёр назначен')
    return redirect('events:event_detail', event_id=application.position.event_id)

@login_required
def assignment_confirm(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, volunteer_profile__user=request.user)
    assignment.status = ApplicationStatus.CONFIRMED
    assignment.save(update_fields=['status'])
    messages.success(request, 'Участие подтверждено')
    return redirect('accounts:dashboard')

@login_required
def assignment_decline(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, volunteer_profile__user=request.user)
    assignment.status = ApplicationStatus.DECLINED
    assignment.save(update_fields=['status'])
    messages.success(request, 'Участие отклонено')
    return redirect('accounts:dashboard')
