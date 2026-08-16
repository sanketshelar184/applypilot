import structlog
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

from app.core.config import get_settings
from app.core.database import AsyncSessionFactory
from app.schemas.auth import TelegramUserData
from app.services.users import upsert_telegram_user

logger = structlog.get_logger()


def main_menu() -> InlineKeyboardMarkup:
    settings = get_settings()
    app_button = InlineKeyboardButton(
        "📝 Create Resume", web_app=WebAppInfo(url=f"{settings.frontend_url}/?action=create")
    )
    return InlineKeyboardMarkup(
        [
            [app_button],
            [InlineKeyboardButton("📄 My Resumes", web_app=WebAppInfo(url=settings.frontend_url))],
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if update.effective_message is None or user is None:
        return
    async with AsyncSessionFactory() as db:
        await upsert_telegram_user(
            db,
            TelegramUserData(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                language_code=user.language_code,
            ),
        )
    await update.effective_message.reply_text(
        f"Welcome, {user.first_name}! 👋\n\n"
        "Send us the job you want. We prepare your application for it.\n\n"
        "Start with a professional, ATS-friendly resume.",
        reply_markup=main_menu(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(
            "Use Create Resume to open the secure resume workspace. "
            "Your work is saved to your Telegram-linked account."
        )


def build_application() -> Application:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")
    application = Application.builder().token(settings.telegram_bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    return application


def run() -> None:
    logger.info("telegram_bot_starting")
    build_application().run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    run()
