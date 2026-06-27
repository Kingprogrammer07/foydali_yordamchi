"""Post yaratish va tarqatish (eski newpost.py).

Refactor:
- global dict'lar o'rniga FSM (per-user, concurrency xavfsiz)
- entity ast.literal_eval hack o'rniga `copy_message` (formatlash to'liq saqlanadi)
- 4x photo/document/video/text takror branch -> bitta copy_message
- post BITTA xabar bo'lib yuboriladi (media + caption birga)
"""
import asyncio

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest, TelegramRetryAfter
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)

from bot.database.repositories import AdminRepo, ChannelRepo, UserRepo
from bot.filters.is_admin import IsAdmin
from bot.keyboards.callbacks import AdminPostCB, ChannelCB, PostCB, TaklifCB
from bot.keyboards.inline import (
    all_chanel,
    btn_create,
    confirmation_keyboard,
    num_btn,
    one_chanel,
    save_pst,
    save_pst_url,
    taklif,
)
from bot.keyboards.reply import admin_main, back_post, main_menu
from bot.states import NewPost

router = Router()

_POST_PROMPT = (
    "Yangi postni yoki E`loningizni kanalga tashlash uchun <b>Qulaylik uchun Tayyor post tashlang</b>❕ "
    "yoki rasmdan boshlab post yasang:"
)


# ── Yordamchilar ──────────────────────────────────────────────────
async def _targets(data: dict, channels: ChannelRepo, users: UserRepo) -> list[int]:
    """Post qaysi chat(lar)ga yuboriladi."""
    sort = data.get("sort")
    if sort == "in_bot":
        return await users.all_ids()
    if sort == "all_chanel":
        return await channels.all_ids()
    if data.get("channel_id"):
        return [data["channel_id"]]
    ids = await channels.all_ids()
    return ids[:1]


_RATE = 0.05  # sekund — ketma-ket yuborishlar orasidagi pauza (~20/s, flood limitidan past)
_MEDIA = {"photo": InputMediaPhoto, "video": InputMediaVideo, "document": InputMediaDocument, "audio": InputMediaAudio}


async def _safe(factory) -> None:
    """Bitta yuborishni xavfsiz bajaradi: RetryAfter -> kutib qayta urinadi, blok/xato -> o'tkazib yuboradi."""
    try:
        return await factory()
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        try:
            return await factory()
        except Exception:
            return None
    except (TelegramForbiddenError, TelegramBadRequest):
        return None  # foydalanuvchi botni bloklagan yoki chat yaroqsiz
    except Exception:
        return None


def _build_media(items: list[dict]) -> list:
    return [_MEDIA[it["type"]](media=it["file_id"]) for it in items]


async def _send_album_buttons(bot: Bot, chat_id: int, items: list[dict], caption: str | None, markup) -> None:
    # Albom captionsiz yuboriladi, keyin caption+tugmalar ALOHIDA xabar bo'lib albomga reply qilinadi.
    sent = await bot.send_media_group(chat_id, media=_build_media(items))
    await bot.send_message(chat_id, caption or "👇", reply_markup=markup, reply_to_message_id=sent[0].message_id)


async def _publish(bot: Bot, data: dict, targets: list[int], buttons: dict | None = None) -> None:
    album_items = data.get("album_items")
    ids = data.get("src_message_ids")
    markup = btn_create(buttons) if buttons else None
    caption = data.get("album_caption")
    multi = len(targets) > 1
    for chat_id in targets:
        if album_items and buttons:        # albom + tugma -> media_group + alohida reply xabar
            await _safe(lambda c=chat_id: _send_album_buttons(bot, c, album_items, caption, markup))
        elif ids:                          # albom (tugmasiz) -> copy_messages (caption albomda qoladi)
            await _safe(lambda c=chat_id: bot.copy_messages(c, data["src_chat_id"], ids))
        else:                              # bitta post
            await _safe(lambda c=chat_id: bot.copy_message(c, data["src_chat_id"], data["src_message_id"], reply_markup=markup))
        if multi:
            await asyncio.sleep(_RATE)


def _parse_url(text: str) -> str | None:
    if text.isdigit():
        return f"tg://user?id={int(text)}" if int(text) > 99999999 else None
    if text.startswith("@"):
        return f"https://t.me/{text[1:]}"
    if "/" in text:
        return text
    if text.endswith((".com", ".uz", ".ru")):
        return f"https://{text}"
    return None


