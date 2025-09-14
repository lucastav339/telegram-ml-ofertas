import logging
from app.config import DISCOUNT_MIN_PCT, DEBUG_MODE
from app.utils import (
    search_products, compute_discount, get_seller_level, good_seller,
    make_affiliate_link, build_caption, send_offer, rds
)

log = logging.getLogger("tasks")


async def pick_and_publish_for_term(term: str, max_posts: int = 2):
    results = await search_products(term, limit=60)
    sent = 0
    log.info(f"[{term}] resultados: {len(results)} | DEBUG_MODE={DEBUG_MODE}")

    for it in results:
        if sent >= max_posts:
            break

        item_id = it.get("id")
        price_now = it.get("price")
        original = it.get("original_price")
        discount = compute_discount(price_now, original)

        if not DEBUG_MODE:
            # Desconto mínimo
            if discount is None or discount < DISCOUNT_MIN_PCT:
                log.info(f"[{term}] SKIP {item_id}: desconto insuficiente ({discount})")
                continue

            # Deduplicação (30 dias)
            if item_id:
                already = await rds.get(f"sent:item:{item_id}")
                if already:
                    log.info(f"[{term}] SKIP {item_id}: já enviado")
                    continue

            # Reputação do vendedor
            seller_id = (it.get("seller") or {}).get("id")
            seller_level = await get_seller_level(seller_id) if seller_id else None
            if not good_seller(seller_level):
                log.info(f"[{term}] SKIP {item_id}: reputação ruim/indefinida ({seller_level})")
                continue
        else:
            # Em DEBUG: ignora filtros e reputação
            seller_level = "debug"

        affiliate_url = make_affiliate_link(it.get("permalink"))
        caption = build_caption(it, int(discount or 0), seller_level or "—", affiliate_url)
        photo = it.get("thumbnail") or it.get("thumbnail_id") or ""

        try:
            await send_offer(photo, caption)
            log.info(f"[{term}] OK postado {item_id}")
        except Exception as e:
            log.error(f"[{term}] ERRO ao postar {item_id}: {e}")
            continue

        if item_id:
            await rds.setex(f"sent:item:{item_id}", 30*24*3600, "1")

        sent += 1

    log.info(f"[{term}] enviados: {sent}")
