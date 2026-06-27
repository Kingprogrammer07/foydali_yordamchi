"""Reply (pastki) klaviaturalar. Tugma matnlari catalog/handler kalitlariga MOS bo'lishi shart."""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def _kb(rows: list[list[str]]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t) for t in row] for row in rows],
        resize_keyboard=True,
    )


# ── Asosiy menyular ───────────────────────────────────────────────
admin_main = _kb([
    ["👤Foydalanuvchi bo`limi👥", "📎Yangi post✏️"],
    ["Admin menejer🎛"],
    ["Statistika📶", "Foydalanuvchilarga yozish"],
])

main_menu = _kb([
    ["📚Maktab darsliklari📚", "🎧Booknomy kitoblar🎧"],
    ["Kompyuter Dasturlari🖥🛠", "🆔 orqali topish"],
    ["📹 Video yuklash"],
    ["Qo`llanma📃", "Statistika📶", "Taklif"],
])

# ── Maktab darsliklari ────────────────────────────────────────────
school_main = _kb([
    ["PDF ochadigan dastur(apk) va (exe)🎛"],
    ["📚11-Sinf darsliklar📚", "📚10-Sinf yangi darsliklar📚"],
    ["📚9-Sinf darsliklar📚", "📚8-Sinf darsliklar📚"],
    ["📚7-Sinf yangi darsliklar📚", "Asosiy Bo`lim⬅️"],
])

sinf11 = _kb([
    ["PDF ochadigan dastur(apk) va (exe)🎛"],
    ["11-Sinf Matematika 1-qism📘", "11-Sinf Adabiyot 1-qism📘"],
    ["11-Sinf Adabiyot 2-qism📘", "11-Sinf Kimyo📘"],
    ["11-Sinf Rus tili📘", "Hamma 11-sinf kitobni yuklash📚"],
    ["🔙Orqaga⬅️", "Asosiy Bo`lim⬅️"],
])

sinf10 = _kb([
    ["PDF ochadigan dastur(apk) va (exe)🎛"],
    ["10-Sinf Ona tili📘", "10-Sinf Biologiya📘"],
    ["10-Sinf Kimyo📘", "10-Sinf Informatika📘"],
    ["10-Sinf Ingliz Tili📘", "10-Sinf Fizika📘"],
    ["10-Sinf Geometriya📘", "10-Sinf Algebra📘"],
    ["10-Sinf Geografiya📘", "10-Sinf Kimyo Nazorat ishi📖"],
    ["🔙Orqaga⬅️", "Asosiy Bo`lim⬅️"],
])

sinf9 = _kb([
    ["PDF ochadigan dastur(apk) va (exe)🎛"],
    ["9-Sinf Informatika📘", "9-Sinf Tarbiya📘"],
    ["9-Sinf Fizika📘", "9-Sinf Geometriya📘"],
    ["9-Sinf Algebra📘", "9-Sinf Geografiya📘"],
    ["9-Sinf Rus tili📘"],
    ["Hamma 9-sinf kitobni yuklash📚"],
    ["🔙Orqaga⬅️", "Asosiy Bo`lim⬅️"],
])

sinf8 = _kb([
    ["PDF ochadigan dastur(apk) va (exe)🎛"],
    ["8-Sinf Ona tili📘", "8-Sinf Rus tili📘"],
    ["8-Sinf Informatika📘", "8-Sinf Tarbiya📘"],
    ["8-Sinf Geometriya📘", "8-Sinf Algebra📘"],
    ["8-Sinf Geografiya📘"],
    ["Hamma 8-sinf kitobni yuklash📚"],
    ["🔙Orqaga⬅️", "Asosiy Bo`lim⬅️"],
])

sinf7 = _kb([
    ["PDF ochadigan dastur(apk) va (exe)🎛"],
    ["7-Sinf Ona tili📘", "7-Sinf Biologiya📘"],
    ["7-Sinf Kimyo📘", "7-Sinf Informatika📘"],
    ["7-Sinf Ingliz Tili📘", "7-Sinf Fizika📘"],
    ["7-Sinf Geometriya📘", "7-Sinf Algebra📘"],
    ["7-Sinf Geografiya📘", "7-Sinf Musiqa📘"],
    ["7-Sinf Tasviriy san`at📘", "7-Sinf Rus tili📘"],
    ["Hamma 7-sinf kitobni yuklash📚"],
    ["🔙Orqaga⬅️", "Asosiy Bo`lim⬅️"],
])

# ── Booknomy ──────────────────────────────────────────────────────
booknomy = _kb([
    ["🏴󠁧󠁢󠁥󠁮󠁧󠁿Ingliz tili📕🎧", "🇷🇺Rus tili📘🎧"],
    ["🇰🇷Koreys tili📗🎧", "Asosiy Bo`lim⬅️"],
])

# ── Kompyuter dasturlari ──────────────────────────────────────────
pc = _kb([
    ["🔐 Windows 10 hack password", "Windows sistemalar✳️"],
    ["Office dasturlar", "Grafik dasturlar🎛"],
    ["Video montaj dasturlar🎥", "Aktivator⚡️"],
    ["Arxiv dasturlar📚", "Converter dasturi🔄"],
    ["Windowslarni yozish📀📼"],
    ["Asosiy bo`lim💡"],
])

grafik_dasturlar = _kb([
    ["Adobe Photoshop", "Blender dasturi"],
    ["3Ds Max", "Corel Draw"],
    ["Adobe Photoshop Lightroom", "Unity Pro"],
    ["Asosiy bo`lim💡"],
])

video_montaj = _kb([
    ["Adobe Premiere Pro", "Adobe after effects"],
    ["Edius 8.53", "Proshow Producer Pro"],
    ["Asosiy bo`lim💡"],
])

office = _kb([
    ["Office 2013", "Office 2019"],
    ["Office 2016", "Office 2021"],
    ["WPS office", "Office activator"],
    ["Asosiy bo`lim💡"],
])

windows_turlari = _kb([
    ["Orginal Windowslar🤖", "LiteOs Windowslar🤖"],
    ["Game Windows🎮"],
    ["Asosiy bo`lim💡"],
])

windows_orginal = _kb([
    ["Windows 11", "Windows 10"],
    ["Windows 8.1", "Windows 7"],
    ["Orqaga🔧", "Asosiy bo`lim💡"],
])

windows_liteos = _kb([
    ["Windows 11 LiteOs", "Windows 10 LiteOs"],
    ["Windows 8.1 LiteOs", "Windows 7 LiteOs"],
    ["Orqaga🔧", "Asosiy bo`lim💡"],
])

# ── Admin menejer ─────────────────────────────────────────────────
admin_manage = _kb([
    ["Admin qo`shish➕", "Adminni olib tashlash➖"],
    ["Kanal qo`shish➕", "Kanalni olib tashlash➖"],
    ["Admin asosiy"],
])

# ── Yordamchi (bekor / orqaga) ────────────────────────────────────
cancel_admin = _kb([["Orqaga🔝"]])      # admin FSM bekor
back_post = _kb([["Orqaga 🔙"]])        # post yasash FSM bekor
