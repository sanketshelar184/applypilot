from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import TelegramAccount, User
from app.schemas.auth import TelegramUserData, UserResponse


async def upsert_telegram_user(db: AsyncSession, data: TelegramUserData) -> User:
    result = await db.execute(
        select(TelegramAccount)
        .options(selectinload(TelegramAccount.user))
        .where(TelegramAccount.telegram_user_id == data.id)
    )
    account = result.scalar_one_or_none()
    if account is None:
        user = User()
        account = TelegramAccount(
            user=user,
            telegram_user_id=data.id,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            language_code=data.language_code,
        )
        db.add(account)
    else:
        user = account.user
        account.username = data.username
        account.first_name = data.first_name
        account.last_name = data.last_name
        account.language_code = data.language_code
        user.last_seen_at = datetime.now(UTC)

    await db.commit()
    await db.refresh(user)
    return user


def to_user_response(user: User) -> UserResponse:
    account = user.telegram_account
    return UserResponse(
        id=str(user.id),
        first_name=account.first_name,
        last_name=account.last_name,
        username=account.username,
        language_code=account.language_code,
        subscription_status=user.subscription_status.value,
    )

