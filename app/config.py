import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")  # ex.: @seucanal ou -100123...
AFFILIATE_TEMPLATE = os.getenv(
    "AFFILIATE_DEEPLINK_TEMPLATE",
    "https://www.mercadolivre.com.br/social/{permalink}?matt_tool=33493852&forceInApp=true&ref=BIpR7TPYySg1Qthm0pqN4n1lfAqxl2nU%2FzDpXE4yAC5EU1HJxyWNsqAN5jwUdUCtFN4j8SZ5RdiHxidr5kdz%2FgHyJkZoBYbZrZ6kifW1ZdrUOXqCd1m4yLwgGDbXuctrKGiOgbqlOZMlkOEgzz1V43p7fwn4uTnCeFBt95Zz3i%2F4Ji%2BaVnEGHoxx0UJOCBvr1Pr1hMc%3D",
)
ML_SITE_ID = os.getenv("ML_SITE_ID", "MLB")

# Filtros
try:
    DISCOUNT_MIN_PCT = float(os.getenv("DISCOUNT_MIN_PCT", "15"))
except Exception:
    DISCOUNT_MIN_PCT = 15.0

try:
    RATING_MIN = float(os.getenv("RATING_MIN", "4.2"))
except Exception:
    RATING_MIN = 4.2

try:
    REVIEWS_MIN = int(os.getenv("REVIEWS_MIN", "50"))
except Exception:
    REVIEWS_MIN = 50

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Agendamento (em minutos)
try:
    SCHEDULE_MINUTES = int(os.getenv("SCHEDULE_MINUTES", "60"))
except Exception:
    SCHEDULE_MINUTES = 60

# Categorias/termos
CATEGORIES = [c.strip() for c in os.getenv("CATEGORIES", "eletronicos, casa, moda").split(",") if c.strip()]
