import httpx
from urllib.parse import quote, urlparse
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, AFFILIATE_TEMPLATE

def extract_product_id(permalink: str) -> str:
    """Extrai o ID/slug do produto a partir do permalink.
    Ex.: https://produto.mercadolivre.com.br/MLB-123456 - retorna MLB-123456
         https://produto.mercadolivre.com.br/MLB-123456/nome - retorna MLB-123456/nome
    Manteremos o último segmento inteiro para compatibilidade com a rota /social.
    """
    path = urlparse(permalink).path
    slug = path.strip("/").split("/")[-1]
    return slug

def make_affiliate_link(permalink: str) -> str:
    product_id = extract_product_id(permalink)
    return AFFILIATE_TEMPLATE.replace("{permalink}", quote(product_id, safe=""))

async def send_offer(photo_url: str, caption_html: str):
    api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    payload = {"chat_id": TELEGRAM_CHANNEL_ID, "photo": photo_url, "caption": caption_html, "parse_mode": "HTML"}
    async with httpx.AsyncClient(timeout=20) as cx:
        r = await cx.post(api, data=payload)
        r.raise_for_status()
        return r.json()