async def _build_channel_list(bot: Bot, rows: list[tuple]) -> tuple[str, list[int]]:
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
    return text, ids


# ── Admin: Yangi post ─────────────────────────────────────────────
@router.message(F.text == "📎Yangi post✏️", IsAdmin(), StateFilter(None), F.chat.type == "private")
async def new_post_start(message: Message, state: FSMContext, channels: ChannelRepo):
    await state.clear()
    kb = one_chanel if await channels.count() < 2 else all_chanel
    await message.reply("Reklamani qayerga bermoqchisiz.❓", reply_markup=kb)


@router.message(Command("yangi_post"), IsAdmin(), StateFilter(None), F.chat.type == "private")
async def yangi_post_cmd(message: Message, state: FSMContext):
    await state.update_data(sort="first_chanel", channel_id=None)
    await message.answer("Chop etish uchun post yuboring.", reply_markup=back_post)
    await state.set_state(NewPost.waiting_post)


@router.callback_query(AdminPostCB.filter(F.action == "first_chanel"), IsAdmin())
async def cb_first_chanel(call: CallbackQuery, state: FSMContext):
    await call.answer("Kanalda post")
    await state.update_data(sort="first_chanel", channel_id=None)
    await call.message.answer(_POST_PROMPT, reply_markup=back_post)
    await state.set_state(NewPost.waiting_post)
    await call.message.delete()


@router.callback_query(AdminPostCB.filter(F.action == "in_bot"), IsAdmin())
async def cb_in_bot(call: CallbackQuery, state: FSMContext):
    await call.answer("Bot ichida post yuborish")
    await state.update_data(sort="in_bot", channel_id=None)
    await call.message.answer(
        "Yangi postni yoki E`loningizni botga tashlash uchun <b>Qulaylik uchun Tayyor post tashlang</b>❕ "
        "yoki rasmdan boshlab post yasang:",
        reply_markup=back_post,
    )
    await state.set_state(NewPost.waiting_post)
    await call.message.delete()


@router.callback_query(AdminPostCB.filter(F.action == "all_chanel"), IsAdmin())
async def cb_all_chanel(call: CallbackQuery, state: FSMContext):
    await call.answer("Hamma kanallarda post")
    await state.update_data(sort="all_chanel", channel_id=None)
    await call.message.answer(_POST_PROMPT, reply_markup=back_post)
    await state.set_state(NewPost.waiting_post)
    await call.message.delete()


@router.callback_query(AdminPostCB.filter(F.action == "one_chanel"), IsAdmin())
async def cb_one_chanel(call: CallbackQuery, bot: Bot, channels: ChannelRepo):
    await call.answer()
    await call.message.answer("Qaysi kanalga <b>Reklama</b> bermoqchisiz❓")
    text, ids = await _build_channel_list(bot, await channels.paged())
    await call.message.answer(text, reply_markup=num_btn(ids))
    await call.message.delete()


# ── Foydalanuvchi: Taklif ─────────────────────────────────────────
@router.message(F.text == "Taklif", StateFilter(None), F.chat.type == "private")
@router.message(Command("yangi_post_taklif"), StateFilter(None), F.chat.type == "private")
async def taklif_start(message: Message):
    await message.reply(
        "Siz adminga 🧾<b>reklama post yoki fikringizni</b> bildirmoqchimisiz❓",
        reply_markup=taklif,
    )


@router.callback_query(TaklifCB.filter(F.action == "new_post"))
async def taklif_new_post(call: CallbackQuery, state: FSMContext):
    await call.answer("Fikr yoki yangi post tanlandi")
    await call.message.delete()
    await call.message.answer(
        "Agar siz adminga 🧾reklama taklif qilmoqchi bo`lsangiz <b>Qulaylik uchun Tayyor post tashlang❕</b> "
        "yoki rasmdan boshlab post yasang\nyoki Bot haqida fikringizni ayting:",
        reply_markup=back_post,
    )
    await state.update_data(sort=None)
    await state.set_state(NewPost.waiting_post)


