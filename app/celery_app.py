from celery import Celery
from celery.schedules import schedule
from app.config import REDIS_URL, SCHEDULE_MINUTES

celery_app = Celery(
    "telegram_ml",
    broker=REDIS_URL,
    backend=REDIS_URL,
)
celery_app.conf.timezone = "America/Sao_Paulo"

# 🔔 agenda: dispara a cada SCHEDULE_MINUTES
celery_app.conf.beat_schedule = {
    "publish-offers-periodic": {
        "task": "publish_offers_all_categories",
        "schedule": schedule(run_every=SCHEDULE_MINUTES * 60),  # segundos
    }
}
