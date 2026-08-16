import hashlib
import hmac
import json
from urllib.parse import urlencode

import pytest

from app.services.telegram_auth import TelegramAuthError, validate_telegram_init_data

TOKEN = "123456:test-token"


def signed_payload(auth_date: int, user_id: int = 42) -> str:
    fields = {
        "auth_date": str(auth_date),
        "query_id": "AAE-test",
        "user": json.dumps(
            {"id": user_id, "first_name": "Ada", "username": "ada"}, separators=(",", ":")
        ),
    }
    check = "\n".join(f"{key}={value}" for key, value in sorted(fields.items()))
    secret = hmac.new(b"WebAppData", TOKEN.encode(), hashlib.sha256).digest()
    fields["hash"] = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    return urlencode(fields)


def test_accepts_valid_init_data() -> None:
    result = validate_telegram_init_data(signed_payload(1_000), TOKEN, 900, now=1_500)
    assert result.user.id == 42
    assert result.user.first_name == "Ada"


def test_rejects_tampered_user() -> None:
    payload = signed_payload(1_000).replace("Ada", "Grace")
    with pytest.raises(TelegramAuthError, match="signature"):
        validate_telegram_init_data(payload, TOKEN, 900, now=1_500)


def test_rejects_expired_init_data() -> None:
    with pytest.raises(TelegramAuthError, match="expired"):
        validate_telegram_init_data(signed_payload(100), TOKEN, 900, now=1_500)
