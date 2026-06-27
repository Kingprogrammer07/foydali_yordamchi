"""Anti-flood — bir foydalanuvchidan juda tez-tez kelgan xabarlarni tashlaydi."""
import time

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.config import THROTTLE_RATE


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate: float = THROTTLE_RATE):
        self.rate = rate
        self._last: dict[int, float] = {}

    async def __call__(self, handler, event: Message, data: dict):
        # Albom (media group) xabarlarini throttle qilmaymiz — aks holda albom buziladi
        if event.media_group_id is not None:
            return await handler(event, data)
        user = event.from_user
        if user is not None:
            now = time.monotonic()
            if now - self._last.get(user.id, 0.0) < self.rate:
                return  # throttled — handler chaqirilmaydi
            self._last[user.id] = now
        return await handler(event, data)
