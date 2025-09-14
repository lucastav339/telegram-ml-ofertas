from app.utils import rds  # substitui o redis.from_url antigo

@app.get("/diagnostics")
async def diagnostics():
    info = {"web_ok": True}
    info["env"] = {
        "REDIS_URL_scheme": os.getenv("REDIS_URL", "")[:6],
        "TELEGRAM_CHANNEL_ID_set": bool(os.getenv("TELEGRAM_CHANNEL_ID")),
        "TELEGRAM_BOT_TOKEN_set": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
    }
    try:
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
