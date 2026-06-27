"""IsAdmin — adminlikni DB'dan JONLI tekshiradi (import-snapshot bug yo'q)."""
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from bot.database.repositories import AdminRepo


class IsAdmin(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery, admins: AdminRepo) -> bool:
        if event.from_user is None:
            return False
        return await admins.exists(event.from_user.id)
