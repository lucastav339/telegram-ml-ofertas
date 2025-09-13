from celery import Celery
from app.config import REDIS_URL

celery_app = Celery(
    "telegram_ml",
    broker=REDIS_URL,
    backend=REDIS_URL,
)
celery_app.conf.timezone = "America/Sao_Paulo"
