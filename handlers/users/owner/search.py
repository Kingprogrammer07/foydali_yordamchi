from aiogram import types
from loader import dp
from keyboards.inline.bot_post_ctr import ishlatish

@dp.message_handler(commands = "search_about")
async def always(message: types.Message):
    if message.chat.type == 'private':
        await message.reply_document(document = "https://t.me/windowsuzprogrammaa/425", caption = "** Videoda batafsil ^\n<b>Teleram foydalanuvchilarini Username bo`lmasa va Telefon raqamini bilmasangiz yoki Topmoqchi bolgan foydalanuvchi sizni qora ro`yhatga(Blokka) kirgizgan bo`lsa ham topib beruvchi bot..</b>(Topish topmasligi Telegram turiga bog`liq!)\n\nAgar ID raqamni qayerda olishni bilmasangiz ~ @ShowJsonBot ~ orqali olishingiz mumkin", reply_markup = ishlatish)