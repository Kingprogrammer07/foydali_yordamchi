"""Global xatolik handlerlari."""
import logging

from aiogram import Bot, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from bot.database.repositories import AdminRepo

logger = logging.getLogger(__name__)
router = Router()


@router.errors(ExceptionTypeFilter(TelegramForbiddenError))
async def bot_blocked(event: ErrorEvent, bot: Bot, admins: AdminRepo) -> bool:
    """Foydalanuvchi botni bloklaganda adminlarni xabardor qiladi."""
    msg = event.update.message or (event.update.callback_query.message if event.update.callback_query else None)
    user = None
    if event.update.message:
        user = event.update.message.from_user
    elif event.update.callback_query:
        user = event.update.callback_query.from_user

    if user is not None:
        username = f"@{user.username}" if user.username else "Yo`q"
        text = (
            "<b>Ushbu foydalanuvchi Botni blockladi😒=></b>\n"
            f"Ismi: {user.full_name}\nUsername: {username}\n"
            f"ID raqami: <pre>{user.id}</pre>\n"
            f"Sabab: {event.exception}"
        )
        for admin_id in await admins.all_ids():
            try:
                await bot.send_message(admin_id, text)
            except Exception:
                pass
    logger.warning("Bot bloklandi: %s", event.exception)
    return True


@router.errors()
async def errors_handler(event: ErrorEvent) -> bool:
    logger.exception("Update'da xatolik: %s", event.exception, exc_info=event.exception)
    return True
