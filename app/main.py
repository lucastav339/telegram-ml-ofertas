from fastapi import FastAPI
import os
import redis.asyncio as redis
from app.celery_app import celery_app

app = FastAPI()


@app.get("/")
def root():
    return {"ok": True, "service": "telegram-ml-web"}


@app.get("/health")
def health_alias():
    return {"ok": True}


@app.get("/healthz")
def healthz():
    return {"ok": True}


# 🔎 Diagnóstico: testa Redis e presença do Worker
@app.get("/diagnostics")
async def diagnostics():
    info = {"web_ok": True}

    # Mostrar só se variáveis existem (sem vazar segredos)
    info["env"] = {
        "REDIS_URL_scheme": os.getenv("REDIS_URL", "")[:6],  # 'redis:' ou 'rediss'
        "TELEGRAM_CHANNEL_ID_set": bool(os.getenv("TELEGRAM_CHANNEL_ID")),
        "TELEGRAM_BOT_TOKEN_set": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
    }

    # Teste Redis
    try:
        rds = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        pong = await rds.ping()
        info["redis_ping"] = pong
    except Exception as e:
        info["redis_ping"] = False
        info["redis_error"] = repr(e)

    # Ping Celery Worker
    try:
        pongs = celery_app.control.ping(timeout=2)
        info["celery_ping"] = pongs or []
        info["celery_ok"] = bool(pongs)
    except Exception as e:
        info["celery_ok"] = False
        info["celery_error"] = repr(e)

    return info


# 🔔 POST padrão (Postman/curl)
@app.post("/run-now")
def run_now():
    try:
        celery_app.send_task("publish_offers_all_categories")
        return {"scheduled": True}
    except Exception as e:
        return {"scheduled": False, "error": repr(e)}


# 🔔 GET amigável (para testar no navegador)
@app.get("/test-run")
def test_run():
    try:
        celery_app.send_task("publish_offers_all_categories")
        return {"scheduled": True, "note": "Executado via GET /test-run"}
    except Exception as e:
        return {"scheduled": False, "error": repr(e)}
