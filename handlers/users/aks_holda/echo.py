from aiogram import types
from loader import dp

@dp.message_handler()
async def else_func(message: types.Message):
    if message.chat.type == 'private':
        await message.reply(text = "⚙️Berilgan parametrlardan birini tanlang!\n🎛Menyudan foydalaning yoki /help 🆘tugmasini bosing!")