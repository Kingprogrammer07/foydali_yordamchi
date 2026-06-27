"""Majburiy obuna gate (eski BigBrother o'rnida) — typed outer middleware.

R7 fix: callback'da update.message None bo'lishi crash bermaydi.
"""
from aiogram import BaseMiddleware, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import Update

from bot.database.repositories import ChannelRepo
from bot.keyboards.inline import subscription_keyboard

_SUBSCRIBED = {ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER}
_ALLOW_COMMANDS = {"/start", "/help"}


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        bot: Bot = data["bot"]
        channels: ChannelRepo = data["channels"]

        # Event turini aniqlash + ruxsat etilgan kirishlar
        if event.message is not None:
            user = event.message.from_user
            chat = event.message.chat
            target = event.message
            first_word = (event.message.text or "").split(maxsplit=1)[:1]
            if first_word and first_word[0] in _ALLOW_COMMANDS:
                return await handler(event, data)
        elif event.callback_query is not None:
            user = event.callback_query.from_user
            msg = event.callback_query.message
            chat = msg.chat if msg else None
            target = msg
            if event.callback_query.data == "check_subs":
                return await handler(event, data)
        else:
            return await handler(event, data)

        # Faqat shaxsiy chatda gate qo'llanadi
        if user is None or chat is None or chat.type != "private":
            return await handler(event, data)

        channel_ids = await channels.all_ids()
        not_subbed = []
        for ch in channel_ids:
            try:
                member = await bot.get_chat_member(ch, user.id)
                if member.status not in _SUBSCRIBED:
                    not_subbed.append(ch)
            except Exception:
                pass

        if not_subbed and target is not None:
            links = []
            for ch in not_subbed:
                try:
                    links.append(await bot.export_chat_invite_link(ch))
                except Exception:
                    pass
            await target.answer(
                "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
                reply_markup=subscription_keyboard(links),
            )
            return  # gate — handler chaqirilmaydi

        return await handler(event, data)
