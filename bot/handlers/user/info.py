"""Ma'lumot bo'limi: /help, qo'llanma, /admin, statistika, ID orqali topish."""
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.database.repositories import UserRepo
from bot.keyboards.callbacks import BotPostCB
from bot.keyboards.inline import admin_contact, btn_url, ishlatish
from bot.keyboards.reply import cancel_admin, main_menu
from bot.states import AdminManager

router = Router()

_QOLLANMA = (
    "Bot xizmatlari:\n"
    "1️⃣ --> Maktab darsliklarini yuklab olishingiz mumkin😉\n"
    "2️⃣--> Booknomy kitoblarni 3xil tilda yuklab olishingiz mumkin😱\n"
    "3️⃣--> Qiyin bo`lmasa Bot haqidagi fikringizni ham qoldiring!!\n"
    "4️⃣--> Botdagi yangi kompyuterlar Bo`limi: bunda siz kompyuterga kerak bolgan kop dasturlarni yuklab olishingiz mumkin\n\n"
    "🖥Bizning kompyuter dasturlari kanalimizga va instagram, Youtube kanallarimizga obuna bo`ling!\n"
)


@router.message(Command("help"), StateFilter(None), F.chat.type == "private")
async def bot_help(message: Message):
    await message.answer(
        "⚙️<b>Botning ishlashi\n🆘Menyudan foydalaning\n🎛Pastdagi tugmalardan foydalaning\n"
        "Tushunmasangiz yoki savollar bo`lsa adminga murojaat qiling!\n💻Admin: @java_strong</b>\n"
        "Boshidan ishlatish /start",
        reply_markup=btn_url,
    )


@router.message(F.text == "Qo`llanma📃", StateFilter(None), F.chat.type == "private")
@router.message(Command("qollanma"), StateFilter(None), F.chat.type == "private")
async def qollanma(message: Message):
    await message.answer(_QOLLANMA, reply_markup=btn_url)


@router.message(Command("admin"), StateFilter(None), F.chat.type == "private")
async def admin_contact_cmd(message: Message):
    await message.answer(
        "<b>Adminga murojaat qilish uchun ushbu havola ustiga bosing</b>✅",
        reply_markup=admin_contact,
    )


@router.message(Command("search_about"), StateFilter(None), F.chat.type == "private")
async def search_about(message: Message):
    await message.answer_document(
        "https://t.me/windowsuzprogrammaa/425",
        caption=(
            "** Videoda batafsil ^\n<b>Teleram foydalanuvchilarini Username bo`lmasa va Telefon raqamini "
            "bilmasangiz yoki Topmoqchi bolgan foydalanuvchi sizni qora ro`yhatga(Blokka) kirgizgan bo`lsa ham "
            "topib beruvchi bot..</b>(Topish topmasligi Telegram turiga bog`liq!)\n\n"
            "Agar ID raqamni qayerda olishni bilmasangiz ~ @ShowJsonBot ~ orqali olishingiz mumkin"
        ),
        reply_markup=ishlatish,
    )


@router.message(F.text == "Statistika📶", StateFilter(None), F.chat.type == "private")
async def statistika(message: Message, users: UserRepo):
    count = await users.count()
    await message.answer(f"👁‍🗨<b>Hozirda botning {count} ta foydalanuvchisi bor</b>")


# ── ID orqali topish (foydalanuvchi funksiyasi) ───────────────────
@router.message(F.text.in_({"🆔 orqali topish", "/id_orqali_topish"}), StateFilter(None), F.chat.type == "private")
async def id_search_intro(message: Message):
    await message.answer(
        "✅ Telegram Foydalanuvchilarini 🆔 raqami orqali topish🔎\n📝 To`liq ma`lumot uchun: <b>/search_about</b>",
        reply_markup=ishlatish,
    )


@router.callback_query(BotPostCB.filter(F.action == "ishla"))
async def id_search_start(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer("ID topish ilovasi ishlashni boshladi!")
    await call.message.answer(
        "<b>Topmoqchi bo`lgan telegram foydalanuvchisining [Telegram ID] raqamini kiriting:</b>",
        reply_markup=cancel_admin,
    )
    await state.set_state(AdminManager.waiting_find_id)


@router.message(AdminManager.waiting_find_id, F.text)
async def id_search_result(message: Message, state: FSMContext):
    text = message.text
    if text == "Orqaga🔝":
        await message.answer("Bekor qilindi!", reply_markup=main_menu)
        await state.clear()
        return
    if text.isnumeric() and int(text) > 99999999:
        await message.answer(
            f"<a href='tg://user?id={int(text)}'>Foydalanuvchi</a> 👈🏻<b>Ko`rish uchun ustiga bosing!</b>\n\n/id_orqali_topish",
            reply_markup=main_menu,
        )
    else:
        await message.answer(
            f"<b>{text}</b> -- Ushbu ID raqamiga tegishli Telegram Foydalanuvchisi topilmadi\n"
            "‼️<b>ID raqam xato bo`lishi mumkin</b>‼️\n\n/id_orqali_topish",
            reply_markup=main_menu,
        )
    await state.clear()
