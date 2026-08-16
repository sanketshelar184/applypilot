import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-at-least-thirty-two-characters")
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123456:test-token")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

