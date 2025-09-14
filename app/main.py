from fastapi import FastAPI
import os
import httpx
import redis.asyncio as redis
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

# ------------ Redis / Celery diagnostics ------------
@app.get("/diagnostics")
async def diagnostics():
    info = {"web_ok": True}
    info["env"] = {
        "REDIS_URL_scheme": os.getenv("REDIS_URL", "")[:6],
        "TELEGRAM_CHANNEL_ID": TELEGRAM_CHANNEL_ID,
        "TELEGRAM_BOT_TOKEN_set": bool(TELEGRAM_BOT_TOKEN),
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

# ------------ Telegram deep diagnostics ------------
API_BASE = lambda t: f"https://api.telegram.org/bot{t}"

@app.get("/tg/getMe")
async def tg_get_me():
    async with httpx.AsyncClient(timeout=15) as cx:
        r = await cx.get(f"{API_BASE(TELEGRAM_BOT_TOKEN)}/getMe")
    return {"status": r.status_code, "body": r.text}

@app.get("/tg/getChat")
async def tg_get_chat():
    async with httpx.AsyncClient(timeout=15) as cx:
        r = await cx.get(f"{API_BASE(TELEGRAM_BOT_TOKEN)}/getChat", params={"chat_id": TELEGRAM_CHANNEL_ID})
    return {"status": r.status_code, "body": r.text}

@app.get("/tg/getAdmins")
async def tg_get_admins():
    async with httpx.AsyncClient(timeout=15) as cx:
        r = await cx.get(f"{API_BASE(TELEGRAM_BOT_TOKEN)}/getChatAdministrators", params={"chat_id": TELEGRAM_CHANNEL_ID})
    return {"status": r.status_code, "body": r.text}

# Mensagem simples para validar postagem
@app.get("/test-telegram")
async def test_telegram():
    async with httpx.AsyncClient(timeout=15) as cx:
        r = await cx.post(f"{API_BASE(TELEGRAM_BOT_TOKEN)}/sendMessage",
                          data={"chat_id": TELEGRAM_CHANNEL_ID, "text": "✅ Teste OK: bot conectado e com permissão de postar."})
    return {"status": r.status_code, "body": r.text}

# Disparo das ofertas
@app.post("/run-now")
def run_now():
    try:
        celery_app.send_task("publish_offers_all_categories")
        return {"scheduled": True}
    except Exception as e:
        return {"scheduled": False, "error": repr(e)}

@app.get("/test-run")
def test_run():
    try:
        celery_app.send_task("publish_offers_all_categories")
        return {"scheduled": True, "note": "Executado via GET /test-run"}
    except Exception as e:
        return {"scheduled": False, "error": repr(e)}
