"""FSM holatlari."""
from aiogram.fsm.state import State, StatesGroup


class AdminManager(StatesGroup):
    waiting_admin_id = State()       # admin qo'shish uchun ID
    waiting_channel_id = State()     # kanal qo'shish uchun ID
    waiting_user_id = State()        # foydalanuvchiga yozish — ID
    waiting_user_message = State()   # foydalanuvchiga yozish — matn
    waiting_find_id = State()        # ID orqali topish


class NewPost(StatesGroup):
    waiting_post = State()           # post/e'lon kontenti (bitta xabar)
    confirm = State()                # foydalanuvchi taklifini tasdiqlash
    waiting_btn_text = State()       # inline tugma yozuvi
    waiting_btn_url = State()        # inline tugma url


class VideoDownload(StatesGroup):
    waiting_url = State()            # yuklab olinadigan havola
