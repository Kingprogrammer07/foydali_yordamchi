from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_url = InlineKeyboardMarkup(row_width = 2)
btn_url.insert(
    InlineKeyboardButton(text = "🆘 Bot Yaratuvchisi", url = "https://t.me/java_strong")
)
btn_url.add(
    InlineKeyboardButton(text = "📲 Telegram", url = "https://t.me/windowsuzprogrammaa"),
    InlineKeyboardButton(text = "📷 Instagram", url = "https://www.instagram.com/invites/contact/?i=m95peeh67d9u&utm_content=o9912bw"),
    InlineKeyboardButton(text = "🎥 Youtube", url = "http://youtube.com/channel/UCKhQtK94Fh5RrxOzlKr6asQ"),
)
