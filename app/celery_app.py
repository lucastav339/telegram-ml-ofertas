import os
from celery import Celery
from celery.schedules import schedule

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SCHEDULE_MINUTES = int(os.getenv("SCHEDULE_MINUTES", "60"))

# Sem TLS: não passe broker_use_ssl
celery_app = Celery(
    "telegram_ml",
    broker=REDIS_URL,
    backend=None,                  # não precisamos do result backend
)

# Ignorar resultados para não tocar backend
celery_app.conf.task_ignore_result = True
celery_app.conf.result_backend = None

# (opcional) evitar warning do Celery 6
celery_app.conf.broker_connection_retry_on_startup = True

celery_app.conf.timezone = "America/Sao_Paulo"
celery_app.conf.beat_schedule = {
    "publish-offers-periodic": {
        "task": "publish_offers_all_categories",
        "schedule": schedule(run_every=SCHEDULE_MINUTES * 60),
    }
}
