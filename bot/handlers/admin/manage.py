"""Admin menejer: admin/kanal qo'shish-o'chirish, foydalanuvchiga yozish."""
from aiogram import Bot, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.database.repositories import AdminRepo, ChannelRepo, UserRepo
from bot.filters.is_admin import IsAdmin
from bot.keyboards.callbacks import DeleteCB
from bot.keyboards.inline import delete_btn
from bot.keyboards.reply import admin_main, admin_manage, cancel_admin, main_menu
from bot.states import AdminManager

router = Router()
router.message.filter(F.chat.type == "private")

_CANCEL = "Orqaga🔝"


# ── Navigatsiya ───────────────────────────────────────────────────
@router.message(F.text == "👤Foydalanuvchi bo`limi👥", IsAdmin(), StateFilter(None))
async def to_user_section(message: Message):
    await message.answer(
        "Siz Foydalanuvchi bo`limidasiz!\n<b>Admin bo`limiga o`tish uchun /start buyrug`ini bering!</b>",
        reply_markup=main_menu,
    )


@router.message(F.text == "Admin menejer🎛", IsAdmin(), StateFilter(None))
async def manager_menu(message: Message):
    await message.answer("Bo`limni tanlang👇", reply_markup=admin_manage)


@router.message(F.text == "Admin asosiy", IsAdmin(), StateFilter(None))
async def admin_home(message: Message):
    await message.answer("Siz asosiy bo`limdasiz Admin", reply_markup=admin_main)


# ── Admin qo'shish ────────────────────────────────────────────────
@router.message(F.text == "Admin qo`shish➕", IsAdmin(), StateFilter(None))
async def add_admin_start(message: Message, state: FSMContext):
    await message.answer("Qo`shmoqchi bo`lgan foydalanuvchi 🆔 sini kiriting:", reply_markup=cancel_admin)
    await state.set_state(AdminManager.waiting_admin_id)


@router.message(AdminManager.waiting_admin_id, F.text)
async def add_admin_finish(message: Message, state: FSMContext, bot: Bot, admins: AdminRepo, users: UserRepo):
    text = message.text
    if text == _CANCEL:
        await state.clear()
        await message.answer("Jarayon tugadi.. Orqaga qaytdingiz.", reply_markup=admin_main)
        return
    if not text.isnumeric():
        await state.clear()
        await message.answer("ID raqamda harflar bo`lmaydi‼️", reply_markup=admin_manage)
        return
    txt = int(text)
    await state.clear()
    if await admins.exists(txt):
        await message.answer(f"{txt} ushbu id adminlar orasida mavjud!!", reply_markup=admin_manage)
    elif txt > 99999999 and await users.exists(txt):
        await admins.add(txt)
        try:
            await bot.send_message(txt, "Tabriklaymiz siz ushbu botga <b>Administrator</b> bo`ldingiz!🥳🥳", reply_markup=admin_main)
        except Exception:
            pass
        await message.answer("Admin qo`shish muvaffaqiyatli amalga oshdi✅", reply_markup=admin_manage)
    else:
        await message.answer("🆔 raqam xato kiritildi..! yoki bot foydalanuvchilari orasida topilmadi", reply_markup=admin_manage)


# ── Admin o'chirish ───────────────────────────────────────────────
@router.message(F.text == "Adminni olib tashlash➖", IsAdmin(), StateFilter(None))
async def list_admins(message: Message, admins: AdminRepo):
    rows = await admins.paged()
    if len(rows) <= 1:
        await message.answer(
            "‼️ <b>Kamida 1 kishi botga admin bo`lishi kerak\nSiz admin o`chirolmaysiz</b> ‼️",
            reply_markup=admin_manage,
        )
        return
    text = ""
    ids = []
    for rid, admin_id in rows:
        text += (
            f"\n<b>{rid}</b>. 🆔 raqami: <pre><b>{admin_id}</b></pre>\n"
            f"Profili: <a href='tg://user?id={admin_id}'>Ko`rish uchun bosing!</a>\n"
            "➖➖➖➖➖➖➖➖➖➖➖\n"
        )
        ids.append(rid)
    await message.answer("Adminlikdan bo`shatadigan odamning\n<b> - ustiga bosing:</b>")
    await message.answer(text, reply_markup=delete_btn(ids, "admin"))


# ── Kanal qo'shish ────────────────────────────────────────────────
@router.message(F.text == "Kanal qo`shish➕", IsAdmin(), StateFilter(None))
async def add_channel_start(message: Message, state: FSMContext):
    await message.answer(
        "Qo`shmoqchi bo`lgan <b>Kanalingizni</b> 🆔 sini (Kanallarning ID raqami (-)manfiy bo`ladi) kiriting:",
        reply_markup=cancel_admin,
    )
    await message.answer("‼️  <b>Avval Botni kanalga qo`shib admin qiling</b>  ‼️")
    await state.set_state(AdminManager.waiting_channel_id)


