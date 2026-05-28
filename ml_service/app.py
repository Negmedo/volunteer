"""
ml_service/app.py
-----------------
ML-сервис для СППР волонтёров.
Реализует Random Forest классификатор, обученный на синтетических данных.

Целевая переменная (success):
  1 — волонтёр принял заявку, организатор отметил явку и поставил 5 баллов
  0 — сценарий не завершён успешно (отказ, неявка, оценка < 5)

Архитектура:
  Django → POST /predict → ml_service → {"ml_score": float, "reasons": [...]}

API-контракт не изменяется — ml_score выдаёт вероятность класса 1
по модели Random Forest вместо взвешенной суммы.
"""

import logging
import os
import pickle

import numpy as np
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Порядок признаков должен строго соответствовать build_features() в services.py
FEATURE_NAMES = [
    "skill_match",
    "language_match",
    "availability_match",
    "location_match",
    "reliability_score",
    "experience_score",
    "motivation_match",
]

MODEL_PATH = os.path.join(os.path.dirname(__file__), "rf_model.pkl")
"""
    Генерирует синтетические обучающие данные.

    Логика формирования целевой переменной:
    - Успех (1) — высокая вероятность если skill_match + reliability высокие,
      слабая локация и доступность снижают шанс.
    - Для имитации реального шума добавляется случайная составляющая.
"""


def _generate_synthetic_data(n_samples: int = 3000, seed: int = 42):

    rng = np.random.default_rng(seed)

    skill_match        = rng.beta(2, 2, n_samples)
    language_match     = rng.beta(3, 1.5, n_samples)
    availability_match = rng.beta(2, 2, n_samples)
    location_match     = rng.choice([0.3, 0.4, 0.7, 0.8, 1.0], n_samples,
                                    p=[0.10, 0.10, 0.15, 0.25, 0.40])
    reliability_score  = rng.beta(2.5, 1.5, n_samples)
    experience_score   = rng.beta(2, 3, n_samples)
    motivation_match   = rng.choice([0.3, 0.7, 1.0], n_samples, p=[0.25, 0.40, 0.35])

    X = np.column_stack([
        skill_match, language_match, availability_match,
        location_match, reliability_score, experience_score, motivation_match,
    ])

    raw = (
        0.30 * skill_match
        + 0.15 * language_match
        + 0.15 * availability_match
        + 0.15 * location_match
        + 0.10 * reliability_score
        + 0.10 * experience_score
        + 0.05 * motivation_match
    )

    # Нелинейные эффекты: бонус за комбинации высоких значений
    bonus = (
        (skill_match > 0.7).astype(float) * (reliability_score > 0.7).astype(float) * 0.15
        + (location_match == 1.0).astype(float) * 0.05
        + (availability_match > 0.8).astype(float) * 0.05
        - (reliability_score < 0.3).astype(float) * 0.10
    )

    noise = rng.normal(0, 0.07, n_samples)
    prob = np.clip(raw + bonus + noise, 0.0, 1.0)
    y = (prob >= 0.60).astype(int)

    return X, y


# ── Обучение / загрузка модели ───────────────────────────────
def _train_model() -> Pipeline:
    """Обучает Random Forest на синтетических данных и сохраняет модель."""
    logger.info("Training Random Forest model on synthetic data...")
    X, y = _generate_synthetic_data()

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            min_samples_leaf=10,
            max_features="sqrt",
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )),
    ])
    pipeline.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    logger.info("Model trained and saved to %s", MODEL_PATH)
    return pipeline


def _load_or_train_model() -> Pipeline:
    """Загружает сохранённую модель или обучает заново."""
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            logger.info("Model loaded from %s", MODEL_PATH)
            return model
        except Exception as exc:
            logger.warning("Failed to load saved model (%s), retraining...", exc)
    return _train_model()


# Загружаем/обучаем при старте сервиса
model: Pipeline = _load_or_train_model()


# ── Вспомогательные функции ──────────────────────────────────
def _clamp(value: float) -> float:
    """Ограничивает значение признака диапазоном [0, 1]."""
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def _build_reasons(features: dict, score: float) -> list[str]:
    """
    Генерирует текстовые объяснения выбора кандидата на основе признаков.
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

    if score >= 0.80:
        reasons.append("→ высокий приоритет (ML)")
    elif score >= 0.55:
        reasons.append("→ средний приоритет (ML)")
    else:
        reasons.append("→ низкий приоритет (ML)")

    return reasons if reasons else ["подходит по суммарным критериям"]


# ── Эндпоинты ────────────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    """
    POST /predict

    Тело запроса (JSON):
    {
      "skill_match":        0.0 - 1.0,
      "language_match":     0.0 - 1.0,
      "availability_match": 0.0 - 1.0,
      "location_match":     0.0 - 1.0,
      "reliability_score":  0.0 - 1.0,
      "experience_score":   0.0 - 1.0,
      "motivation_match":   0.0 - 1.0
    }

    Ответ:
    {
      "ml_score": 0.0 - 1.0,   # P(успешный сценарий) по Random Forest
      "reasons":  ["...", "..."],
      "features_used": {...}    # для отладки
    }
    """
    data = request.get_json(force=True, silent=True) or {}

    features = {key: _clamp(data.get(key, 0.0)) for key in FEATURE_NAMES}
    X = np.array([[features[k] for k in FEATURE_NAMES]])

    # Вероятность класса 1 (успешный сценарий)
    ml_score = round(float(model.predict_proba(X)[0][1]), 4)

    reasons = _build_reasons(features, ml_score)

    return jsonify({
        "ml_score": ml_score,
        "reasons": reasons,
        "features_used": features,
    })


@app.route("/health", methods=["GET"])
def health():
    """Проверка работоспособности сервиса."""
    return jsonify({
        "status": "ok",
        "service": "volunteer-ml",
        "model": "RandomForestClassifier",
    })


@app.route("/model/info", methods=["GET"])
def model_info():
    """Информация об обученной модели (для диплома / отладки)."""
    clf = model.named_steps["clf"]
    importances = dict(zip(FEATURE_NAMES, clf.feature_importances_.tolist()))
    return jsonify({
        "model_type": "RandomForestClassifier",
        "n_estimators": clf.n_estimators,
        "max_depth": clf.max_depth,
        "feature_importances": importances,
        "trained_on": "synthetic_data",
        "target": "P(accepted + attended + rating==5)",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8765, debug=False)
