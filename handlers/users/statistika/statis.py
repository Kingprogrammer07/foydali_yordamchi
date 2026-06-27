from loader import dp
from aiogram.dispatcher.filters import Text
from data.post_data import db
from aiogram import types


@dp.message_handler(Text(equals = "Statistika📶"))
async def statistik(message: types.Message):
    if message.chat.type == "private":
        await message.reply(text = f"👁‍🗨<b>Hozirda botning {db.user_count()} ta foydalanuvchisi bor</b>")
