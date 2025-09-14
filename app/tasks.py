import asyncio
import redis.asyncio as redis

from app.celery_app import celery_app
from app.config import (
    CATEGORIES, DISCOUNT_MIN_PCT, REDIS_URL
)
from app.fetcher_meli import search_products
from app.filters import compute_discount, get_seller_level, good_seller
from app.publisher_telegram import send_offer, make_affiliate_link

rds = redis.from_url(REDIS_URL)

def format_currency(v):
    try:
        return f"R$ {float(v):.2f}"
    except Exception:
        return "-"

def build_caption(item, discount_pct: int, seller_level: str, affiliate_url: str) -> str:
    title = item.get("title") or "Oferta"
    price_now = item.get("price") or 0
    original = item.get("original_price") or 0

    return (
        f"⚡ <b>OFERTA RELÂMPAGO</b>\n\n"
        f"{title}\n\n"
        f"De: <s>{format_currency(original)}</s>\n"
        f"Por: <b>{format_currency(price_now)}</b> ({discount_pct}% OFF)\n"
        f"🏆 Vendedor: {seller_level or '—'}\n\n"
        f"👉 <a href='{affiliate_url}'>Conferir no Mercado Livre</a>\n"
        f"#promo #ofertas"
    )

async def pick_and_publish_for_term(term: str, max_posts: int = 2):
    results = await search_products(term, limit=60)
    sent = 0

    for it in results:
        if sent >= max_posts:
            break

        item_id = it.get("id")
        price_now = it.get("price")
        original = it.get("original_price")  # pode ser None
        discount = compute_discount(price_now, original)

        # Desconto mínimo
        if discount is None or discount < DISCOUNT_MIN_PCT:
            continue

        # Deduplicação (30 dias)
        if item_id:
            already = await rds.get(f"sent:item:{item_id}")
            if already:
                continue

        # Reputação do vendedor
        seller_id = (it.get("seller") or {}).get("id")
        seller_level = await get_seller_level(seller_id) if seller_id else None
        if not good_seller(seller_level):
            continue

        affiliate_url = make_affiliate_link(it.get("permalink"))
        caption = build_caption(it, int(discount), seller_level or "—", affiliate_url)

        # Publicar no Telegram
        photo = it.get("thumbnail") or it.get("thumbnail_id") or ""
        await send_offer(photo, caption)

        # Marcar como enviado
        if item_id:
            await rds.setex(f"sent:item:{item_id}", 30*24*3600, "1")

        sent += 1

@celery_app.task(name="publish_offers_all_categories")
def publish_offers_all_categories():
    async def _run():
        for term in CATEGORIES:
            try:
                await pick_and_publish_for_term(term, max_posts=2)
                await asyncio.sleep(2)
            except Exception:
                # Em produção: registrar no logger/Sentry
                continue
    asyncio.run(_run())
