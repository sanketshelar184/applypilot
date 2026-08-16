from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import CurrentUser, DatabaseSession
from app.core.config import get_settings
from app.core.security import create_access_token
from app.schemas.auth import AuthResponse, TelegramAuthRequest, UserResponse
from app.services.telegram_auth import TelegramAuthError, validate_telegram_init_data
from app.services.users import to_user_response, upsert_telegram_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/telegram", response_model=AuthResponse)
async def authenticate_telegram(payload: TelegramAuthRequest, db: DatabaseSession) -> AuthResponse:
    settings = get_settings()
    try:
        validated = validate_telegram_init_data(
            payload.init_data,
            settings.telegram_bot_token,
            settings.telegram_auth_max_age_seconds,
        )
    except TelegramAuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    user = await upsert_telegram_user(db, validated.user)
    await db.refresh(user, attribute_names=["telegram_account"])
    return AuthResponse(
        access_token=create_access_token(str(user.id)), user=to_user_response(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_me(user: CurrentUser) -> UserResponse:
    return to_user_response(user)

