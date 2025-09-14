import os
import ssl
from celery import Celery
from celery.schedules import schedule

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SCHEDULE_MINUTES = int(os.getenv("SCHEDULE_MINUTES", "60"))

# Use result backend? (para este projeto, normalmente NÃO precisa)
USE_RESULT_BACKEND = False  # deixe False para evitar mais pontos de falha

# Config SSL só quando usar rediss://
broker_use_ssl = None
backend_use_ssl = None
if REDIS_URL.startswith("rediss://"):
    # Preferencialmente valide o certificado:
    cert_level = ssl.CERT_REQUIRED
    # Se falhar por cadeia de certificados no seu ambiente, troque temporariamente para:
    # cert_level = ssl.CERT_OPTIONAL
    # (Como último recurso de teste: cert_level = ssl.CERT_NONE)

    broker_use_ssl = {"ssl_cert_reqs": cert_level}
    backend_use_ssl = {"ssl_cert_reqs": cert_level}

celery_app = Celery(
    "telegram_ml",
    broker=REDIS_URL,
    backend=(REDIS_URL if USE_RESULT_BACKEND else None),
    broker_use_ssl=broker_use_ssl,
    redis_backend_use_ssl=backend_use_ssl,
)

# Se não for usar backend de resultados, ignore resultados:
if not USE_RESULT_BACKEND:
    celery_app.conf.task_ignore_result = True
    celery_app.conf.result_backend = None

celery_app.conf.timezone = "America/Sao_Paulo"
celery_app.conf.beat_schedule = {
    "publish-offers-periodic": {
        "task": "publish_offers_all_categories",
        "schedule": schedule(run_every=SCHEDULE_MINUTES * 60),
    }
}
