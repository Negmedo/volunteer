"""
Жизненный цикл отклика и назначения.
"""

import csv
import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import VolunteerProfile, Role
from apps.events.models import EventPosition, Event
from apps.notifications.models import Notification
from .models import Application, Assignment, ApplicationStatus


def _get_volunteer_profile(user):
    profile, _ = VolunteerProfile.objects.get_or_create(user=user)
    return profile


@login_required
def position_detail(request, position_id):
    position = get_object_or_404(
        EventPosition.objects.select_related(
            'event', 'event__city', 'event__district', 'direction', 'task_type'
        ).prefetch_related(
            'required_skill_items__skill',
            'optional_skill_items__skill',
            'language_requirements__language',
            'availability_requirements',
        ),
        id=position_id,
        event__is_public=True,
    )

    already_applied = False
    already_assigned = False

    if request.user.is_authenticated and getattr(request.user.profile, 'role', None) == Role.VOLUNTEER:
        vp = _get_volunteer_profile(request.user)
        already_applied = Application.objects.filter(position=position, volunteer_profile=vp).exists()
        already_assigned = Assignment.objects.filter(
            position=position, volunteer_profile=vp
        ).exclude(status=ApplicationStatus.DECLINED).exists()

    return render(request, 'applications/position_detail.html', {
        'position': position,
        'already_applied': already_applied,
        'already_assigned': already_assigned,
    })


@login_required
def apply_to_position(request, position_id):
    if request.user.profile.role != Role.VOLUNTEER:
        return redirect('accounts:dashboard')

    position = get_object_or_404(
        EventPosition.objects.select_related('event'),
        id=position_id,
        event__is_public=True,
    )
    volunteer_profile = _get_volunteer_profile(request.user)

    if Application.objects.filter(position=position, volunteer_profile=volunteer_profile).exists():
        messages.info(request, 'Вы уже откликались на эту роль.')
        return redirect('accounts:volunteer_dashboard')

    if request.method == 'POST':
        motivation_text = request.POST.get('motivation_text', '').strip()
        Application.objects.create(
            position=position,
            volunteer_profile=volunteer_profile,
            motivation_text=motivation_text,
        )
        Notification.objects.create(
            user=position.event.created_by,
            title='Новый отклик',
            body=f'На роль «{position.title}» откликнулся '
                 f'{request.user.get_full_name() or request.user.username}.',
        )
        messages.success(request, 'Отклик успешно отправлен.')
        return redirect('accounts:volunteer_dashboard')

    return render(request, 'applications/apply_form.html', {'position': position})


@login_required
def assignment_confirm(request, assignment_id):
    assignment = get_object_or_404(
        Assignment, id=assignment_id, volunteer_profile__user=request.user
    )
    if request.method == 'POST' and assignment.status == ApplicationStatus.INVITED:
        assignment.status = ApplicationStatus.CONFIRMED
        assignment.save(update_fields=['status'])
        Application.objects.filter(
            position=assignment.position,
            volunteer_profile=assignment.volunteer_profile,
        ).update(status=ApplicationStatus.CONFIRMED)
        Notification.objects.create(
            user=assignment.position.event.created_by,
            title='Волонтёр подтвердил участие',
            body=f'{assignment.volunteer_profile.user.get_full_name() or assignment.volunteer_profile.user.username} '
                 f'подтвердил участие в роли «{assignment.position.title}».',
        )
        messages.success(request, 'Участие подтверждено.')
    return redirect('accounts:volunteer_dashboard')


@login_required
def assignment_decline(request, assignment_id):
    assignment = get_object_or_404(
        Assignment, id=assignment_id, volunteer_profile__user=request.user
    )
    if request.method == 'POST' and assignment.status == ApplicationStatus.INVITED:
        assignment.status = ApplicationStatus.DECLINED
        assignment.hours_worked = 0
        assignment.coordinator_rating = None
        assignment.save(update_fields=['status', 'hours_worked', 'coordinator_rating'])
        Application.objects.filter(
            position=assignment.position,
            volunteer_profile=assignment.volunteer_profile,
        ).update(status=ApplicationStatus.DECLINED)
        assignment.volunteer_profile.recalculate_stats()
        messages.success(request, 'Участие отклонено.')
    return redirect('accounts:volunteer_dashboard')


@login_required
def assign_application(request, application_id):
    application = get_object_or_404(
        Application, id=application_id,
        position__event__created_by=request.user
    )
    assignment, _ = Assignment.objects.get_or_create(
        position=application.position,
        volunteer_profile=application.volunteer_profile,
        defaults={'assigned_by': request.user},
    )
    assignment.status = ApplicationStatus.INVITED
    assignment.assigned_by = request.user
    assignment.hours_worked = 0
    assignment.coordinator_rating = None
    assignment.save(update_fields=['status', 'assigned_by', 'hours_worked', 'coordinator_rating'])

    application.status = ApplicationStatus.INVITED
    application.save(update_fields=['status'])

    Notification.objects.create(
        user=application.volunteer_profile.user,
        title='Приглашение на роль',
        body=f'Организатор приглашает вас на роль «{application.position.title}» '
             f'в мероприятии «{application.position.event.title}». Подтвердите или отклоните участие в личном кабинете.',
    )
    messages.success(request, 'Приглашение отправлено волонтёру.')
    return redirect('events:event_detail', event_id=application.position.event_id)


