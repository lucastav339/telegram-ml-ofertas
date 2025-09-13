import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")  # ex.: @seucanal ou -100123...
AFFILIATE_TEMPLATE = os.getenv("AFFILIATE_DEEPLINK_TEMPLATE", "https://SEU-TEMPLATE?url={permalink}")
ML_SITE_ID = os.getenv("ML_SITE_ID", "MLB")

# Filtros
DISCOUNT_MIN_PCT = float(os.getenv("DISCOUNT_MIN_PCT", "15"))
RATING_MIN = float(os.getenv("RATING_MIN", "4.2"))  # usado quando disponível
REVIEWS_MIN = int(os.getenv("REVIEWS_MIN", "50"))   # usado quando disponível

# Redis (Render fornece a URL pronta)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Agendamento (em minutos)
SCHEDULE_MINUTES = int(os.getenv("SCHEDULE_MINUTES", "60"))  # 60=1h, 180=3h, 360=6h

# Categorias/termos (separe por vírgula)
CATEGORIES = [c.strip() for c in os.getenv("CATEGORIES", "eletronicos, casa, moda").split(",") if c.strip()]
