from celery import Celery
from celery.schedules import schedule
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SCHEDULE_MINUTES = int(os.getenv("SCHEDULE_MINUTES", "60"))

# Configurações extras para TLS
broker_use_ssl = None
backend_use_ssl = None

if REDIS_URL.startswith("rediss://"):
    broker_use_ssl = {"ssl_cert_reqs": "CERT_NONE"}
    backend_use_ssl = {"ssl_cert_reqs": "CERT_NONE"}

celery_app = Celery(
    "telegram_ml",
    broker=REDIS_URL,
    backend=REDIS_URL,
    broker_use_ssl=broker_use_ssl,
    redis_backend_use_ssl=backend_use_ssl,
)

celery_app.conf.timezone = "America/Sao_Paulo"

# 🔔 Agenda periódica (Beat) — dispara a cada SCHEDULE_MINUTES
celery_app.conf.beat_schedule = {
    "publish-offers-periodic": {
        "task": "publish_offers_all_categories",
        "schedule": schedule(run_every=SCHEDULE_MINUTES * 60),  # em segundos
    }
}
