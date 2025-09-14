from fastapi import FastAPI
import os
import redis.asyncio as redis
import httpx
from app.celery_app import celery_app
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

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


# 🔎 Diagnóstico: testa Redis e Worker
@app.get("/diagnostics")
async def diagnostics():
    info = {"web_ok": True}
    info["env"] = {
        "REDIS_URL_scheme": os.getenv("REDIS_URL", "")[:6],
        "TELEGRAM_CHANNEL_ID_set": bool(os.getenv("TELEGRAM_CHANNEL_ID")),
        "TELEGRAM_BOT_TOKEN_set": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
    }

    try:
        rds = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        pong = await rds.ping()
        info["redis_ping"] = pong
    except Exception as e:
        info["redis_ping"] = False
        info["redis_error"] = repr(e)

    try:
        pongs = celery_app.control.ping(timeout=2)
        info["celery_ping"] = pongs or []
        info["celery_ok"] = bool(pongs)
    except Exception as e:
        info["celery_ok"] = False
        info["celery_error"] = repr(e)

    return info


# 🔔 Forçar execução via POST (para Postman/curl)
@app.post("/run-now")
def run_now():
    try:
        celery_app.send_task("publish_offers_all_categories")
        return {"scheduled": True}
    except Exception as e:
        return {"scheduled": False, "error": repr(e)}


# 🔔 Forçar execução via GET (para navegador)
@app.get("/test-run")
def test_run():
    try:
        celery_app.send_task("publish_offers_all_categories")
        return {"scheduled": True, "note": "Executado via GET /test-run"}
    except Exception as e:
        return {"scheduled": False, "error": repr(e)}


# 🔎 Teste de envio direto ao Telegram (ignora filtros/Redis)
@app.get("/test-telegram")
async def test_telegram():
    try:
        api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHANNEL_ID, "text": "✅ Teste OK: bot conectado e com permissão de postar."}
        async with httpx.AsyncClient(timeout=15) as cx:
            r = await cx.post(api, data=data)
            r.raise_for_status()
        return {"ok": True, "telegram_response": r.json()}
    except Exception as e:
        return {"ok": False, "error": repr(e)}
