from aiogram.types import CallbackQuery, Message
from data.config import CHANNELS
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.subscription import btn
from keyboards.keyboard.all_button import Admin, keyboard
from loader import bot, dp
from utils.misc import subscription
from data.post_data import db


@dp.message_handler(CommandStart())
async def show_channels(message: Message):
    is_admin = lambda chat_id: db.is_admin(chat_id)
    link = []
    if message.chat.type == 'private':    
        if is_admin(message.from_id):
            await message.answer(text = f"{message.from_user.get_mention()} -- <b>⚜️Admin aka⚜️</b> Assalom-u alaykum Bot xizmatingizda!", reply_markup = Admin)

        elif db.is_user(message.from_id):
            await message.answer(text = "Assalom-u alaykum <b>Foydali yordamchi [PC Mexanics]</b> botga Xush kelibsiz..! Bot xizmatingizda✅", reply_markup = keyboard)
        else:
            if not(db.is_user(message.from_id)):
                for channel in CHANNELS:
                    chat = await bot.get_chat(channel)
                    invite_link = await chat.export_invite_link()
                    link.append(invite_link)
                await message.answer(f"<b>Foydali yordamchi [PC Mexanics]</b> botga Xush kelibsiz!!\nKanalga obuna bo`lsangiz bot xizmatingizda bo`ladi!",
                                    reply_markup = btn(link),
                                    disable_web_page_preview = True)
                link.clear()

    else:
        pass

@dp.callback_query_handler(text = "check_subs")
async def checker(call: CallbackQuery):
    await call.answer()
    result = str()
    link = []
    for channel in CHANNELS:
        status = await subscription.check(user_id = call.from_user.id,
                                          channel = channel)
        channel = await bot.get_chat(channel)
        invite_link = await channel.export_invite_link()
        link.append(invite_link)
        if not(status):
            result += (f"\n<b><a href = '{invite_link}'>{channel.title}</a></b> kanaliga obuna bo'lmagansiz..🤨")
        else:
            result += f"\n<b><a href = '{invite_link}'>{channel.title}</a></b> kanaliga obuna bo'lgansiz!✅"

    if status:
        await call.message.answer(result, reply_markup = keyboard, disable_web_page_preview=True)
    else:
        await call.message.answer(result, reply_markup = btn(link), disable_web_page_preview=True)
        link.clear()
    if not(db.is_user(call.message.from_id)):
        db.user_plus(call.message.from_id)
