# Telegram ML Ofertas (MVP pronto para Render)

Canal de ofertas do Mercado Livre com bot do Telegram. Busca produtos, filtra por desconto e reputação, evita repetição e publica com link de afiliado.

## 1) O que você precisa
- Bot do Telegram (token via BotFather) e canal onde o bot é admin.
- Conta no Render.com.
- Redis gerenciado (Redis Cloud/Upstash) → pegue a `REDIS_URL`.
- Seu template de afiliado já incluso (com base no link que você enviou).

## 2) Variáveis de ambiente (Render → Environment)
Copie do `.env.example`:
- `TELEGRAM_BOT_TOKEN` = token do BotFather
- `TELEGRAM_CHANNEL_ID` = @seucanal (ou ID numérico -100...)
- `ML_SITE_ID` = MLB
- `AFFILIATE_DEEPLINK_TEMPLATE` = (já configurado neste repo)
- `DISCOUNT_MIN_PCT` = 15 (ajuste como quiser)
- `RATING_MIN` = 4.2 (opcional, não usado no MVP)
- `REVIEWS_MIN` = 50 (opcional, não usado no MVP)
- `SCHEDULE_MINUTES` = 60 (1h) / 180 / 360
- `CATEGORIES` = termos separados por vírgula (ex.: "smartphone, notebook, tv 4k")
- `REDIS_URL` = URL completa do Redis (ex.: rediss://default:senha@host:porta)

## 3) Render: serviços
Crie **3 serviços** (mesmo repo):
- **Web Service (FastAPI)**
  - Build: `pip install -r requirements.txt`
  - Start: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
- **Background Worker (Celery Worker)**
  - Build: `pip install -r requirements.txt`
  - Start: `celery -A app.celery_app worker -Q default -l info`
- **Background Worker (Celery Beat)**
  - Build: `pip install -r requirements.txt`
  - Start: `celery -A app.celery_app beat -l info`

Defina as MESMAS variáveis de ambiente nos 3 serviços.

## 4) Teste rápido
- Abra `https://SEU_WEB_SERVICE.onrender.com/healthz` → deve retornar `{"ok": true}`.
- Dispare um ciclo manual em `POST https://SEU_WEB_SERVICE.onrender.com/run-now` (pelo Insomnia/Postman).
- Verifique se chegaram ofertas no seu canal do Telegram.

## 5) Como funciona (MVP)
- Busca pública na API do ML por cada termo em `CATEGORIES` (60 itens).
- Calcula desconto com base em `price` e `original_price` (quando disponível).
- Filtra por `DISCOUNT_MIN_PCT` e reputação do vendedor (níveis 5_/4_).
- Dedup no Redis (30 dias).
- Publica foto + texto + link de afiliado (template personalizado).

## 6) Evoluções
- Usar Prices API (OAuth) para desconto mais preciso.
- Pegar reviews reais e filtrar por `RATING_MIN`/`REVIEWS_MIN`.
- Registrar em Postgres, A/B testing e painel de controle.

## 7) Segurança
- Nunca commitar tokens. Use apenas Environment Variables no Render.
