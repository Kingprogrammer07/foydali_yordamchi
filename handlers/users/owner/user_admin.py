from aiogram import types
from loader import dp
from keyboards.keyboard.all_button import havola

@dp.message_handler(commands = "admin")
async def always(message: types.Message):
    await message.reply(
        text = "<b>Adminga murojaat qilish uchun ushbu havola ustiga bosing</b>✅",
        reply_markup = havola
    )