@router.message(AdminManager.waiting_channel_id, F.text)
async def add_channel_finish(message: Message, state: FSMContext, channels: ChannelRepo):
    text = message.text
    await state.clear()
    if text == _CANCEL:
        await message.answer("Jarayon yakunlandi..! Orqaga qaytdingiz.", reply_markup=admin_manage)
        return
    if text.startswith("-") and text[1:].isdigit() and int(text) < -99999999999:
        try:
            await channels.add(int(text))
            await message.answer("Kanal ➕qo`shish <b>muvaffaqiyatli amalga oshdi</b>✅", reply_markup=admin_manage)
        except Exception:
            await message.answer("<b>Kanalga botni qo`shib admin qiling!!</b>", reply_markup=admin_manage)
    else:
        await message.answer(
            "ID raqam manfiy va faqat raqamlardan iborat bo`lishi kerak‼️ (masalan: -1001234567890)",
            reply_markup=admin_manage,
        )


# ── Kanal o'chirish ───────────────────────────────────────────────
@router.message(F.text == "Kanalni olib tashlash➖", IsAdmin(), StateFilter(None))
async def list_channels(message: Message, bot: Bot, channels: ChannelRepo):
    rows = await channels.paged()
    if len(rows) <= 1:
        await message.answer(
            "‼️ <b>Kamida 1 ta kanal botga ulangan bo`lishi kerak\nSiz kanal o`chirolmaysiz</b> ‼️",
            reply_markup=admin_manage,
        )
        return
    text = ""
    ids = []
    for rid, ch in rows:
        try:
            chat = await bot.get_chat(ch)
            link = await bot.export_chat_invite_link(ch)
            title = chat.title
        except Exception:
            title, link = str(ch), "https://t.me"
        text += f"\n{rid} - <b><a href='{link}'>{title}</a></b>\n➖➖➖➖➖➖➖➖"
        ids.append(rid)
    await message.answer("Qaysi kanalni olib tashlamoqchi bo`lsangiz o`shani\n<b>ustiga bosing:</b>")
    await message.answer(text, reply_markup=delete_btn(ids, "kanal"))


# ── O'chirish callback ────────────────────────────────────────────
@router.callback_query(DeleteCB.filter())
async def delete_entry(call: CallbackQuery, callback_data: DeleteCB, bot: Bot, admins: AdminRepo, channels: ChannelRepo):
    row_id = callback_data.id
    if callback_data.kind == "kanal":
        ch = await channels.get(row_id)
        try:
            title = (await bot.get_chat(ch)).title
        except Exception:
            title = str(ch)
        await channels.delete(row_id)
        await call.answer(f"{title} -- shu kanal botdan olib tashlandi!", show_alert=True)
        await call.message.delete()
    else:  # admin
        if row_id == 1:
            await call.answer("Siz Bot yaratuvchisini o`chirib tashlayolmaysiz! 😡", show_alert=True)
            await call.message.delete()
            return
        admin_id = await admins.get(row_id)
        await admins.delete(row_id)
        await call.answer(f"{admin_id} -- shu raqamli admin lavozimidan olib tashlandi!", show_alert=True)
        try:
            await bot.send_message(admin_id, "Siz <b>Administrator</b> lavozimidan bo`shatildingiz😒", reply_markup=main_menu)
        except Exception:
            pass
        await call.message.delete()


# ── Foydalanuvchilarga yozish ─────────────────────────────────────
@router.message(F.text == "Foydalanuvchilarga yozish", IsAdmin(), StateFilter(None))
async def write_user_start(message: Message, state: FSMContext):
    await message.answer(
        "Botning Foydalanuvchilariga yozish uchun <b>ularning 🆔 raqamini kiriting:</b>",
        reply_markup=cancel_admin,
    )
    await state.set_state(AdminManager.waiting_user_id)


@router.message(AdminManager.waiting_user_id, F.text)
async def write_user_id(message: Message, state: FSMContext, users: UserRepo):
    text = message.text
    if text == _CANCEL:
        await state.clear()
        await message.answer("Jarayon yakunlandi..! Orqaga aytdingiz.", reply_markup=admin_main)
        return
    if text.isdigit() and await users.exists(int(text)):
        await state.update_data(target_id=int(text))
        await message.answer(
            "🆔 raqam saqlandi ✅\nEndi 📝 <b>Yozmoqchi bo`lgan textni kiriting:</b>",
            reply_markup=cancel_admin,
        )
        await state.set_state(AdminManager.waiting_user_message)
    else:
        await state.clear()
        await message.answer(f"<b>** {text} ** siz bazada yo`q odamni kiritdingiz</b> ‼️", reply_markup=admin_main)


@router.message(AdminManager.waiting_user_message, F.text)
async def write_user_message(message: Message, state: FSMContext, bot: Bot):
    if message.text == _CANCEL:
        await state.clear()
        await message.answer("Jarayon yakunlandi..! Orqaga qaytdingiz.", reply_markup=admin_main)
        return
    data = await state.get_data()
    target = data.get("target_id")
    await state.clear()
    try:
        await bot.send_message(target, f"Sizga 👤admindan xabar keldi:\n\n{message.html_text}", reply_markup=main_menu)
        await message.answer(
            f"<a href='tg://user?id={target}'>Foydalanuvchiga</a> muvaffaqiyatli yuborildi✅",
            reply_markup=admin_main,
        )
    except Exception:
        await message.answer(
            "Siz yuborgan xabar foydalanuvchiga yetib bormadi..\n<b>Sababi u botni bloklagan</b>",
            reply_markup=admin_main,
        )
