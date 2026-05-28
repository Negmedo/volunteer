FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Обучаем и сохраняем модель на этапе сборки образа,
# чтобы первый запрос к /predict не ждал обучения.
RUN python -c "import app"

EXPOSE 8765

CMD ["gunicorn", "--bind", "0.0.0.0:8765", "--workers", "2", "--timeout", "60", "app:app"]
