from apps.accounts.models import VolunteerProfile, SkillLevel, LanguageLevel

SKILL_ORDER = {
    SkillLevel.BEGINNER: 1,
    SkillLevel.INTERMEDIATE: 2,
    SkillLevel.ADVANCED: 3,
    SkillLevel.PROFESSIONAL: 4,
}
LANG_ORDER = {
    LanguageLevel.BASIC: 1,
    LanguageLevel.CONVERSATIONAL: 2,
    LanguageLevel.FLUENT: 3,
}


def _base_candidates():
    return VolunteerProfile.objects.select_related('user', 'city', 'district').prefetch_related(
        'skills__skill', 'languages__language', 'availability_items', 'preferred_directions', 'preferred_task_types'
    ).filter(user__profile__role='VOLUNTEER')



def _score_position(position, volunteer, strict=True):
    reasons = []
    suggestions = []
    if position.requires_car and not volunteer.has_car:
        return None
    if position.requires_night_shift and volunteer.avoid_night_shifts:
        return None
    if position.requires_physical_work and not volunteer.physical_work_ok:
        return None
    if position.requires_heavy_lifting and not volunteer.carry_heavy_ok:
        return None
    if position.avoid_large_crowds_sensitive and volunteer.avoid_large_crowds:
        return None

    volunteer_skills = {item.skill_id: SKILL_ORDER.get(item.level, 0) for item in volunteer.skills.all()}
    volunteer_langs = {item.language_id: LANG_ORDER.get(item.level, 0) for item in volunteer.languages.all()}
    volunteer_avails = {(a.weekday, a.time_of_day) for a in volunteer.availability_items.all()}

    req_skills = list(position.required_skill_items.select_related('skill'))
    opt_skills = list(position.optional_skill_items.select_related('skill'))
    req_langs = list(position.language_requirements.select_related('language'))
    req_avails = list(position.availability_requirements.all())

    location_ok = True
    if strict:
        if position.event.city_id and volunteer.city_id and position.event.city_id != volunteer.city_id:
            location_ok = False
        if position.event.district_id and volunteer.district_id and position.event.district_id != volunteer.district_id:
            location_ok = False
        if not location_ok:
            return None
    else:
        if position.event.district_id and volunteer.district_id != position.event.district_id:
            suggestions.append('расширен подбор за пределы района')
        elif position.event.city_id and volunteer.city_id != position.event.city_id:
            suggestions.append('расширен подбор за пределы города')

    missing_skills = 0
    partial_skills = 0
    for req in req_skills:
        volunteer_level = volunteer_skills.get(req.skill_id, 0)
        needed = SKILL_ORDER.get(req.min_level, 0)
        if volunteer_level >= needed:
            continue
        if strict:
            return None
        if volunteer_level == 0:
            missing_skills += 1
        else:
            partial_skills += 1
    if partial_skills:
        suggestions.append('частичное совпадение обязательных навыков')
    if missing_skills:
        suggestions.append('не все обязательные навыки закрыты полностью')

    partial_langs = 0
    for req in req_langs:
        volunteer_level = volunteer_langs.get(req.language_id, 0)
        needed = LANG_ORDER.get(req.min_level, 0)
        if volunteer_level >= needed:
            continue
        if strict:
            return None
        partial_langs += 1
    if partial_langs:
        suggestions.append('языковые требования закрыты частично')

    if req_avails and not volunteer_avails.intersection({(a.weekday, a.time_of_day) for a in req_avails}):
        if strict:
            return None
        suggestions.append('доступность совпадает не полностью')

    matched_optional = 0
    for opt in opt_skills:
        if volunteer_skills.get(opt.skill_id, 0) >= SKILL_ORDER.get(opt.min_level, 0):
            matched_optional += 1
    if req_skills:
        reasons.append(f'обязательные навыки: {max(len(req_skills)-missing_skills,0)}/{len(req_skills)}')
    if req_langs:
        reasons.append(f'языки: {max(len(req_langs)-partial_langs,0)}/{len(req_langs)}')
    if req_avails:
        reasons.append('учтена доступность')

    req_component = 1.0
    if req_skills:
        req_component = max((len(req_skills) - missing_skills - 0.5*partial_skills) / len(req_skills), 0)
    opt_component = 1.0 if not opt_skills else matched_optional / len(opt_skills)
    skill_score = round(0.7 * req_component + 0.3 * opt_component, 3)

    reliability = float(volunteer.attendance_rate or 0) / 100.0 if volunteer.attendance_rate else min(float(volunteer.coordinator_rating or 0) / 5.0, 1.0)
    preference = 1.0 if ((position.direction_id and volunteer.preferred_directions.filter(id=position.direction_id).exists()) or (position.task_type_id and volunteer.preferred_task_types.filter(id=position.task_type_id).exists())) else 0.5
    final_score = round(0.5 * skill_score + 0.25 * reliability + 0.25 * preference, 3)
    if suggestions:
        reasons.append('⚠ ' + '; '.join(suggestions))
    elif position.event.district_id and volunteer.district_id == position.event.district_id:
        reasons.append('тот же район')
    elif position.event.city_id and volunteer.city_id == position.event.city_id:
        reasons.append('тот же город')

    return {
        'volunteer': volunteer,
        'score': final_score,
        'skill_score': round(skill_score, 3),
        'reliability': round(reliability, 3),
        'reasons': reasons or ['подходит по базовым условиям'],
        'is_relaxed': not strict and bool(suggestions),
    }


def run_position_matching(position):
    strict_results = []
    relaxed_results = []
    for volunteer in _base_candidates():
        result = _score_position(position, volunteer, strict=True)
        if result is not None:
            strict_results.append(result)
            continue
        relaxed = _score_position(position, volunteer, strict=False)
        if relaxed is not None:
            relaxed_results.append(relaxed)

    strict_results.sort(key=lambda x: x['score'], reverse=True)
    relaxed_results.sort(key=lambda x: x['score'], reverse=True)

    recommendations = []
    if not strict_results:
        recommendations.append('Не найдено кандидатов по строгим критериям.')
        if position.event.district_id:
            recommendations.append('Рассмотреть расширение подбора за пределы района.')
        if position.required_skill_items.exists():
            recommendations.append('Разрешить частичное совпадение обязательных навыков для срочного добора.')
        if position.slots_total > 1:
            recommendations.append('Проверить, не завышено ли требуемое количество волонтёров для роли.')

    return {
        'strict_results': strict_results,
        'relaxed_results': relaxed_results,
        'recommendations': recommendations,
    }
