from fastapi import FastAPI
from app.celery_app import celery_app

app = FastAPI()

# ✅ Root para não dar 404 em HEAD/GET /
@app.get("/")
def root():
    return {"ok": True, "service": "telegram-ml-web"}

# ✅ Health "clássico"
@app.get("/health")
def health_alias():
    return {"ok": True}

# ✅ Health usado no projeto
@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/run-now")
def run_now():
    celery_app.send_task("publish_offers_all_categories")
    return {"scheduled": True}