# ── Post kontenti qabul qilish ────────────────────────────────────
@router.message(NewPost.waiting_post)
async def post_received(message: Message, state: FSMContext, bot: Bot, admins: AdminRepo, album: list[Message] | None = None):
    if message.text == "Orqaga 🔙":
        await state.clear()
        is_adm = await admins.exists(message.from_user.id)
        await message.answer("Bekor qilindi.", reply_markup=admin_main if is_adm else main_menu)
        return

    data = await state.get_data()
    is_admin_flow = data.get("sort") is not None

    ids = None
    album_items = None
    album_caption = None
    if album:
        ids = [m.message_id for m in album]
        album_items = []
        for m in album:
            if m.photo:
                album_items.append({"type": "photo", "file_id": m.photo[-1].file_id})
            elif m.video:
                album_items.append({"type": "video", "file_id": m.video.file_id})
            elif m.document:
                album_items.append({"type": "document", "file_id": m.document.file_id})
            elif m.audio:
                album_items.append({"type": "audio", "file_id": m.audio.file_id})
            if album_caption is None and m.caption:
                album_caption = m.caption_html
    await state.update_data(
        src_chat_id=message.chat.id,
        src_message_id=message.message_id,
        src_message_ids=ids,
        album_items=album_items,
        album_caption=album_caption,
        buttons={},  # yangi post uchun tugmalarni tozalash
    )

    if is_admin_flow:  # admin chop etish oqimi
        if album:  # albom — oldin nusxa (preview), keyin chop etish/tugma tanlovi
            await bot.copy_messages(message.chat.id, message.chat.id, ids)
            await message.answer(
                "Shu albomni chop etasizmi? (\"Tugmacha bilan\" tanlasangiz — tugmalar albom ostida "
                "alohida xabarda chiqadi)",
                reply_markup=save_pst,
            )
        else:
            await message.answer("Shu postni chop etasizmi?", reply_markup=admin_main)
            await message.copy_to(message.chat.id, reply_markup=save_pst)
    else:              # foydalanuvchi taklifi
        if album:  # albom taklifini hozircha qabul qilmaymiz (tasdiqlash oqimi murakkab)
            await message.answer(
                "Taklifni <b>bitta post</b> qilib yuboring (albom hozircha qo`llab-quvvatlanmaydi). "
                "Yoki bekor qilish uchun \"Orqaga 🔙\".",
                reply_markup=back_post,
            )
            return
        await state.update_data(from_id=message.from_user.id, from_mention=message.from_user.mention_html())
        await message.reply("📝 E`loningiz saqlandi!", reply_markup=main_menu)
        await message.copy_to(message.chat.id)
        await message.answer("Postni tekshirish uchun yuboraymi?", reply_markup=confirmation_keyboard)
        await state.set_state(NewPost.confirm)


# ── Admin: chop etish tugmalari ───────────────────────────────────
@router.callback_query(AdminPostCB.filter(F.action == "first_url"), IsAdmin())
async def cb_first_url(call: CallbackQuery):
    await call.answer("Havola yaratish bo`limi")
    await call.message.edit_reply_markup(reply_markup=save_pst_url)


@router.callback_query(AdminPostCB.filter(F.action == "first_back"), IsAdmin())
async def cb_first_back(call: CallbackQuery):
    await call.answer("Orqaga qaytdingiz")
    await call.message.edit_reply_markup(reply_markup=save_pst)


@router.callback_query(AdminPostCB.filter(F.action == "first_oddiy"), IsAdmin())
async def cb_first_oddiy(call: CallbackQuery, state: FSMContext, bot: Bot, channels: ChannelRepo, users: UserRepo):
    data = await state.get_data()
    await call.answer("Bu post tugmachalarsiz chop etildi", show_alert=True)
    await _publish(bot, data, await _targets(data, channels, users))
    await call.message.delete()
    await state.clear()


@router.callback_query(AdminPostCB.filter(F.action == "first_new_btn"), IsAdmin())
async def cb_first_new_btn(call: CallbackQuery, state: FSMContext):
    await call.answer("Yangi tugma qo`shish")
    await call.message.answer(
        "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:", reply_markup=back_post
    )
    await state.set_state(NewPost.waiting_btn_text)
    await call.message.delete()


# ── Inline tugma builder (havola yozuvi + url) ────────────────────
@router.message(NewPost.waiting_btn_text, F.text)
async def btn_text_received(message: Message, state: FSMContext, bot: Bot, channels: ChannelRepo, users: UserRepo):
    text = message.text
    if text == "Orqaga 🔙":
        await state.clear()
        await message.answer("Yangi tugmacha qo`shish to`xtatildi!", reply_markup=admin_main)
        return
    if text == "/stop":
        data = await state.get_data()
        buttons = data.get("buttons", {})
        await _publish(bot, data, await _targets(data, channels, users), buttons=buttons)
        await message.answer("Post chop etildi!", reply_markup=admin_main)
        await state.clear()
        return
    await state.update_data(cur_btn=text)
    await message.reply(
        "Endi yangi havola uchun <b>url</b> yoki 🆔 raqamini kiriting:(Kiritgan zahoti chop etiladi!)\n/post_stop"
    )
    await state.set_state(NewPost.waiting_btn_url)