@login_required
def mark_completed(request, assignment_id):
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        position__event__created_by=request.user,
        status=ApplicationStatus.CONFIRMED,
    )

    if request.method == 'POST':
        hours = request.POST.get('hours_worked', '0').strip()
        rating = request.POST.get('coordinator_rating', '').strip()
        note = request.POST.get('coordinator_note', '').strip()

        try:
            assignment.hours_worked = max(0, int(hours))
        except ValueError:
            assignment.hours_worked = 0

        if rating and rating.isdigit() and 1 <= int(rating) <= 5:
            assignment.coordinator_rating = int(rating)
        else:
            assignment.coordinator_rating = None

        assignment.coordinator_note = note
        assignment.status = ApplicationStatus.COMPLETED
        assignment.save()

        Application.objects.filter(
            position=assignment.position,
            volunteer_profile=assignment.volunteer_profile,
        ).update(status=ApplicationStatus.COMPLETED)

        assignment.volunteer_profile.recalculate_stats()

        Notification.objects.create(
            user=assignment.volunteer_profile.user,
            title='Участие завершено',
            body=f'Ваше участие в роли «{assignment.position.title}» отмечено как выполненное. '
                 f'Часов добавлено: {assignment.hours_worked}.'
                 + (f' Оценка: {assignment.coordinator_rating}/5.' if assignment.coordinator_rating else ''),
        )
        messages.success(request, 'Участие отмечено как выполненное. Часы и статистика пересчитаны суммарно по завершённым назначениям.')

    return redirect('events:event_detail', event_id=assignment.position.event_id)


@login_required
def mark_failed(request, assignment_id):
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        position__event__created_by=request.user,
        status=ApplicationStatus.CONFIRMED,
    )

    if request.method == 'POST':
        note = request.POST.get('coordinator_note', '').strip()
        assignment.coordinator_note = note
        assignment.hours_worked = 0
        assignment.coordinator_rating = None
        assignment.status = ApplicationStatus.FAILED
        assignment.save(update_fields=['status', 'coordinator_note', 'hours_worked', 'coordinator_rating'])

        Application.objects.filter(
            position=assignment.position,
            volunteer_profile=assignment.volunteer_profile,
        ).update(status=ApplicationStatus.FAILED)

        assignment.volunteer_profile.recalculate_stats()

        Notification.objects.create(
            user=assignment.volunteer_profile.user,
            title='Неявка зафиксирована',
            body=f'По роли «{assignment.position.title}» зафиксирована неявка. '
                 'Это влияет на ваш рейтинг надёжности.',
        )
        messages.warning(request, 'Неявка зафиксирована. Статистика волонтёра обновлена.')

    return redirect('events:event_detail', event_id=assignment.position.event_id)


@login_required
def export_assignments_csv(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    assignments = Assignment.objects.filter(
        position__event=event,
    ).select_related(
        'volunteer_profile__user',
        'volunteer_profile__city',
        'volunteer_profile__district',
        'position',
        'assigned_by',
    ).order_by('position__title', 'volunteer_profile__user__last_name')

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = (
        f'attachment; filename="assignments_{event_id}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow([
        'Роль', 'Фамилия', 'Имя', 'Email', 'Телефон', 'Город', 'Район',
        'Статус', 'Часы', 'Оценка (1-5)', 'Комментарий', 'Дата назначения',
    ])

    for a in assignments:
        vp = a.volunteer_profile
        user = vp.user
        profile = getattr(user, 'profile', None)
        writer.writerow([
            a.position.title,
            user.last_name,
            user.first_name,
            user.email,
            profile.phone if profile else '',
            str(vp.city) if vp.city else '',
            str(vp.district) if vp.district else '',
            a.get_status_display(),
            a.hours_worked,
            a.coordinator_rating or '',
            a.coordinator_note,
            a.created_at.strftime('%d.%m.%Y'),
        ])

    return response


@login_required
def import_volunteers_csv(request, event_id):
    if request.user.profile.role != Role.ORG:
        return redirect('accounts:dashboard')

    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        raw = uploaded_file.read()
        try:
            text = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            text = raw.decode('utf-8', errors='ignore')

        csv_file = io.StringIO(text)
        reader = csv.DictReader(csv_file)
        first_position = event.positions.order_by('id').first()
        if not first_position:
            messages.error(request, 'Сначала создайте хотя бы одну роль в мероприятии.')
            return redirect('applications:import_volunteers_csv', event_id=event.id)

        created_count = 0
        for row in reader:
            email = (row.get('email') or '').strip().lower()
            if not email:
                continue
            vp = VolunteerProfile.objects.filter(user__email__iexact=email).select_related('user').first()
            if not vp:
                continue
            _, created = Application.objects.get_or_create(
                position=first_position,
                volunteer_profile=vp,
                defaults={'status': ApplicationStatus.NEW},
            )
            if created:
                created_count += 1

        if created_count:
            messages.success(request, f'Импорт завершён. Добавлено откликов: {created_count}.')
        else:
            messages.info(request, 'Импорт завершён, новых откликов не добавлено.')
        return redirect('events:event_detail', event_id=event.id)

    return render(request, 'applications/import_csv.html', {'event': event})
