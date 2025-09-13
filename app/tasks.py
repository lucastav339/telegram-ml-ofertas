import httpx
from urllib.parse import quote
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, AFFILIATE_TEMPLATE

def make_affiliate_link(permalink: str) -> str:
    return AFFILIATE_TEMPLATE.replace("{permalink}", quote(permalink, safe=""))

async def send_offer(photo_url: str, caption_html: str):
    api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    payload = {"chat_id": TELEGRAM_CHANNEL_ID, "photo": photo_url, "caption": caption_html, "parse_mode": "HTML"}
    async with httpx.AsyncClient(timeout=20) as cx:
        r = await cx.post(api, data=payload)
        r.raise_for_status()
        return r.json()
