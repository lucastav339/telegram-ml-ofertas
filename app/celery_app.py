import os
from celery import Celery
from celery.schedules import schedule

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SCHEDULE_MINUTES = int(os.getenv("SCHEDULE_MINUTES", "60"))

# ↓↓↓ MUITO IMPORTANTE: limitar conexões do Celery/Kombu
BROKER_POOL_LIMIT = int(os.getenv("BROKER_POOL_LIMIT", "2"))  # pool de conexões do broker
WORKER_PREFETCH = int(os.getenv("WORKER_PREFETCH", "1"))      # evita reservar muitas tasks

celery_app = Celery(
    "telegram_ml",
    broker=REDIS_URL,
    backend=None,               # sem result backend
    include=["app.tasks"],      # garante que a task seja registrada
)

# Ignorar resultados
celery_app.conf.task_ignore_result = True
celery_app.conf.result_backend = None

# Conexões & estabilidade
celery_app.conf.broker_pool_limit = BROKER_POOL_LIMIT
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.broker_heartbeat = 30
celery_app.conf.worker_prefetch_multiplier = WORKER_PREFETCH
celery_app.conf.worker_cancel_long_running_tasks_on_connection_loss = True

celery_app.conf.timezone = "America/Sao_Paulo"

# Agenda
celery_app.conf.beat_schedule = {
    "publish-offers-periodic": {
        "task": "publish_offers_all_categories",
        "schedule": schedule(run_every=SCHEDULE_MINUTES * 60),
    }
}
