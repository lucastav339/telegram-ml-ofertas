import asyncio
import json
import time
from datetime import datetime
import redis.asyncio as redis

from app.celery_app import celery_app
from app.config import (
    CATEGORIES, DISCOUNT_MIN_PCT, RATING_MIN, REVIEWS_MIN, SCHEDULE_MINUTES, REDIS_URL
)
from app.fetcher_meli import search_products
from app.filters import compute_discount, get_seller_level, good_seller
from app.publisher_telegram import send_offer, make_affiliate_link

rds = redis.from_url(REDIS_URL)

def format_caption(item, discount_pct: int, seller_level: str, affiliate_url: str) -> str:
    title = item.get("title")
    price_now = item.get("price")
    original = item.get("original_price")
    rating = item.get("reviews_rating") or "—"
    reviews = item.get("reviews_qty") or "—"

    return (
        f"⚡ <b>OFERTA RELÂMPAGO</b>\n\n"
        f"{title}\n\n"
        f"De: <s>R$ {original:.2f}</s>\n"
        f"Por: <b>R$ {price_now:.2f}</b> ({discount_pct}% OFF)\n"
        f"⭐ Média: {rating} ({reviews} avaliações)\n"
        f"🏆 Vendedor: {seller_level}\n\n"
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
        photo = it.get("thumbnail") or it.get("thumbnail_id")
        price_now = it.get("price")
        original = it.get("original_price")  # pode vir None; se None, pulamos
        discount = compute_discount(price_now, original)

        # filtro de desconto
        if discount is None or discount < DISCOUNT_MIN_PCT:
            continue

        # dedupe (evitar repetição nos últimos 30 dias)
        already = await rds.get(f"sent:item:{item_id}")
        if already:
            continue

        # reputação do vendedor
        seller_id = (it.get("seller") or {}).get("id")
        seller_level = await get_seller_level(seller_id) if seller_id else None
        if not good_seller(seller_level):
            continue

        # (opcional) reviews — em MVP, pulamos ou deixamos "—"

        affiliate_url = make_affiliate_link(it.get("permalink"))
        caption = format_caption(it, int(discount), seller_level or "—", affiliate_url)

        # publicar
        await send_offer(photo, caption)

        # marcar no Redis por 30 dias
        await rds.setex(f"sent:item:{item_id}", 30*24*3600, "1")

        sent += 1

@celery_app.task(name="publish_offers_all_categories")
def publish_offers_all_categories():
    # executado pelo Celery Beat, chama o fluxo async
    async def _run():
        for term in CATEGORIES:
            try:
                await pick_and_publish_for_term(term, max_posts=2)
                await asyncio.sleep(2)
            except Exception:
                # em produção: logar no Sentry
                continue

    asyncio.run(_run())
