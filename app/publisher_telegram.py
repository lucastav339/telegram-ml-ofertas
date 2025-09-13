import math
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

def compute_discount(now: float | None, original: float | None) -> float | None:
    if not now or not original or original <= now:
        return None
    return round(100 * (1 - (now / original)))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=8))
async def get_seller_level(seller_id: int) -> str | None:
    # Reputação do vendedor (nível)
    url = f"https://api.mercadolibre.com/users/{seller_id}"
    async with httpx.AsyncClient(timeout=20) as cx:
        r = await cx.get(url)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        data = r.json()
        rep = data.get("seller_reputation", {}) or {}
        return rep.get("level_id")  # ex.: "5_green", "4_yellow", etc.

def good_seller(level_id: str | None) -> bool:
    if not level_id:
        return False
    # regra simples: aceitar níveis "5_" (verde) e "4_"
    return level_id.startswith("5") or level_id.startswith("4")
