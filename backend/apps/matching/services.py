"""
apps/matching/services.py
-------------------------
Модуль интеллектуального подбора волонтёров (СППР).

Архитектура:
  1. hard_filter       — жёсткое исключение неподходящих кандидатов
  2. build_features    — формирование вектора признаков по паре (роль, волонтёр)
  3. call_ml_service   — вызов Flask ML-endpoint, получение ml_score + reasons
  4. hybrid_score      — финальный балл: 0.5*ml + 0.3*skill + 0.2*reliability
  5. run_position_matching — оркестратор, возвращает strict/relaxed/recommendations

Если ML-сервис недоступен, система переключается на локальный fallback scoring
без прерывания работы Django.
"""

import logging
import urllib.request
import json

from django.conf import settings

from apps.accounts.models import VolunteerProfile, SkillLevel, LanguageLevel

logger = logging.getLogger(__name__)

SKILL_ORDER = {
    SkillLevel.BEGINNER:      1,
    SkillLevel.INTERMEDIATE:  2,
    SkillLevel.ADVANCED:      3,
    SkillLevel.PROFESSIONAL:  4,
}
LANG_ORDER = {
    LanguageLevel.BASIC:          1,
    LanguageLevel.CONVERSATIONAL:  2,
    LanguageLevel.FLUENT:          3,
}


# ── 0. Кандидаты ─────────────────────────────────────────────
def _base_candidates():
    return (
        VolunteerProfile.objects
        .select_related("user", "city", "district")
        .prefetch_related(
            "skills__skill",
            "languages__language",
            "availability_items",
            "preferred_directions",
            "preferred_task_types",
        )
        .filter(user__profile__role="VOLUNTEER")
    )


