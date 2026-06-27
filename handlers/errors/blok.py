from aiogram.utils.exceptions import BotBlocked
from loader import dp, bot 
from aiogram import types
from data.post_data import db

@dp.errors_handler(exception = BotBlocked)
async def bot_blokked(update: types.Update, exception = Exception):
    ism = update.message.from_user.full_name
    username = update.message.from_user.username
    id_raqami = update.message.from_id 
    adminlar = list(*zip(*db.admin_view()))
    exception = str(exception)
    xato = exception[11:]
    for admin_korish in adminlar: 
        if username != None:
            await bot.send_message(chat_id = admin_korish, text = f'<b>Ushbu foydalanuvchi Botni blockladi😒=></b>\nIsmi: {ism}\nUsername: @{username}\nID raqami: <pre>{id_raqami}</pre>\nBot Bloklash sababi: <b>Bot ishlamayotgan payt so`rov yuborildi!</b>\n{xato}')
        else:
            await bot.send_message(chat_id = admin_korish, text = f'<b>Ushbu foydalanuvchi Botni blockladi😒=></b>\nIsmi: {ism}\nUsername: Yo`q\nID raqami: <pre>{id_raqami}</pre>\nBot Bloklash sababi: <b>Bot ishlamayotgan payt so`rov yuborildi!</b>\n{xato}')
    return True