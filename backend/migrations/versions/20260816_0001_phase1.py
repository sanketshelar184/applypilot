"""Phase 1 user, Telegram account, and resume foundation."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260816_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("subscription_status", sa.Enum("FREE", "PRO", "EXPIRED", name="subscription_status", native_enum=False), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
    )
    op.create_index("ix_users_subscription_status", "users", ["subscription_status"])
    op.create_table(
        "telegram_accounts",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("telegram_user_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(64)), sa.Column("first_name", sa.String(128), nullable=False),
        sa.Column("last_name", sa.String(128)), sa.Column("language_code", sa.String(16)),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_telegram_accounts_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_telegram_accounts"),
        sa.UniqueConstraint("telegram_user_id", name="uq_telegram_accounts_telegram_user_id"),
        sa.UniqueConstraint("user_id", name="uq_telegram_accounts_user_id"),
    )
    op.create_index("ix_telegram_accounts_telegram_user_id", "telegram_accounts", ["telegram_user_id"])
    op.create_table(
        "resumes",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(160), nullable=False), sa.Column("target_role", sa.String(160)),
        sa.Column("status", sa.Enum("DRAFT", "COMPLETE", "ARCHIVED", name="resume_status", native_enum=False), nullable=False),
        sa.Column("is_master", sa.Boolean(), nullable=False), sa.Column("professional_summary", sa.Text()),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_resumes_user_id_users", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_resumes"),
    )
    op.create_index("ix_resumes_user_id", "resumes", ["user_id"])


def downgrade() -> None:
    op.drop_table("resumes")
    op.drop_table("telegram_accounts")
    op.drop_table("users")

