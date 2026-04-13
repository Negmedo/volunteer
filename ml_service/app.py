"""
ml_service/app.py
-----------------
Baseline ML-сервис для СППР волонтёров.
Реализует Вариант А: формульный scoring + объяснения.

Архитектур:
  Django → POST /predict → ml_service → {"ml_score": float, "reasons": [...]}

Когда появятся реальные данные — логику внутри predict()
можно заменить на обученную sklearn-модель без изменения API-контракта.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# Веса признаков — задокументированы явно для диплома
WEIGHTS = {
    "skill_match":       0.30,
    "language_match":    0.15,
    "availability_match":0.15,
    "location_match":    0.15,
    "reliability_score": 0.10,
    "experience_score":  0.10,
    "motivation_match":  0.05,
}


def _clamp(value: float) -> float:
    """Ограничивает значение признака диапазоном [0, 1]."""
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def _build_reasons(features: dict, score: float) -> list[str]:
    """
    Генерирует текстовые объяснения выбора кандидата.
    Используется для отображения на странице подбора (Explainable AI).
    """
    reasons = []

    if features["skill_match"] >= 0.9:
        reasons.append("полное совпадение навыков")
    elif features["skill_match"] >= 0.6:
        reasons.append("хорошее совпадение навыков")
    elif features["skill_match"] >= 0.3:
        reasons.append("частичное совпадение навыков")

    if features["language_match"] >= 0.9:
        reasons.append("языковые требования выполнены")
    elif features["language_match"] >= 0.5:
        reasons.append("языки частично совпадают")

    if features["availability_match"] >= 0.8:
        reasons.append("доступность совпадает")
    elif features["availability_match"] >= 0.4:
        reasons.append("доступность частично совпадает")

    if features["location_match"] >= 0.9:
        reasons.append("тот же район")
    elif features["location_match"] >= 0.6:
        reasons.append("тот же город")
    else:
        reasons.append("локация не совпадает")

    if features["reliability_score"] >= 0.8:
        reasons.append("высокая надёжность")
    elif features["reliability_score"] >= 0.5:
        reasons.append("средняя надёжность")
    elif features["reliability_score"] > 0:
        reasons.append("низкая надёжность")

    if features["experience_score"] >= 0.75:
        reasons.append("опыт соответствует или превышает требования")
    elif features["experience_score"] >= 0.4:
        reasons.append("опыт частично соответствует")

    if features["motivation_match"] >= 0.8:
        reasons.append("направление совпадает с предпочтениями")

    if score >= 0.8:
        reasons.append("→ высокий приоритет")
    elif score >= 0.55:
        reasons.append("→ средний приоритет")
    else:
        reasons.append("→ низкий приоритет")

    return reasons if reasons else ["подходит по суммарным критериям"]


@app.route("/predict", methods=["POST"])
def predict():
    """
    POST /predict

    Тело запроса (JSON):
    {
      "skill_match":        0.0 – 1.0,
      "language_match":     0.0 – 1.0,
      "availability_match": 0.0 – 1.0,
      "location_match":     0.0 – 1.0,
      "reliability_score":  0.0 – 1.0,
      "experience_score":   0.0 – 1.0,
      "motivation_match":   0.0 – 1.0
    }

    Ответ:
    {
      "ml_score": 0.0 – 1.0,
      "reasons":  ["...", "..."]
    }
    """
    data = request.get_json(force=True, silent=True) or {}

    features = {key: _clamp(data.get(key, 0.0)) for key in WEIGHTS}

    ml_score = round(
        sum(features[key] * weight for key, weight in WEIGHTS.items()),
        4,
    )

    reasons = _build_reasons(features, ml_score)

    return jsonify({
        "ml_score": ml_score,
        "reasons": reasons,
        "features_used": features,   # для отладки и диплома
    })


@app.route("/health", methods=["GET"])
def health():
    """Проверка работоспособности сервиса."""
    return jsonify({"status": "ok", "service": "volunteer-ml"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8765, debug=False)