@router.message(NewPost.waiting_btn_url, F.text)
async def btn_url_received(message: Message, state: FSMContext):
    text = message.text
    if text in ("Orqaga 🔙", "/post_stop"):
        await state.clear()
        await message.answer("Yangi tugmacha qo`shish to`xtatildi!", reply_markup=admin_main)
        return
    url = _parse_url(text)
    if url is None:
        await state.clear()
        await message.answer("Siz kiritgan text havola emas !!", reply_markup=admin_main)
        return
    data = await state.get_data()
    buttons = data.get("buttons", {})
    buttons[data["cur_btn"]] = url
    await state.update_data(buttons=buttons)
    await message.answer(
        "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:/stop", reply_markup=back_post
    )
    await state.set_state(NewPost.waiting_btn_text)


# ── Foydalanuvchi taklifini tasdiqlash ────────────────────────────
@router.callback_query(PostCB.filter(F.action == "post"), NewPost.confirm)
async def user_confirm(call: CallbackQuery, state: FSMContext, bot: Bot, admins: AdminRepo):
    data = await state.get_data()
    await state.clear()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Post Adminga yuborildi")
    for admin_id in await admins.all_ids():
        try:
            await bot.send_message(
                admin_id,
                f"Foydalanuvchi {data.get('from_mention')} (<pre>{data.get('from_id')}</pre>) quyidagi postni chop etmoqchi:",
            )
            await bot.copy_message(admin_id, data["src_chat_id"], data["src_message_id"], reply_markup=confirmation_keyboard)
        except Exception:
            pass


@router.callback_query(PostCB.filter(F.action == "cancel"), NewPost.confirm)
async def user_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Post rad etildi.")


@router.message(NewPost.confirm)
async def confirm_unknown(message: Message):
    await message.answer("Chop etish yoki rad etishni tanlang")


# ── Admin taklifni tasdiqlaydi/rad etadi ──────────────────────────
@router.callback_query(PostCB.filter(F.action == "post"), IsAdmin(), StateFilter(None))
async def admin_approve(call: CallbackQuery, bot: Bot, channels: ChannelRepo):
    targets = await channels.all_ids()
    await call.message.edit_reply_markup(reply_markup=None)
    if targets:
        try:
            title = (await bot.get_chat(targets[0])).title
        except Exception:
            title = "kanal"
        await call.answer(f"{title} -- shu kanalda chop etildi!", show_alert=True)
        await call.message.send_copy(targets[0])


@router.callback_query(PostCB.filter(F.action == "cancel"), IsAdmin(), StateFilter(None))
async def admin_decline(call: CallbackQuery):
    await call.answer("Post rad etildi.", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)


# ── Kanal tanlash (one_chanel) + sahifalash ───────────────────────
@router.callback_query(ChannelCB.filter(), IsAdmin())
async def channel_select(call: CallbackQuery, callback_data: ChannelCB, state: FSMContext, bot: Bot, channels: ChannelRepo):
    action, cid = callback_data.action, callback_data.id

    if cid == 0:  # ❌ yopish
        await call.answer()
        await call.message.delete()
        return

    if action == "number":
        chan = await channels.get(cid)
        await state.update_data(sort="first_chanel", channel_id=chan)
        await call.answer()
        await call.message.answer(_POST_PROMPT, reply_markup=back_post)
        await state.set_state(NewPost.waiting_post)
        await call.message.delete()

    elif action == "oldinga":
        if await channels.max_id() == cid:
            await call.answer("Siz so`ngi sahifadasiz!", show_alert=True)
            return
        await call.answer()
        text, ids = await _build_channel_list(bot, await channels.range(cid + 1, cid + 8))
        await call.message.edit_text(text)
        await call.message.edit_reply_markup(reply_markup=num_btn(ids))

    elif action == "orqaga":
        if cid == 1:
            await call.answer("Siz 1-sahifadasiz", show_alert=True)
            return
        await call.answer()
        text, ids = await _build_channel_list(bot, await channels.range(cid - 8, cid - 1))
        await call.message.edit_text(text)
        await call.message.edit_reply_markup(reply_markup=num_btn(ids))
