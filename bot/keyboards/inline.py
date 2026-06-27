"""Inline klaviaturalar."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.callbacks import AdminPostCB, BotPostCB, ChannelCB, DeleteCB, PostCB, TaklifCB


# ── Majburiy obuna ────────────────────────────────────────────────
def subscription_keyboard(invite_links: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for link in invite_links:
        builder.button(text="Obuna bo'lish", url=link)
    builder.button(text="Obunani tekshirish ✅", callback_data="check_subs")
    builder.adjust(1)
    return builder.as_markup()


# ── Post tasdiqlash ───────────────────────────────────────────────
confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="🆗 Chop etish", callback_data=PostCB(action="post").pack()),
    InlineKeyboardButton(text="❌ Rad etish", callback_data=PostCB(action="cancel").pack()),
]])

# ── Foydalanuvchi taklifi ─────────────────────────────────────────
taklif = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="🆕 Fikr yoki Yangi post", callback_data=TaklifCB(action="new_post").pack()),
]])

# ── Admin: post manzili ───────────────────────────────────────────
one_chanel = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="📢 Kanalda", callback_data=AdminPostCB(action="first_chanel").pack()),
    InlineKeyboardButton(text="🤖 Bot ichida", callback_data=AdminPostCB(action="in_bot").pack()),
]])

all_chanel = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="📢 1 ta kanalda", callback_data=AdminPostCB(action="one_chanel").pack()),
    InlineKeyboardButton(text="🤖 Bot ichida", callback_data=AdminPostCB(action="in_bot").pack()),
    InlineKeyboardButton(text="📢 Hamma Kanallarda", callback_data=AdminPostCB(action="all_chanel").pack()),
]])

save_pst = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="🆗 Chop etish", callback_data=AdminPostCB(action="first_oddiy").pack()),
    InlineKeyboardButton(text="🆗 Tugmacha bilan", callback_data=AdminPostCB(action="first_url").pack()),
]])

save_pst_url = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="🆕 Yangi Tugma", callback_data=AdminPostCB(action="first_new_btn").pack()),
    InlineKeyboardButton(text="↪️ Orqaga", callback_data=AdminPostCB(action="first_back").pack()),
]])

# ── ID orqali topish ──────────────────────────────────────────────
ishlatish = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Ishlatish", callback_data=BotPostCB(action="ishla").pack()),
]])

# ── Statik havolalar ──────────────────────────────────────────────
btn_url = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🆘 Bot Yaratuvchisi", url="https://t.me/java_strong")],
    [
        InlineKeyboardButton(text="📲 Telegram", url="https://t.me/windowsuzprogrammaa"),
        InlineKeyboardButton(text="📷 Instagram", url="https://www.instagram.com/invites/contact/?i=m95peeh67d9u&utm_content=o9912bw"),
        InlineKeyboardButton(text="🎥 Youtube", url="http://youtube.com/channel/UCKhQtK94Fh5RrxOzlKr6asQ"),
    ],
])

admin_contact = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="👨‍💻Admin👨‍💻", url="https://t.me/java_strong"),
]])


# ── Dinamik builder'lar ───────────────────────────────────────────
def btn_create(lugat: dict[str, str]) -> InlineKeyboardMarkup:
    """Post uchun foydalanuvchi qo'shgan havola tugmalari."""
    n = len(lugat)
    width = 2 if n <= 3 else (4 if n < 5 else 5)
    builder = InlineKeyboardBuilder()
    for text, url in lugat.items():
        builder.button(text=text, url=url)
    builder.adjust(width)
    return builder.as_markup()


def num_btn(num_list: list[int]) -> InlineKeyboardMarkup:
    """Kanal raqamlari + sahifalash (post bermoqchi bo'lgan kanalni tanlash)."""
    builder = InlineKeyboardBuilder()
    for i in num_list:
        builder.button(text=str(i), callback_data=ChannelCB(action="number", id=i))
    builder.adjust(4)
    if len(num_list) > 8:
        nav = InlineKeyboardBuilder()
        nav.button(text="↩️", callback_data=ChannelCB(action="orqaga", id=num_list[0]))
        nav.button(text="❌", callback_data=ChannelCB(action="delete", id=0))
        nav.button(text="↪️", callback_data=ChannelCB(action="oldinga", id=num_list[-1]))
        builder.attach(nav)
    return builder.as_markup()


def delete_btn(num_list: list[int], kind: str) -> InlineKeyboardMarkup:
    """Admin/kanal o'chirish raqamlari + sahifalash. kind: 'admin' | 'kanal'."""
    builder = InlineKeyboardBuilder()
    for i in num_list:
        builder.button(text=str(i), callback_data=DeleteCB(action="number", id=i, kind=kind))
    builder.adjust(4)
    if len(num_list) > 8:
        nav = InlineKeyboardBuilder()
        nav.button(text="↩️", callback_data=ChannelCB(action="orqaga", id=num_list[0]))
        nav.button(text="❌", callback_data=ChannelCB(action="delete", id=0))
        nav.button(text="↪️", callback_data=ChannelCB(action="oldinga", id=num_list[-1]))
        builder.attach(nav)
    return builder.as_markup()
