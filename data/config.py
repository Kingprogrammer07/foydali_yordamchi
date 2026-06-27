import os

from dotenv import load_dotenv

from data.post_data import db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")                              # Bot token (.env dan)
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN .env faylida topilmadi! .env.example dan nusxa oling.")

ADMINS: list = list(*zip(*db.admin_view()))                     # adminlar ro'yxati
CHANNELS: list = list(*zip(*db.channel_view()))              # kanallar ro'yxati
