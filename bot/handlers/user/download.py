"""Video yuklash: Instagram / YouTube / TikTok havoladan media."""
import asyncio
import re

import requests
from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import config
from bot.keyboards.reply import back_post, main_menu
from bot.states import VideoDownload

router = Router()

_ABOUT = "@foydali_dastur_kitobbot <b>orqali yuklab olindi 📥</b>"
_YT_ID = re.compile(r"(?:youtu\.be/|watch\?v=|/shorts/|/embed/)([0-9A-Za-z_-]{11})")


def _headers(host: str) -> dict:
    return {"X-RapidAPI-Key": config.RAPIDAPI_KEY, "X-RapidAPI-Host": host}


def _instagram(link: str) -> str:
    url = f"https://{config.RAPIDAPI_INSTAGRAM_HOST}/index"
    resp = requests.get(url, headers=_headers(config.RAPIDAPI_INSTAGRAM_HOST), params={"url": link})
    return resp.json()["media"]


def _tiktok(link: str) -> str:
    url = f"https://{config.RAPIDAPI_TIKTOK_HOST}/"
    resp = requests.get(url, headers=_headers(config.RAPIDAPI_TIKTOK_HOST), params={"url": link, "hd": "0"})
    return resp.json().get("data").get("play")


def _youtube(video_id: str) -> tuple[str, str]:
    url = f"https://{config.RAPIDAPI_YOUTUBE_HOST}/v2/video/details"
    resp = requests.get(url, headers=_headers(config.RAPIDAPI_YOUTUBE_HOST), params={"videoId": video_id})
    media = resp.json()
    return media.get("title"), media.get("videos").get("items")[1].get("url")


@router.message(F.text == "📹 Video yuklash", StateFilter(None), F.chat.type == "private")
async def ask_url(message: Message, state: FSMContext):
    await message.reply(
        "Menga ** <b> 📷 Instagram, 📹YouTube, 🕹TikTok</b> ** tarmoqlaridan video, rasm yoki story "
        "havolasini tashlang va men Yuklab beraman😉",
        reply_markup=back_post,
    )
    await state.set_state(VideoDownload.waiting_url)


@router.message(VideoDownload.waiting_url, F.text)
async def download(message: Message, state: FSMContext, bot: Bot):
    url = message.text

    if url == "Orqaga 🔙":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=main_menu)
        return

    await state.clear()
    try:
        await message.delete()
    except Exception:
        pass

    if url.startswith(("https://youtu.be/", "https://www.youtube.com/")):
        await bot.send_message(message.chat.id, "⏳", reply_markup=main_menu)
        match = _YT_ID.search(url)
        if not match:
            await message.answer("Afsuski videoni yuklab bo`lmadi 😞")
            return
        try:
            title, video = await asyncio.to_thread(_youtube, match.group(1))
            await message.answer_video(video, caption=f"{title}\n\n{_ABOUT}")
        except Exception:
            await message.answer("Afsuski videoni yuklab bo`lmadi 😞")

    elif url.startswith(("https://www.instagram.com/", "https://instagram.com/")):
        await bot.send_message(message.chat.id, "⏳", reply_markup=main_menu)
        try:
            media = await asyncio.to_thread(_instagram, url)
            await message.answer_document(media, caption=_ABOUT)
        except Exception:
            await message.answer("Afsuski video yoki rasmni yuklab bo`lmadi 😞")

    elif url.startswith("https://vt.tiktok.com/"):
        await bot.send_message(message.chat.id, "⏳", reply_markup=main_menu)
        try:
            media = await asyncio.to_thread(_tiktok, url)
            await message.answer_document(media, caption=_ABOUT)
        except Exception:
            await message.answer("Afsuski video yoki rasmni yuklab bo`lmadi 😞")

    else:
        await message.answer("Havola noto`g`ri. 📷 Instagram, 📹 YouTube yoki 🕹 TikTok havolasini yuboring.", reply_markup=main_menu)
