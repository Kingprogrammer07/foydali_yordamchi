"""Konfiguratsiya — barcha sozlamalar .env faylidan o'qiladi."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN .env faylida topilmadi! .env.example dan nusxa oling.")

# RapidAPI (video yuklash)
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_INSTAGRAM_HOST = os.getenv("RAPIDAPI_INSTAGRAM_HOST")
RAPIDAPI_TIKTOK_HOST = os.getenv("RAPIDAPI_TIKTOK_HOST")
RAPIDAPI_YOUTUBE_HOST = os.getenv("RAPIDAPI_YOUTUBE_HOST")

# data/database.sqlite3 — loyiha ildizidagi mavjud DB fayl
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "database.sqlite3"

# Throttling: bir foydalanuvchidan minimal so'rov oralig'i (sekund).
# Past qiymat — FSM oqimida tez yozilgan xabar tushib qolmasligi uchun.
THROTTLE_RATE = 0.3
