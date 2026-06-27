from loader import dp, bot
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from keyboards.keyboard.all_button import keyboard
from aiogram.dispatcher import FSMContext
from keyboards.inline.newpst import back
from states.video_down import video_url
from .all_request import instagram, tiktok, you_tube
from pytube import YouTube

# Orqaga 🔙

@dp.message_handler(Text(equals = "📹 Video yuklash"))
async def dowland(message: Message):
    if message.chat.type == "private":
        await message.reply(text = "Menga ** <b> 📷 Instagram, 📹YouTube, 🕹TikTok</b> ** tarmoqlaridan video, rasm yoki story havolasini tashlang va men Yuklab beraman😉", reply_markup = back)
        await video_url.get_url.set()

@dp.message_handler(state = video_url.get_url, content_types = ['text'])
async def down_go(message: Message, state: FSMContext):
    chat_id = message.chat.id
    url = message.text
    await message.delete()
    about_bot = "@foydali_dastur_kitobbot <b>orqali yuklab olindi 📥</b>"
    if url.startswith("https://youtu.be/") or url.startswith("https://www.youtube.com/"):
        await bot.send_message(chat_id = chat_id, text = "⏳", reply_markup = keyboard)
        url: str = f"{YouTube(url)}"
        url = url.replace("<pytube.__main__.YouTube object: videoId=", "").replace(">", "")
        try:
            await message.answer_video(video = you_tube(url)[1], caption = f"{you_tube(url)[0]}\n\n{about_bot}</b>")
        except:
            await message.answer(text = "Afsuski videoni yuklab bo`lmadi 😞")
        await state.finish()

    elif url.startswith("https://www.instagram.com/") or url.startswith("https://instagram.com/"):
        await bot.send_message(chat_id = chat_id, text = "⏳", reply_markup = keyboard)
        try:
            await message.answer_document(document = instagram(url), caption = f"{about_bot}")
        except:
            await message.answer(text = "Afsuski video yoki rasmni yuklab bo`lmadi 😞")
        await state.finish()

    elif url.startswith("https://vt.tiktok.com/"):
        await bot.send_message(chat_id = chat_id, text = "⏳", reply_markup = keyboard)
        try:
            await message.answer_document(document = tiktok(url), caption = f"{about_bot}")
        except:
            await message.answer(text = "Afsuski video yoki rasmni yuklab bo`lmadi 😞")
        await state.finish()

            