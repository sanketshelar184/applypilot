import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from urllib.parse import parse_qsl

from app.schemas.auth import TelegramUserData


class TelegramAuthError(ValueError):
    pass


@dataclass(frozen=True)
class ValidatedTelegramData:
    user: TelegramUserData
    auth_date: int
    query_id: str | None


def validate_telegram_init_data(
    init_data: str, bot_token: str, max_age_seconds: int, now: int | None = None
) -> ValidatedTelegramData:
    if not init_data or not bot_token:
        raise TelegramAuthError("Telegram authentication is not configured")

    fields = dict(parse_qsl(init_data, keep_blank_values=True, strict_parsing=True))
    received_hash = fields.pop("hash", None)
    if not received_hash:
        raise TelegramAuthError("Missing Telegram signature")

    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(fields.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    expected_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_hash, received_hash):
        raise TelegramAuthError("Invalid Telegram signature")

    try:
        auth_date = int(fields["auth_date"])
        user = TelegramUserData.model_validate(json.loads(fields["user"]))
    except (KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
        raise TelegramAuthError("Invalid Telegram authentication payload") from exc

    current_time = int(time.time()) if now is None else now
    if auth_date > current_time + 30 or current_time - auth_date > max_age_seconds:
        raise TelegramAuthError("Telegram authentication has expired")

    return ValidatedTelegramData(user=user, auth_date=auth_date, query_id=fields.get("query_id"))

