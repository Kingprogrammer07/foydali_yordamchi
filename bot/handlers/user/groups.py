"""Guruh chatlari: kalit so'z javoblari + yangi/chiqgan a'zolar."""
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

router = Router()

_PAROL = {
    "parol", "password", "pass", "kod", "zip paroli", "kodi", "buni kodi nima",
    "kodi nima", "paroli nima", "nima kod", "nima buni kodi", "paroli nima buni", "buni paroli nima",
}
_YORDAM = {
    "yordam", "help", "yordam berish", "yordam bervoringla", "yordam beringlar", "yordam bervoringlar",
}
_KERAK = {"kerak", "topib bering", "telegram bot", "bot"}


@router.message(F.new_chat_members)
async def on_join(message: Message):
    for user in message.new_chat_members:
        await message.answer(
            f"Assalom-u alaykum, {user.mention_html()}  Xush kelibsiz!\n<b>Qanday yordam bera olamiz 😉</b>"
        )
    try:
        await message.delete()
    except Exception:
        pass


@router.message(F.left_chat_member)
async def on_leave(message: Message):
    try:
        await message.delete()
    except Exception:
        pass


@router.message(StateFilter(None), ~(F.chat.type == "private"), F.text)
async def keyword_reply(message: Message):
    text = (message.text or "").lower()
    if text in _PAROL:
        await message.reply(
            "📁 <b>Hamma fayllarni 🔐paroli o`sha faylni pastiga yozib qo`yilgan..</b>\n"
            "Agar yozilmagan bo`lsa, Buni sinab ko`ring: <pre>@windowsuzprogrammaa</pre> yoki <pre>@windowsuzprogramm</pre>\n\n"
            "<b>Shularda ham xatolik bersa /admin bilan bog`laning </b>‼️"
        )
    elif text in _YORDAM:
        await message.reply(
            "🤔 <b>Muammolaringiz bo`lsa screenshot qilib tashlasangiz tezroq muammoyizga yechim topasiz </b>😉"
        )
    elif text in _KERAK:
        await message.reply(
            "<b>Birorta Programma yoki dastur kerak bo`lsa 🧑🏼‍💻 adminga yozavering(/admin)</b>"
        )