# ── 1. Проверка ML-сервиса ───────────────────────────────────
def check_ml_service() -> bool:
    """
    Проверяет доступность ML-сервиса через /health endpoint.
    Вызывается один раз за запрос — не завязан на наличие кандидатов.
    """
    url = getattr(settings, "ML_SERVICE_URL", "http://ml:8765/predict")
    health_url = url.replace("/predict", "/health")
    timeout = getattr(settings, "ML_SERVICE_TIMEOUT", 3)
    try:
        req = urllib.request.Request(health_url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception as exc:
        logger.warning("ML service health check failed: %s", exc)
        return False


# ── 2. Hard filter ───────────────────────────────────────────
def _passes_hard_filter(position, volunteer) -> bool:
    if position.requires_car and not volunteer.has_car:
        return False
    if position.requires_night_shift and volunteer.avoid_night_shifts:
        return False
    if position.requires_physical_work and not volunteer.physical_work_ok:
        return False
    if position.requires_heavy_lifting and not volunteer.carry_heavy_ok:
        return False
    if position.avoid_large_crowds_sensitive and volunteer.avoid_large_crowds:
        return False
    return True


def _location_match_strict(position, volunteer) -> bool:
    if position.event.city_id and volunteer.city_id:
        if position.event.city_id != volunteer.city_id:
            return False
    if position.event.district_id and volunteer.district_id:
        if position.event.district_id != volunteer.district_id:
            return False
    return True


# ── 3. Feature builder ───────────────────────────────────────
def build_features(position, volunteer) -> dict:
    """
    Вектор нормированных признаков [0, 1] для пары (роль, волонтёр).
    """
    volunteer_skills = {
        item.skill_id: SKILL_ORDER.get(item.level, 0)
        for item in volunteer.skills.all()
    }
    volunteer_langs = {
        item.language_id: LANG_ORDER.get(item.level, 0)
        for item in volunteer.languages.all()
    }
    volunteer_avails = {
        (a.weekday, a.time_of_day)
        for a in volunteer.availability_items.all()
    }

    req_skills = list(position.required_skill_items.select_related("skill"))
    opt_skills = list(position.optional_skill_items.select_related("skill"))
    req_langs  = list(position.language_requirements.select_related("language"))
    req_avails = list(position.availability_requirements.all())

    # skill_match
    if req_skills:
        matched = sum(
            1 for r in req_skills
            if volunteer_skills.get(r.skill_id, 0) >= SKILL_ORDER.get(r.min_level, 0)
        )
        req_part = matched / len(req_skills)
    else:
        req_part = 1.0

    if opt_skills:
        matched_opt = sum(
            1 for o in opt_skills
            if volunteer_skills.get(o.skill_id, 0) >= SKILL_ORDER.get(o.min_level, 0)
        )
        opt_part = matched_opt / len(opt_skills)
    else:
        opt_part = 1.0

    skill_match = round(0.7 * req_part + 0.3 * opt_part, 3)

    # language_match
    if req_langs:
        matched_lang = sum(
            1 for r in req_langs
            if volunteer_langs.get(r.language_id, 0) >= LANG_ORDER.get(r.min_level, 0)
        )
        language_match = round(matched_lang / len(req_langs), 3)
    else:
        language_match = 1.0

    # availability_match
    if req_avails:
        pos_avail_set = {(a.weekday, a.time_of_day) for a in req_avails}
        intersection = volunteer_avails.intersection(pos_avail_set)
        availability_match = round(len(intersection) / len(pos_avail_set), 3)
    else:
        availability_match = 1.0

    # location_match (градуированная)
    if position.event.district_id and volunteer.district_id:
        if volunteer.district_id == position.event.district_id:
            location_match = 1.0
        elif volunteer.city_id == position.event.city_id:
            location_match = 0.8
        else:
            location_match = 0.3
    elif position.event.city_id and volunteer.city_id:
        location_match = 1.0 if volunteer.city_id == position.event.city_id else 0.4
    else:
        location_match = 0.7

    # reliability_score
    attendance = float(volunteer.attendance_rate or 0) / 100.0
    rating = float(volunteer.coordinator_rating or 0) / 5.0
    if attendance > 0 and rating > 0:
        reliability_score = round((attendance + rating) / 2, 3)
    elif attendance > 0:
        reliability_score = round(attendance, 3)
    elif rating > 0:
        reliability_score = round(rating, 3)
    else:
        reliability_score = 0.5

    # experience_score
    experience_score = round(float(volunteer.profile_completion_percent or 0) / 100.0, 3)

    # motivation_match
    direction_ok = bool(
        position.direction_id
        and volunteer.preferred_directions.filter(id=position.direction_id).exists()
    )
    task_type_ok = bool(
        position.task_type_id
        and volunteer.preferred_task_types.filter(id=position.task_type_id).exists()
    )
    if direction_ok and task_type_ok:
        motivation_match = 1.0
    elif direction_ok or task_type_ok:
        motivation_match = 0.7
    else:
        motivation_match = 0.3

    return {
        "skill_match":        skill_match,
        "language_match":     language_match,
        "availability_match": availability_match,
        "location_match":     location_match,
        "reliability_score":  reliability_score,
        "experience_score":   experience_score,
        "motivation_match":   motivation_match,
    }


# ── 4. ML client ─────────────────────────────────────────────
def call_ml_service(features: dict) -> dict | None:
    url = getattr(settings, "ML_SERVICE_URL", "http://ml:8765/predict")
    timeout = getattr(settings, "ML_SERVICE_TIMEOUT", 3)
    try:
        payload = json.dumps(features).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        logger.warning("ML service unavailable: %s — using local fallback", exc)
        return None


def _fallback_score(features: dict) -> dict:
    """Локальный скоринг если ML-сервис недоступен."""
    weights = {
        "skill_match": 0.30, "language_match": 0.15,
        "availability_match": 0.15, "location_match": 0.15,
        "reliability_score": 0.10, "experience_score": 0.10,
        "motivation_match": 0.05,
    }
    score = round(sum(features[k] * w for k, w in weights.items()), 4)
    reasons = []
    if features["skill_match"] >= 0.7:
        reasons.append("хорошее совпадение навыков")
    if features["language_match"] >= 0.8:
        reasons.append("языковые требования выполнены")
    if features["location_match"] >= 0.8:
        reasons.append("тот же район/город")
    if features["reliability_score"] >= 0.7:
        reasons.append("высокая надёжность")
    if not reasons:
        reasons.append("подходит по суммарным критериям")
    return {"ml_score": score, "reasons": reasons}


# ── 5. Hybrid score ──────────────────────────────────────────
def compute_hybrid_score(ml_score: float, features: dict) -> float:
    return round(
        0.5 * ml_score
        + 0.3 * features["skill_match"]
        + 0.2 * features["reliability_score"],
        3,
    )


# ── 6. Кандидат-pipeline ─────────────────────────────────────
def _score_candidate(position, volunteer, strict: bool) -> dict | None:
    if not _passes_hard_filter(position, volunteer):
        return None
    if strict and not _location_match_strict(position, volunteer):
        return None

    features = build_features(position, volunteer)

    if strict:
        volunteer_skills = {
            item.skill_id: SKILL_ORDER.get(item.level, 0)
            for item in volunteer.skills.all()
        }
        for req in position.required_skill_items.select_related("skill"):
            if volunteer_skills.get(req.skill_id, 0) < SKILL_ORDER.get(req.min_level, 0):
                return None

        volunteer_langs = {
            item.language_id: LANG_ORDER.get(item.level, 0)
            for item in volunteer.languages.all()
        }
        for req in position.language_requirements.select_related("language"):
            if volunteer_langs.get(req.language_id, 0) < LANG_ORDER.get(req.min_level, 0):
                return None

    ml_result = call_ml_service(features) or _fallback_score(features)
    ml_score = float(ml_result.get("ml_score", 0.0))
    reasons = ml_result.get("reasons", [])
    hybrid = compute_hybrid_score(ml_score, features)

    return {
        "volunteer":   volunteer,
        "score":       hybrid,
        "ml_score":    round(ml_score, 3),
        "skill_score": round(features["skill_match"], 3),
        "reliability": round(features["reliability_score"], 3),
        "features":    features,
        "reasons":     reasons,
        "is_relaxed":  not strict,
    }


# ── 7. Оркестратор ───────────────────────────────────────────
def run_position_matching(position) -> dict:
    """
    ml_available проверяется через /health — независимо от наличия кандидатов.
    Это устраняет ложное срабатывание "локальный скоринг" при пустом списке.
    """
    ml_available = check_ml_service()

    strict_results  = []
    relaxed_results = []

    for volunteer in _base_candidates():
        result = _score_candidate(position, volunteer, strict=True)
        if result is not None:
            strict_results.append(result)
            continue
        relaxed = _score_candidate(position, volunteer, strict=False)
        if relaxed is not None:
            relaxed_results.append(relaxed)

    strict_results.sort(key=lambda x: x["score"], reverse=True)
    relaxed_results.sort(key=lambda x: x["score"], reverse=True)

    recommendations = []
    if not strict_results:
        recommendations.append("По строгим критериям кандидаты не найдены.")
        if position.event.district_id:
            recommendations.append("Рассмотрите расширение подбора за пределы района.")
        if position.required_skill_items.exists():
            recommendations.append("Проверьте, не завышены ли требования к обязательным навыкам.")
        if position.slots_total > 1:
            recommendations.append("Проверьте, не завышено ли требуемое количество волонтёров.")
    elif len(strict_results) < position.slots_total:
        recommendations.append(
            f"Найдено {len(strict_results)} кандидат(ов), нужно {position.slots_total}. "
            "Рассмотрите расширенный подбор."
        )

    return {
        "strict_results":  strict_results,
        "relaxed_results": relaxed_results,
        "recommendations": recommendations,
        "ml_available":    ml_available,
    }