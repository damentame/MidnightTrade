# ctrader-xau-lsfvg-bot

Automated XAUUSD cTrader strategy bot with FastAPI dashboard endpoints.

## Quickstart
1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Start services:
   ```bash
   docker compose up --build
   ```
3. Run migrations:
   ```bash
   docker compose exec backend alembic upgrade head
   ```

## cTrader OAuth
- Start auth flow: `GET /api/ctrader/auth/start`
- Callback endpoint: `GET /api/ctrader/callback`

## Run bot runner
Inside backend container:
```bash
python -m app.jobs.runner
```

## Dashboard
- API base: `http://localhost:8000/api`
- UI (minimal): `http://localhost:8000/`

## Safety
Use demo first. In dev, set `trading_enabled=false` before enabling real execution.
