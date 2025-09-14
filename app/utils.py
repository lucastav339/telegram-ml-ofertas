import redis.asyncio as redis
from app.config import REDIS_URL
from app.fetcher_meli import search_products
from app.filters import compute_discount, get_seller_level, good_seller
from app.publisher_telegram import make_affiliate_link, send_offer

# Pool único e pequeno (evita estourar limite do Redis Cloud)
_pool = redis.ConnectionPool.from_url(REDIS_URL, max_connections=5, decode_responses=False)
rds = redis.Redis(connection_pool=_pool)

def _format_currency(v) -> str:
    try:
        return f"R$ {float(v):.2f}"
    except Exception:
        return "-"

def build_caption(item: dict, discount_pct: int, seller_level: str, affiliate_url: str) -> str:
    title = item.get("title") or "Oferta"
    price_now = item.get("price") or 0
    original = item.get("original_price") or 0
    return (
        f"⚡ <b>OFERTA RELÂMPAGO</b>\n\n"
        f"{title}\n\n"
        f"De: <s>{_format_currency(original)}</s>\n"
        f"Por: <b>{_format_currency(price_now)}</b> ({discount_pct}% OFF)\n"
        f"🏆 Vendedor: {seller_level or '—'}\n\n"
        f"👉 <a href='{affiliate_url}'>Conferir no Mercado Livre</a>\n"
        f"#promo #ofertas"
    )

__all__ = [
    "rds",
    "search_products",
    "compute_discount",
    "get_seller_level",
    "good_seller",
    "make_affiliate_link",
    "send_offer",
