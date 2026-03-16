from dataclasses import dataclass

from apps.accounts.models import VolunteerProfile
from apps.events.models import Event


@dataclass
class MatchExplanation:
    reasons: list[str]
    hard_filter_passed: bool


def _get_ids(queryset):
    return set(queryset.values_list("id", flat=True))


def hard_filter_volunteers(event: Event):
    """
    Этап 1. Жёсткая фильтрация.
    Отсекаем тех, кто точно не подходит.
    """

    if not hasattr(event, "requirement"):
        return VolunteerProfile.objects.none()

    requirement = event.requirement

    volunteers = VolunteerProfile.objects.select_related(
        "user",
        "city",
        "district",
    ).prefetch_related(
        "skills",
        "languages",
        "preferred_directions",
        "preferred_task_types",
        "availability_slots",
    )

    filtered = []

    required_skill_ids = _get_ids(requirement.required_skills.all())
    required_language_ids = _get_ids(requirement.required_languages.all())
    preferred_slot_ids = _get_ids(requirement.preferred_availability_slots.all())

    for volunteer in volunteers:
        # 1. город
        if event.city and volunteer.city and volunteer.city_id != event.city_id:
            continue

        # 2. район
        if event.district and volunteer.district:
            if volunteer.district_id != event.district_id and not requirement.allows_other_districts:
                continue

        # 3. обязательные навыки
        volunteer_skill_ids = _get_ids(volunteer.skills.all())
        if required_skill_ids and not required_skill_ids.issubset(volunteer_skill_ids):
            continue

        # 4. обязательные языки
        volunteer_language_ids = _get_ids(volunteer.languages.all())
        if required_language_ids and not required_language_ids.issubset(volunteer_language_ids):
            continue

        # 5. минимальный опыт
        if volunteer.experience_level < requirement.min_experience_level:
            continue

        # 6. авто
        if requirement.requires_car and not volunteer.has_car:
            continue

        # 7. ночные смены
        if requirement.requires_night_shift and not volunteer.ready_for_night_shifts:
            continue

        # 8. доступность
        volunteer_slot_ids = _get_ids(volunteer.availability_slots.all())
        if preferred_slot_ids and not volunteer_slot_ids.intersection(preferred_slot_ids):
            continue

        filtered.append(volunteer)

    return filtered


def build_feature_scores(volunteer: VolunteerProfile, event: Event):
    """
    Этап 2. Формирование признаков.
    Возвращаем словарь нормированных score от 0 до 1.
    """
    requirement = event.requirement

    volunteer_skill_ids = _get_ids(volunteer.skills.all())
    volunteer_language_ids = _get_ids(volunteer.languages.all())
    volunteer_slot_ids = _get_ids(volunteer.availability_slots.all())
    volunteer_direction_ids = _get_ids(volunteer.preferred_directions.all())
    volunteer_task_type_ids = _get_ids(volunteer.preferred_task_types.all())

    required_skill_ids = _get_ids(requirement.required_skills.all())
    optional_skill_ids = _get_ids(requirement.optional_skills.all())
    required_language_ids = _get_ids(requirement.required_languages.all())
    preferred_slot_ids = _get_ids(requirement.preferred_availability_slots.all())

    # обязательные навыки
    if required_skill_ids:
        required_skill_match = len(volunteer_skill_ids.intersection(required_skill_ids)) / len(required_skill_ids)
    else:
        required_skill_match = 1.0

    # желательные навыки
    if optional_skill_ids:
        optional_skill_match = len(volunteer_skill_ids.intersection(optional_skill_ids)) / len(optional_skill_ids)
    else:
        optional_skill_match = 1.0

    # языки
    if required_language_ids:
        language_match = len(volunteer_language_ids.intersection(required_language_ids)) / len(required_language_ids)
    else:
        language_match = 1.0

    # доступность
    if preferred_slot_ids:
        availability_match = len(volunteer_slot_ids.intersection(preferred_slot_ids)) / len(preferred_slot_ids)
    else:
        availability_match = 1.0

    # направление
    if requirement.direction_id:
        direction_match = 1.0 if requirement.direction_id in volunteer_direction_ids else 0.0
    else:
        direction_match = 1.0

    # тип задачи
    if requirement.task_type_id:
        task_type_match = 1.0 if requirement.task_type_id in volunteer_task_type_ids else 0.0
    else:
        task_type_match = 1.0

    # опыт
    if requirement.min_experience_level > 0:
        experience_score = min(volunteer.experience_level / requirement.min_experience_level, 1.0)
    else:
        experience_score = 1.0

    # район / локация
    if event.district and volunteer.district:
        location_score = 1.0 if volunteer.district_id == event.district_id else 0.6
    elif event.city and volunteer.city:
        location_score = 1.0 if volunteer.city_id == event.city_id else 0.5
    else:
        location_score = 0.7

    # надёжность пока привязываем к заполненности профиля
    reliability_score = min(volunteer.profile_completion_percent / 100, 1.0)

    return {
        "required_skill_match": round(required_skill_match, 3),
        "optional_skill_match": round(optional_skill_match, 3),
        "language_match": round(language_match, 3),
        "availability_match": round(availability_match, 3),
        "direction_match": round(direction_match, 3),
        "task_type_match": round(task_type_match, 3),
        "experience_score": round(experience_score, 3),
        "location_score": round(location_score, 3),
        "reliability_score": round(reliability_score, 3),
    }


