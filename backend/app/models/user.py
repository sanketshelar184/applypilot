import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDTimestampMixin


class SubscriptionStatus(StrEnum):
    FREE = "free"
    PRO = "pro"
    EXPIRED = "expired"


class User(UUIDTimestampMixin, Base):
    __tablename__ = "users"

    subscription_status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus, name="subscription_status", native_enum=False),
        default=SubscriptionStatus.FREE,
        nullable=False,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    telegram_account: Mapped["TelegramAccount"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    resumes: Mapped[list["Resume"]] = relationship(back_populates="user")


class TelegramAccount(UUIDTimestampMixin, Base):
    __tablename__ = "telegram_accounts"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    telegram_user_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )
    username: Mapped[str | None] = mapped_column(String(64))
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(128))
    language_code: Mapped[str | None] = mapped_column(String(16))
    user: Mapped[User] = relationship(back_populates="telegram_account")


from app.models.resume import Resume  # noqa: E402
