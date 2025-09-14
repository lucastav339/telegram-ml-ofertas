import os

# Helpers ----------------------------------------------------------
def _env_bool(name: str, default: bool = False) -> bool:
    return str(os.getenv(name, str(default))).strip().lower() in ("1", "true", "yes", "y", "on")

def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name, None)
    if raw is None:
        return default
    try:
        return int(float(raw))
    except Exception:
        return default

def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name, None)
    if raw is None:
        return default
    try:
        return float(raw)
    except Exception:
        return default

# Telegram ---------------------------------------------------------
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID: str = os.getenv("TELEGRAM_CHANNEL_ID", "")  # ex.: @seucanal ou -100123...

# Mercado Livre / Afiliados ---------------------------------------
# Template já baseado no link que você enviou (substitui {permalink} pelo slug do produto)
AFFILIATE_TEMPLATE: str = os.getenv(
    "AFFILIATE_DEEPLINK_TEMPLATE",
    "https://www.mercadolivre.com.br/social/{permalink}?matt_tool=33493852&forceInApp=true&ref=BIpR7TPYySg1Qthm0pqN4n1lfAqxl2nU%2FzDpXE4yAC5EU1HJxyWNsqAN5jwUdUCtFN4j8SZ5RdiHxidr5kdz%2FgHyJkZoBYbZrZ6kifW1ZdrUOXqCd1m4yLwgGDbXuctrKGiOgbqlOZMlkOEgzz1V43p7fwn4uTnCeFBt95Zz3i%2F4Ji%2BaVnEGHoxx0UJOCBvr1Pr1hMc%3D",
)
ML_SITE_ID: str = os.getenv("ML_SITE_ID", "MLB")

# Filtros ----------------------------------------------------------
DISCOUNT_MIN_PCT: int = _env_int("DISCOUNT_MIN_PCT", 10)
RATING_MIN: float = _env_float("RATING_MIN", 4.2)   # (ainda opcional no MVP)
REVIEWS_MIN: int = _env_int("REVIEWS_MIN", 50)      # (ainda opcional no MVP)

# Redis / Agenda ---------------------------------------------------
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SCHEDULE_MINUTES: int = _env_int("SCHEDULE_MINUTES", 60)

# Categorias / termos de busca (separados por vírgula) -------------
CATEGORIES = [
    c.strip() for c in os.getenv("CATEGORIES", "smartphone, notebook, tv 4k").split(",") if c.strip()
]

# Modo de teste (ignora filtros e força postar ao menos 1 item por termo)
DEBUG_MODE: bool = _env_bool("DEBUG_MODE", False)
