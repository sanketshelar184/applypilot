# ApplyPilot

ApplyPilot is a Telegram-first AI resume and job application assistant. Its promise is simple: **Send us the job you want. We prepare your application for it.**

This repository implements Phase 1: a Telegram bot opens a secure Telegram Mini App, the backend validates Telegram identity server-side, creates or updates the user in PostgreSQL, and serves a personal resume dashboard.

## Architecture

- `frontend/` — Next.js, TypeScript, Tailwind CSS Telegram Mini App
- `backend/` — FastAPI API, async SQLAlchemy, Alembic, and async Telegram bot
- PostgreSQL — normalized user, channel identity, and resume foundation
- Stateless bearer sessions — issued only after Telegram init-data HMAC and age verification

The core `User` is separate from `TelegramAccount`, allowing future web and WhatsApp identities. API routes depend on services and authenticated ownership context; Phase 2 resume sections can be added without changing authentication or channel code.

## Local setup

1. Copy `.env.example` to `.env` and replace all secrets. Generate `SECRET_KEY` with a cryptographically secure random value.
2. In BotFather, create a bot and Mini App, set its URL to your HTTPS frontend URL, and add the token/username to `.env`.
3. Start PostgreSQL with `docker compose up -d postgres`.
4. Backend:
   ```powershell
   cd backend
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -e ".[dev]"
   alembic upgrade head
   uvicorn app.main:app --reload
   ```
5. Bot (a second terminal): `cd backend; python -m app.telegram.bot`
6. Frontend:
   ```powershell
   cd frontend
   Copy-Item ..\.env.example .env.local
   npm install
   npm run dev
   ```

Telegram requires an HTTPS Mini App URL. For local device testing, expose port 3000 through a trusted HTTPS tunnel and update `FRONTEND_URL` and BotFather. The API origin must be present in `CORS_ORIGINS`.

## Database migrations

Run `cd backend; alembic upgrade head`. Production startup applies committed migrations and never uses `create_all`.

## Authentication and security

The Mini App sends Telegram `initData` unchanged to `POST /api/v1/auth/telegram`. The backend reconstructs the data-check string, verifies its HMAC with the bot token, checks `auth_date`, and only then upserts the identity and issues a JWT. Never send the bot token or application secret to the frontend.

All resume queries include the current user ID. CORS is explicit, logs avoid auth payloads, and `/docs` documents the grouped API. Use a secrets manager and TLS in production.

## Testing

```powershell
cd backend
pytest
ruff check .
```

Frontend checks: `npm run typecheck` and `npm run build`.

## Deployment

The frontend is Vercel-compatible and emits a standalone Next.js build. Backend and bot share a Docker image but run as separate stateless processes, suitable for Render, Railway, Fly.io, or container platforms. Use managed PostgreSQL, an HTTPS frontend/API, a long random secret, and a webhook-based bot deployment at larger scale.

## Phase 2 readiness

The `Resume` aggregate and ownership boundary already exist. Phase 2 should add versioned personal details, education, experience, projects, skills, certifications, editor endpoints, and the first ATS template through migrations and domain services—not by expanding route handlers.

