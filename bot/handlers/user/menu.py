"""Menyu navigatsiyasi (bo'limlar) + echo fallback (eng oxirgi router)."""
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from bot.keyboards import reply

router = Router()

_WIN_WARN = (
    "Windows turini Tanlang!👇\n"
    "‼️Windowslarni Rufus(Fleshkaga) yoki UltraIso(fleshka yoki diskka) dasturi orqali yoziladi‼️\n"
    "Rufus va UltraIso asosiy menuda Windows yozish bo`limida!"
)

# text -> (javob matni, klaviatura)
NAV: dict[str, tuple[str, object]] = {
    "📚Maktab darsliklari📚": ("Siz maktab darsliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply.school_main),
    "🔙Orqaga⬅️": ("Siz maktab darsliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply.school_main),
    "📚11-Sinf darsliklar📚": ("11-sinf dasrliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply.sinf11),
    "📚10-Sinf yangi darsliklar📚": ("10-sinf darsliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply.sinf10),
    "📚9-Sinf darsliklar📚": ("9-sinf darsliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply.sinf9),
    "📚8-Sinf darsliklar📚": ("8-sinf darsliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply.sinf8),
    "📚7-Sinf yangi darsliklar📚": ("7-sinf bo`limidasiz ➡️ Menuni Tanlang!👇", reply.sinf7),
    "Asosiy Bo`lim⬅️": ("Siz asosiy bo`limdasiz! Menyuni tanlang👇", reply.main_menu),
    "🎧Booknomy kitoblar🎧": ("Siz <b>Booknomy</b> bo`limidasiz tilni tanlang!👇", reply.booknomy),
    "Grafik dasturlar🎛": ("Siz grafik dasturlar bo`limidasiz!", reply.grafik_dasturlar),
    "Office dasturlar": ("Office dasturlardan Tanlang!👇", reply.office),
    "Video montaj dasturlar🎥": ("Video montaj dasturlarini Tanlang!👇", reply.video_montaj),
    "Asosiy bo`lim💡": ("Siz asosiy menudasiz!👇\nMaktab bo`limiga o`tish uchun /start bering!", reply.pc),
    "Windows sistemalar✳️": (_WIN_WARN, reply.windows_turlari),
    "Orqaga🔧": (_WIN_WARN, reply.windows_turlari),
    "Orginal Windowslar🤖": ("Orginal Windowslarni Tanlang!👇\n" + _WIN_WARN, reply.windows_orginal),
    "LiteOs Windowslar🤖": ("Yengil ishlaydigan lite os windowslarni Tanlang!👇\n" + _WIN_WARN, reply.windows_liteos),
}


@router.message(F.text.in_(set(NAV)), StateFilter(None), F.chat.type == "private")
async def navigate(message: Message):
    text, keyboard = NAV[message.text]
    await message.answer(text, reply_markup=keyboard)


@router.message(F.text.in_({"Kompyuter Dasturlari🖥🛠", "/pc_mexanics"}), StateFilter(None), F.chat.type == "private")
async def pc_section(message: Message):
    await message.answer("Siz asosiy menudasiz!👇", reply_markup=reply.pc)


# ── Echo — hech bir handler ushlamagan matn (ENG OXIRGI) ──────────
@router.message(StateFilter(None), F.chat.type == "private", F.text)
async def echo(message: Message):
    await message.reply(
        f"<b>Botda ** {message.text} ** buyrug`i topilmadi!</b>\n"
        "⚙️Berilgan parametrlardan birini tanlang!\n🎛Menyudan foydalaning yoki /help 🆘tugmasini bosing!"
    )
