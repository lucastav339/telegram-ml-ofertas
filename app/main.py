from fastapi import FastAPI
from app.celery_app import celery_app

app = FastAPI()

@app.get("/healthz")
def health():
    return {"ok": True}

@app.post("/run-now")
def run_now():
    celery_app.send_task("publish_offers_all_categories")
    return {"scheduled": True}
