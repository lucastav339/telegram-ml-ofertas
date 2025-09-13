import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import ML_SITE_ID

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=8))
async def search_products(term: str, limit: int = 50):
    """Busca pública por termo/categoria no site do ML Brasil (MLB)."""
    url = f"https://api.mercadolibre.com/sites/{ML_SITE_ID}/search"
    params = {"q": term, "limit": limit, "sort": "relevance"}
    async with httpx.AsyncClient(timeout=20) as cx:
        r = await cx.get(url, params=params)
        r.raise_for_status()
        return r.json().get("results", [])
