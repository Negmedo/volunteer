"""
apps/applications/views.py
--------------------------
Полный жизненный цикл отклика и назначения:

  Волонтёр:
    position_detail      — просмотр роли перед откликом
    apply_to_position    — GET показывает форму с motivation_text, POST отправляет
    assignment_confirm   — волонтёр подтверждает участие
    assignment_decline   — волонтёр отказывается

  Организатор:
    assign_application   — назначить волонтёра
    mark_completed       — отметить явку + часы + оценка → auto recalculate
    mark_failed          — отметить неявку → auto recalculate
    export_assignments_csv — выгрузка CSV назначений по мероприятию
    import_volunteers_csv  — импорт CSV волонтёров для подбора
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


# ── Вспомогательные ─────────────────────────────────────────

def _get_volunteer_profile(user):
    profile, _ = VolunteerProfile.objects.get_or_create(user=user)
    return profile


# ── Волонтёрские вьюхи ──────────────────────────────────────

@login_required
def position_detail(request, position_id):
    """
    Страница просмотра роли до отклика.
    Волонтёр видит полное описание: навыки, языки, ограничения, условия.
    """
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
    """
    GET  — показывает форму с полем motivation_text и кнопкой подтверждения.
    POST — создаёт Application, уведомляет организатора.
    Отклик не отправляется «вслепую» — только через форму подтверждения.
    """
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

    return render(request, 'applications/apply_form.html', {
        'position': position,
    })


@login_required
def assignment_confirm(request, assignment_id):
    assignment = get_object_or_404(
        Assignment, id=assignment_id, volunteer_profile__user=request.user
    )
    if request.method == 'POST':
        assignment.status = ApplicationStatus.CONFIRMED
        assignment.save(update_fields=['status'])
        # Обновить статус заявки тоже
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
    if request.method == 'POST':
        assignment.status = ApplicationStatus.DECLINED
        assignment.save(update_fields=['status'])
        Application.objects.filter(
            position=assignment.position,
            volunteer_profile=assignment.volunteer_profile,
        ).update(status=ApplicationStatus.DECLINED)
        # Пересчёт статистики после отказа
        assignment.volunteer_profile.recalculate_stats()
        messages.success(request, 'Участие отклонено.')
    return redirect('accounts:volunteer_dashboard')


# ── Организаторские вьюхи ────────────────────────────────────

@login_required
def assign_application(request, application_id):
    """Назначить волонтёра на роль из списка откликов."""
    application = get_object_or_404(
        Application, id=application_id,
        position__event__created_by=request.user
    )
    assignment, _ = Assignment.objects.get_or_create(
        position=application.position,
        volunteer_profile=application.volunteer_profile,
        defaults={'assigned_by': request.user},
    )
    assignment.status = ApplicationStatus.ASSIGNED
    assignment.assigned_by = request.user
    assignment.save(update_fields=['status', 'assigned_by'])

    application.status = ApplicationStatus.ASSIGNED
    application.save(update_fields=['status'])

    Notification.objects.create(
        user=application.volunteer_profile.user,
        title='Новое назначение',
        body=f'Вас назначили на роль «{application.position.title}» '
             f'в мероприятии «{application.position.event.title}».',
    )
    messages.success(request, 'Волонтёр назначен.')
    return redirect('events:event_detail', event_id=application.position.event_id)


@login_required
def mark_completed(request, assignment_id):
    """
    Организатор отмечает: волонтёр пришёл и выполнил роль.
    Принимает часы (hours_worked) и оценку (coordinator_rating 1–5).
    После сохранения автоматически пересчитывает статистику волонтёра.
    """
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        position__event__created_by=request.user,
        status__in=[ApplicationStatus.ASSIGNED, ApplicationStatus.CONFIRMED],
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

        assignment.coordinator_note = note
        assignment.status = ApplicationStatus.COMPLETED
        assignment.save()

        # Обновить статус заявки
        Application.objects.filter(
            position=assignment.position,
            volunteer_profile=assignment.volunteer_profile,
        ).update(status=ApplicationStatus.COMPLETED)

        # Автоматический пересчёт показателей волонтёра
        assignment.volunteer_profile.recalculate_stats()

        Notification.objects.create(
            user=assignment.volunteer_profile.user,
            title='Участие завершено',
            body=f'Ваше участие в роли «{assignment.position.title}» отмечено как выполненное. '
                 f'Часов: {assignment.hours_worked}.'
                 + (f' Оценка: {assignment.coordinator_rating}/5.' if assignment.coordinator_rating else ''),
        )
        messages.success(request, 'Участие отмечено как выполненное. Статистика волонтёра обновлена.')

    return redirect('events:event_detail', event_id=assignment.position.event_id)


@login_required
def mark_failed(request, assignment_id):
    """
    Организатор отмечает: волонтёр не явился или не выполнил роль.
    Автоматически снижает attendance_rate.
    """
    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        position__event__created_by=request.user,
        status__in=[ApplicationStatus.ASSIGNED, ApplicationStatus.CONFIRMED],
    )

    if request.method == 'POST':
        note = request.POST.get('coordinator_note', '').strip()
        assignment.coordinator_note = note
        assignment.status = ApplicationStatus.FAILED
        assignment.save(update_fields=['status', 'coordinator_note'])

        Application.objects.filter(
            position=assignment.position,
            volunteer_profile=assignment.volunteer_profile,
        ).update(status=ApplicationStatus.FAILED)

        # Автоматический пересчёт
        assignment.volunteer_profile.recalculate_stats()

        Notification.objects.create(
            user=assignment.volunteer_profile.user,
            title='Неявка зафиксирована',
            body=f'По роли «{assignment.position.title}» зафиксирована неявка. '
                 'Это влияет на ваш рейтинг надёжности.',
        )
        messages.warning(request, 'Неявка зафиксирована. Статистика волонтёра обновлена.')

    return redirect('events:event_detail', event_id=assignment.position.event_id)


# ── Экспорт CSV ──────────────────────────────────────────────

@login_required
def export_assignments_csv(request, event_id):
    """
    Экспорт CSV списка назначений по мероприятию.
    Организатор скачивает файл для отчётности.
    """
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
        'Роль',
        'Фамилия',
        'Имя',
        'Email',
        'Телефон',
        'Город',
        'Район',
        'Статус',
        'Часы',
        'Оценка (1-5)',
        'Комментарий',
        'Дата назначения',
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


# ── Импорт CSV ───────────────────────────────────────────────

@login_required
def import_volunteers_csv(request, event_id):
    """
    Импорт CSV-файла со списком волонтёров для подбора.
    Формат: email, first_name, last_name (первая строка — заголовок).
    Если пользователь с таким email существует — добавляет его Application на указанную позицию.

    Требование руководителя: отдельный импорт CSV от организатора.
    """
    if request.user.profile.role != Role.ORG:
        return redirect('accounts:dashboard')

    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        position_id = request.POST.get('position_id')

        if not csv_file:
            messages.error(request, 'Файл не загружен.')
            return redirect('events:event_detail', event_id=event_id)

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Загрузите файл в формате CSV.')
            return redirect('events:event_detail', event_id=event_id)

        position = None
        if position_id:
            position = get_object_or_404(EventPosition, id=position_id, event=event)

        try:
            decoded = csv_file.read().decode('utf-8-sig')
            reader = csv.DictReader(io.StringIO(decoded))

            from django.contrib.auth.models import User

            created_count = 0
            skipped_count = 0
            errors = []

            for row_num, row in enumerate(reader, start=2):
                email = (row.get('email') or row.get('Email') or '').strip().lower()
                if not email:
                    errors.append(f'Строка {row_num}: нет email')
                    continue

                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    errors.append(f'Строка {row_num}: пользователь {email} не найден в системе')
                    skipped_count += 1
                    continue

                if getattr(getattr(user, 'profile', None), 'role', None) != Role.VOLUNTEER:
                    errors.append(f'Строка {row_num}: {email} не является волонтёром')
                    skipped_count += 1
                    continue

                if position:
                    vp, _ = VolunteerProfile.objects.get_or_create(user=user)
                    _, app_created = Application.objects.get_or_create(
                        position=position,
                        volunteer_profile=vp,
                        defaults={'motivation_text': 'Импортирован из CSV'},
                    )
                    if app_created:
                        created_count += 1
                    else:
                        skipped_count += 1

            msg = f'Импорт завершён: добавлено {created_count}, пропущено {skipped_count}.'
            if errors:
                msg += f' Ошибки: {"; ".join(errors[:5])}'
                if len(errors) > 5:
                    msg += f' и ещё {len(errors) - 5}.'
            messages.success(request, msg)

        except Exception as exc:
            messages.error(request, f'Ошибка при чтении файла: {exc}')

        return redirect('events:event_detail', event_id=event_id)

    # GET — форма выбора файла и позиции
    return render(request, 'applications/import_csv.html', {
        'event': event,
        'positions': event.positions.all(),
    })