from fastapi import FastAPI
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

# 🔔 dispara a task manualmente via POST (padrão)
@app.post("/run-now")
def run_now():
    celery_app.send_task("publish_offers_all_categories")
    return {"scheduled": True}

# 🔔 dispara a task manualmente via GET (pra testar no navegador)
@app.get("/test-run")
def test_run():
    celery_app.send_task("publish_offers_all_categories")
    return {"scheduled": True, "note": "Executado via GET /test-run"}
