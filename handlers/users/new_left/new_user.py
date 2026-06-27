from loader import dp, bot
from aiogram.types import Message, ContentType

@dp.message_handler(content_types = ContentType.NEW_CHAT_MEMBERS)
async def somebody_added(message: Message):
    for user in message.new_chat_members:
        await message.answer(text = f"Assalom-u alaykum, {user.get_mention()}  Xush kelibsiz!\n<b>Qanday yordam bera olamiz 😉</b>")
        await message.delete()

@dp.message_handler(content_types = ContentType.LEFT_CHAT_MEMBER)
async def somebody_deled(message: Message):
    await message.delete()