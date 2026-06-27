"""Maktab darsliklari va Booknomy kitoblarini yuborish (catalog'dan generic)."""
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from bot.content.catalog import BOOKS, Item

router = Router()


async def send_items(message: Message, items: list[Item]) -> None:
    for item in items:
        if item.method == "photo":
            await message.answer_photo(item.file, caption=item.caption)
        else:
            await message.answer_document(item.file, caption=item.caption)


@router.message(F.text.in_(set(BOOKS)), StateFilter(None), F.chat.type == "private")
async def send_book(message: Message):
    await send_items(message, BOOKS[message.text])
