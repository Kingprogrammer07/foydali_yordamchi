"""Albom (media group) yig'uvchi — Telegram albomni alohida xabarlar bilan yuboradi.

Bir media_group_id bo'yicha xabarlarni to'playdi va debounce (kutish) tugagach
faqat oxirgi xabar handler'ni `data['album']` (to'liq ro'yxat) bilan chaqiradi.
Outer middleware sifatida (filtrlashdan oldin) ulanadi.
"""
import asyncio

from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):
    def __init__(self, delay: float = 0.6):
        self.delay = delay
        self._albums: dict[str, list[Message]] = {}

    async def __call__(self, handler, event: Message, data: dict):
        if event.media_group_id is None:
            return await handler(event, data)

        key = event.media_group_id
        self._albums.setdefault(key, []).append(event)

        await asyncio.sleep(self.delay)

        bucket = self._albums.get(key)
        # Faqat (kutishdan keyin) eng oxirgi kelgan xabar to'plamni handler'ga uzatadi
        if not bucket or bucket[-1].message_id != event.message_id:
            return  # boshqa albom a'zosi — yutiladi

        album = sorted(self._albums.pop(key), key=lambda m: m.message_id)
        data["album"] = album
        return await handler(event, data)