def calculate_hybrid_score(feature_scores: dict):
    """
    Этап 3-4. Гибридный итоговый score.
    Пока без ML, но структура уже готова.
    """

    score = (
        0.30 * feature_scores["required_skill_match"] +
        0.15 * feature_scores["optional_skill_match"] +
        0.15 * feature_scores["language_match"] +
        0.10 * feature_scores["availability_match"] +
        0.05 * feature_scores["direction_match"] +
        0.05 * feature_scores["task_type_match"] +
        0.10 * feature_scores["experience_score"] +
        0.05 * feature_scores["location_score"] +
        0.05 * feature_scores["reliability_score"]
    )

    return round(score, 3)


def build_explanations(volunteer: VolunteerProfile, event: Event, feature_scores: dict):
    """
    Этап 4. Объяснение выбора.
    """
    reasons = []

    if feature_scores["required_skill_match"] == 1:
        reasons.append("совпали все обязательные навыки")
    elif feature_scores["required_skill_match"] > 0:
        reasons.append("частично совпали обязательные навыки")

    if feature_scores["optional_skill_match"] > 0:
        reasons.append("есть желательные навыки")

    if feature_scores["language_match"] == 1:
        reasons.append("подходит по языкам")
    elif feature_scores["language_match"] > 0:
        reasons.append("частично подходит по языкам")

    if feature_scores["availability_match"] > 0:
        reasons.append("совпадает по доступности")

    if feature_scores["experience_score"] >= 1:
        reasons.append("опыт соответствует или выше минимального")

    if feature_scores["location_score"] >= 1:
        reasons.append("подходит по локации")

    if volunteer.has_car and getattr(event.requirement, "requires_car", False):
        reasons.append("есть автомобиль")

    if volunteer.ready_for_night_shifts and getattr(event.requirement, "requires_night_shift", False):
        reasons.append("готов к ночным сменам")

    if not reasons:
        reasons.append("подходит по суммарным критериям")

    return reasons


def run_matching_for_event(event: Event):
    """
    Главный orchestration-метод.
    """
    candidates = hard_filter_volunteers(event)
    results = []

    for volunteer in candidates:
        feature_scores = build_feature_scores(volunteer, event)
        final_score = calculate_hybrid_score(feature_scores)
        reasons = build_explanations(volunteer, event, feature_scores)

        results.append({
            "volunteer": volunteer,
            "score": final_score,
            "features": feature_scores,
            "reasons": reasons,
        })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results