from aiogram import types
from loader import dp
from aiogram.dispatcher.filters.builtin import CommandHelp
from keyboards.inline.kanal_va_bot_url import btn_url


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    if message.chat.type == "private":
        text = ("⚙️<b>Botning ishlashi\n🆘Menyudan foydalaning\n🎛Pastdagi tugmalardan foydalaning\nTushunmasangiz yoki savollar bo`lsa adminga murojaat qiling!\n💻Admin: @java_strong</b>\nBoshidan ishlatish /start")
        await message.answer(text = text, reply_markup = btn_url)
