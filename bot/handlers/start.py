"""/start va majburiy obuna tekshiruvi (check_subs)."""
from aiogram import Bot, F, Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message

from bot.database.repositories import AdminRepo, ChannelRepo, UserRepo
from bot.keyboards.inline import subscription_keyboard
from bot.keyboards.reply import admin_main, main_menu

router = Router()

_SUBSCRIBED = {ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}


async def _is_subscribed(bot: Bot, channel_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(channel_id, user_id)
        return member.status in _SUBSCRIBED
    except Exception:
        return False


@router.message(CommandStart(), StateFilter(None), F.chat.type == "private")
async def show_channels(message: Message, bot: Bot, admins: AdminRepo, users: UserRepo, channels: ChannelRepo):
    user_id = message.from_user.id

    if await admins.exists(user_id):
        await message.answer(
            f"{message.from_user.mention_html()} -- <b>⚜️Admin aka⚜️</b> Assalom-u alaykum Bot xizmatingizda!",
            reply_markup=admin_main,
        )
        return

    if await users.exists(user_id):
        await message.answer(
            "Assalom-u alaykum <b>Foydali yordamchi [PC Mexanics]</b> botga Xush kelibsiz..! Bot xizmatingizda✅",
            reply_markup=main_menu,
        )
        return

    links = []
    for ch in await channels.all_ids():
        try:
            links.append(await bot.export_chat_invite_link(ch))
        except Exception:
            pass
    await message.answer(
        "<b>Foydali yordamchi [PC Mexanics]</b> botga Xush kelibsiz!!\n"
        "Kanalga obuna bo`lsangiz bot xizmatingizda bo`ladi!",
        reply_markup=subscription_keyboard(links),
        disable_web_page_preview=True,
    )


@router.callback_query(F.data == "check_subs")
async def check_subs(call: CallbackQuery, bot: Bot, users: UserRepo, channels: ChannelRepo):
    await call.answer()
    user_id = call.from_user.id  # R6 fix: avval call.message.from_id (bot id) edi

    lines = []
    links = []
    all_ok = True
    for ch in await channels.all_ids():
        ok = await _is_subscribed(bot, ch, user_id)
        all_ok = all_ok and ok
        try:
            chat = await bot.get_chat(ch)
            link = await bot.export_chat_invite_link(ch)
            links.append(link)
            title = chat.title
        except Exception:
            title = "kanal"
        if ok:
            lines.append(f"\n<b><a href='{link}'>{title}</a></b> kanaliga obuna bo'lgansiz!✅")
        else:
            lines.append(f"\n<b><a href='{link}'>{title}</a></b> kanaliga obuna bo'lmagansiz..🤨")

    result = "".join(lines)
    if all_ok:
        if not await users.exists(user_id):
            await users.add(user_id)
        await call.message.answer(result, reply_markup=main_menu, disable_web_page_preview=True)
    else:
        await call.message.answer(result, reply_markup=subscription_keyboard(links), disable_web_page_preview=True)
