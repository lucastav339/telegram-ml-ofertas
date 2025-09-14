from celery import Celery
from celery.schedules import schedule
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SCHEDULE_MINUTES = int(os.getenv("SCHEDULE_MINUTES", "60"))

# Se broker usa TLS (rediss://), habilite SSL no broker
broker_use_ssl = None
if REDIS_URL.startswith("rediss://"):
    # Se seu provedor tem CA válida, use CERT_REQUIRED.
    # Se acusar erro de certificado, troque para CERT_OPTIONAL temporariamente.
    broker_use_ssl = {"ssl_cert_reqs": "CERT_REQUIRED"}

celery_app = Celery(
    "telegram_ml",
    broker=REDIS_URL,
    backend=None,                 # 🔴 sem backend de resultados
    broker_use_ssl=broker_use_ssl,
)

# Não guardar resultados (evita tocar no backend)
celery_app.conf.task_ignore_result = True
celery_app.conf.result_backend = None

celery_app.conf.timezone = "America/Sao_Paulo"
celery_app.conf.beat_schedule = {
    "publish-offers-periodic": {
        "task": "publish_offers_all_categories",
        "schedule": schedule(run_every=SCHEDULE_MINUTES * 60),
    }
}
