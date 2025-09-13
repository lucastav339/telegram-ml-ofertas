from celery import Celery
from app.config import REDIS_URL

celery_app = Celery(
    "telegram_ml",
    broker=REDIS_URL,
    backend=REDIS_URL,
)
celery_app.conf.timezone = "America/Sao_Paulo"
# Beat schedule programático poderia ser adicionado aqui se quisermos crontab;
# como estamos rodando o beat via comando, a tarefa será registrada pela view /run-now.
