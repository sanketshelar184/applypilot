import uuid
from enum import StrEnum

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDTimestampMixin


class ResumeStatus(StrEnum):
    DRAFT = "draft"
    COMPLETE = "complete"
    ARCHIVED = "archived"


class Resume(UUIDTimestampMixin, Base):
    __tablename__ = "resumes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(160), default="Untitled Resume", nullable=False)
    target_role: Mapped[str | None] = mapped_column(String(160))
    status: Mapped[ResumeStatus] = mapped_column(
        Enum(ResumeStatus, name="resume_status", native_enum=False),
        default=ResumeStatus.DRAFT,
        nullable=False,
    )
    is_master: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    professional_summary: Mapped[str | None] = mapped_column(Text)
    user: Mapped["User"] = relationship(back_populates="resumes")


from app.models.user import User  # noqa: E402
