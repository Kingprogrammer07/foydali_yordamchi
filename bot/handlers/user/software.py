"""Kompyuter dasturlarini yuborish (catalog'dan generic)."""
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from bot.content.catalog import SOFTWARE
from bot.handlers.user.books import send_items

router = Router()


@router.message(F.text.in_(set(SOFTWARE)), StateFilter(None), F.chat.type == "private")
async def send_software(message: Message):
    await send_items(message, SOFTWARE[message.text])
