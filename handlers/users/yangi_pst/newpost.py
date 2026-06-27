from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ContentType
from aiogram.dispatcher.filters import Text
from data.config import ADMINS, CHANNELS
from keyboards.inline.manage_post import confirmation_keyboard, post_callback
from loader import dp, bot
from states.newpost import NewPost_new
from data.post_data import db
import ast
from keyboards.inline.newpst import (
    for_taklif,taklif,
    back,
    for_admin_post,
    one_chanel,
    all_chanel,
    save_pst,
    save_pst_url,
    btn_create,
    num_btn, for_channel
    )
from keyboards.keyboard.all_button import Admin, keyboard

user_entity: dict = {}
analiz: dict = {}
btn_text: dict = {}
tugmalar = {}


type_video = 'video'
type_photo = 'photo'
type_document = 'file'
type_text = 'text'

def controll():
    try:
        if 2 > db.chanel_count():
            return True
        else:
            return False
    except:
        return False

@dp.message_handler(Text(equals = "📎Yangi post✏️"), user_id = ADMINS)
async def fikr(message: Message):
    user_entity.clear()
    analiz.clear()
    btn_text.clear()

    if message.chat.type == "private":
        if controll():
            await message.reply(text = "Reklamani qayerga bermoqchisiz.❓", reply_markup = one_chanel)
        else:
            await message.reply(text = "Reklamani qayerga bermoqchisiz.❓", reply_markup = all_chanel)


@dp.callback_query_handler(for_admin_post.filter())
async def admin_pst(call: CallbackQuery, callback_data: dict):
    action = callback_data.get("action")
    message = call.message
    if action == "first_chanel":       # first channel
        await call.answer(text = "Kanalda post")
        analiz.update({"sort": "first_chanel"})
        await message.answer(text = "Yangi postni yoki E`loningizni kanalga tashlash uchun <b>Qulaylik uchun Tayyor post tashlang</b>❕ yoki rasmdan boshlab post yasang:", reply_markup = back)
        await NewPost_new.NewMessage.set()
        await message.delete()

    elif action == "first_url":
        await call.answer(text = "Havola yaratish bo`limi")
        await call.message.edit_reply_markup(save_pst_url)

    elif action == "first_back":
        await call.answer(text = "Orqaga qaytdingiz")
        await call.message.edit_reply_markup(save_pst)

    elif action == "first_oddiy":         ## kanalga oddiy chop etish
        analizing = analiz.get("yoqlama")
        iid = analiz.get('channel_id')
        if not(analizing == "bor"):
            await call.answer(text = "Bu post kanalga tugmachalarsiz chop etildi", show_alert = True)
            msg = await message.edit_reply_markup()
            await msg.send_copy(chat_id = CHANNELS[0])
            await message.delete()
        else:
            await call.answer(text = "Bu post kanalga tugmachalarsiz chop etildi", show_alert = True)
            msg = await message.edit_reply_markup()
            await msg.send_copy(chat_id = iid[0])
            await message.delete()

    elif action == "first_new_btn":
        await call.answer(text = "Yangi tugma qo`shish")
        await message.answer(text = "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:", reply_markup = back)
        await NewPost_new.new_btn_text.set()
        await message.delete()

    elif action == "in_bot":
        await call.answer(text = "Bot ichida post yuborish")
        await message.answer(text = "Yangi postni yoki E`loningizni botga tashlash uchun <b>Qulaylik uchun Tayyor post tashlang</b>❕ yoki rasmdan boshlab post yasang:", reply_markup = back)
        analiz.update({"sort": "in_bot"})
        await NewPost_new.NewMessage.set()
        await message.delete()

    elif action == "one_chanel":
        await message.reply(text = "Qaysi kanalga <b>Reklama</b> bermoqchisiz❓")
        await call.answer()
        for_btn = []
        malumotlar = str()
        for i in db.vkm_stili():
            channel = await bot.get_chat(i[1])
            invite_link = await channel.export_invite_link()
            for_btn.append(i[0])
            malumotlar += f"\n{i[0]} - <b><a href = '{invite_link}'>{channel.title}</a></b>\n➖➖➖➖➖➖➖➖"
        await message.answer(text = f"{malumotlar}", reply_markup = num_btn(for_btn))
        await message.delete()


                                                                ## taklif va fikr  FOYDALANUVCHILAR
@dp.message_handler(Text(equals = "Taklif"))
async def fikr(message: Message):
    if message.chat.type == "private":
        await message.reply(text = "Siz adminga 🧾<b>reklama post yoki fikringizni</b> bildirmoqchimisiz❓", reply_markup = taklif)

@dp.message_handler(commands = ["yangi_post_taklif"])
async def fikr(message: Message):
    if message.chat.type == "private":
        await message.reply(text = "Siz adminga 🧾<b>reklama post yoki fikringizni</b> bildirmoqchimisiz❓", reply_markup = taklif)


@dp.callback_query_handler(for_taklif.filter(action = 'new_post'))
async def user_pst(call: CallbackQuery):
    message = call.message
    await call.answer(text = "Fikr yoki yangi post tanlandi")
    await message.delete()
    await message.answer(text = "Agar siz adminga 🧾reklama taklif qilmoqchi bo`lsangiz <b>Qulaylik uchun Tayyor post tashlang❕</b> yoki rasmdan boshlab post yasang\nyoki Bot haqida fikringizni ayting:", reply_markup = back)
    await NewPost_new.NewMessage.set()

@dp.message_handler(state=NewPost_new.NewMessage, content_types = ['video', 'document', 'photo', 'text'])                              ##  Yangi post
async def enter_message(message: Message, state: FSMContext):
    chat_id = message.from_id
    text = message.text
    photo = message.photo
    document = message.document
    video = message.video
    caption = message.caption
    caption_entitiy = message.caption_entities
    is_id = db.is_in_post(chat_id)
    is_elon = db.is_in_elon(chat_id)
    sort = analiz.get("sort")
    is_admin = db.is_admin(chat_id)
    analizing = analiz.get("yoqlama")
    try:
        if text:
            if text != "Orqaga 🔙":
                if not(is_elon):
                    if not(is_admin):
                        await state.update_data({"text": text, "mention": message.from_user.get_mention(), "raqam": message.from_id})
                        db.for_elon(chat_id,text)
                        user_entity.update({"entity": f"{message.entities}", "turi": type_text, "usr_id": chat_id})
                        await message.reply(text = "Taklif 📝 E`loningiz saqlandi!", reply_markup = keyboard)
                        await message.reply(text = text,  entities = message.entities)
                        await message.answer(text = "Postni tekshirish uchun yuboraymi?", 
                                            reply_markup = confirmation_keyboard)
                        await NewPost_new.Confirm.set()
                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.for_elon(chat_id,text)
                            await state.update_data({"text": text})
                            user_entity.update({"entity": f"{message.entities}", "turi": type_text})
                            await message.reply(text = "📝 E`loningiz saqlandi!", reply_markup = Admin)
                            await message.reply(text = text,  entities = message.entities, reply_markup = save_pst)


                else:
                    if not(is_admin):
                        await state.update_data({"text": text, "mention": message.from_user.get_mention(), "raqam": message.from_id})
                        db.for_elon_update(chat_id,text)
                        user_entity.update({"entity": f"{message.entities}", "turi": type_text, "usr_id": chat_id})
                        await message.reply(text = "📝 E`loningiz saqlandi!", reply_markup = keyboard)
                        await message.reply(text = text,  entities = message.entities)
                        await message.answer(text = "Postni tekshirish uchun yuboraymi?", 
                                            reply_markup = confirmation_keyboard)
                        await NewPost_new.Confirm.set()
                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.for_elon_update(chat_id,text)
                            await state.update_data({"text": text})
                            user_entity.update({"entity": f"{message.entities}", "turi": type_text})
                            await message.reply(text = "📝 E`loningiz saqlandi!", reply_markup = Admin)
                            await message.reply(text = text,  entities = message.entities, reply_markup = save_pst)
            else:
                await state.finish()
                await message.reply(text = "Yangi post tayyorlash bekor qilindi!", reply_markup = keyboard)

        elif photo:
            if caption is None:
                await state.update_data({"chat_id": chat_id,"file_id": photo[-1].file_id, "turi": type_photo})
                await message.reply(text = "Rasm saqlandi ✅\n<b>📝 Rasm tagidagi xabarni kiriting:</b>")
                await NewPost_new.user_caption.set()
            else:
                if not(is_id):
                    if not(is_admin):
                        await state.finish()
                        db.for_post(chat_id,photo[-1].file_id,caption)
                        user_entity.update({"entity": f"{caption_entitiy}", "turi": type_photo, "usr_id": chat_id})
                        await state.update_data({"file_id": photo[-1].file_id,"caption": caption, "entity": f"{caption_entitiy}","mention": message.from_user.get_mention(), "raqam": message.from_id})     ## btn o`zgartirish -- `
                        await message.reply_photo(photo = photo[-1].file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)
                        await NewPost_new.Confirm.set()
                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.for_post(chat_id,photo[-1].file_id,caption)
                            user_entity.update({"entity": f"{caption_entitiy}", "turi": type_photo})
                            await state.update_data({"file_id": photo[-1].file_id,"caption": caption, "entity": f"{caption_entitiy}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_photo(photo = photo[-1].file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = save_pst)

                else:
                    if not(is_admin):
                        await state.finish()
                        db.post_update(photo[-1].file_id,caption,chat_id)
                        user_entity.update({"entity": f"{caption_entitiy}", "turi": type_photo})
                        await state.update_data({"file_id": photo[-1].file_id,"caption": caption, "entity": f"{caption_entitiy}","mention": message.from_user.get_mention(), "raqam": message.from_id})     ## btn o`zgartirish -- `
                        await message.reply_photo(photo = photo[-1].file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)
                        await NewPost_new.Confirm.set()
                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.post_update(photo[-1].file_id,caption,chat_id)
                            user_entity.update({"entity": f"{caption_entitiy}", "turi": type_photo})
                            await state.update_data({"file_id": photo[-1].file_id,"caption": caption, "entity": f"{caption_entitiy}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_photo(photo = photo[-1].file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = save_pst)



        elif document:
            if caption is None:
                await state.update_data({"chat_id": chat_id,"file_id": document.file_id, "turi": type_document})
                await message.reply(text = "Fayl saqlandi saqlandi ✅\n<b>📝 Fayl tagidagi xabarni kiriting:</b>")
                await NewPost_new.user_caption.set()

            else:
                if not(is_id):
                    if not(is_admin):
                        await state.finish()
                        db.for_post(chat_id,document.file_id,caption)
                        user_entity.update({"entity": f"{caption_entitiy}", "turi": type_document, "usr_id": chat_id})
                        await state.update_data({"caption": caption, "entity": f"{caption_entitiy}","mention": message.from_user.get_mention()})     ## btn o`zgartirish -- `
                        await message.reply_document(document = document.file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)
                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.for_post(chat_id,document.file_id,caption)
                            user_entity.update({"entity": f"{caption_entitiy}", "turi": type_document})
                            await state.update_data({"caption": caption, "entity": f"{caption_entitiy}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_document(document = document.file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = save_pst)

                
                else:
                    if not(is_admin):
                        await state.finish()
                        db.post_update(document.file_id,caption,chat_id)
                        user_entity.update({"entity": f"{caption_entitiy}", "turi": type_document})
                        await state.update_data({"caption": caption, "entity": f"{caption_entitiy}","mention": message.from_user.get_mention()})     ## btn o`zgartirish -- `
                        await message.reply_document(document = document.file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)
                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.post_update(document.file_id,caption,chat_id)
                            user_entity.update({"entity": f"{caption_entitiy}", "turi": type_document})
                            await state.update_data({"file_id": document.file_id,"caption": caption, "entity": f"{caption_entitiy}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_document(document = document.file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = save_pst)


        elif video:
            if caption is None:
                await state.update_data({"chat_id": chat_id,"file_id": video.file_id, "turi": type_video})
                await message.reply(text = "Video saqlandi saqlandi ✅\n<b>📝 Video tagidagi xabarni kiriting:</b>")
                await NewPost_new.user_caption.set()

            else:
                if not(is_id):
                    if not(is_admin):
                        await state.finish()
                        db.for_post(chat_id,video.file_id,caption)
                        user_entity.update({"entity": f"{caption_entitiy}", "turi": type_video, "usr_id": chat_id})
                        await state.update_data({"file_id": video.file_id,"caption": caption, "entity": f"{caption_entitiy}","mention": message.from_user.get_mention(), "raqam": message.from_id})     ## btn o`zgartirish -- `
                        await message.reply_video(video = video.file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)
                        await NewPost_new.Confirm.set()

                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":    
                            await state.finish()
                            db.for_post(chat_id,video.file_id,caption)
                            user_entity.update({"entity": f"{caption_entitiy}", "turi": type_video})
                            await state.update_data({"file_id": video.file_id,"caption": caption, "entity": f"{caption_entitiy}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_video(video = video.file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = save_pst)


                else:
                    if not(is_admin):
                        await state.finish()
                        db.post_update(video.file_id,caption,chat_id)
                        user_entity.update({"entity": f"{caption_entitiy}", "turi": type_video})
                        await state.update_data({"file_id": video.file_id,"caption": caption, "entity": f"{caption_entitiy}","mention": message.from_user.get_mention(), "raqam": message.from_id})     ## btn o`zgartirish -- `
                        await message.reply_video(video = video.file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)
                        await NewPost_new.Confirm.set()
                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":    
                            await state.finish()
                            db.post_update(video.file_id,caption,chat_id)
                            user_entity.update({"entity": f"{caption_entitiy}", "turi": type_video})
                            await state.update_data({"file_id": video.file_id,"caption": caption, "entity": f"{caption_entitiy}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_video(video = video.file_id, caption = caption, caption_entities = caption_entitiy, reply_markup = save_pst)
        
        else:                                                           ## btn o`zgartirish` --
            await message.reply(text = "Xato turdagi fayl tashlandi!! Boshidan  boshlang!", reply_markup = keyboard)
            await state.finish()
    except:
        await state.finish()
        for i in ADMINS:
            await bot.send_message(chat_id = i,text = "Fayllarni turlashda xatolik bor! [ newpost.py line: 59 ]", reply_markup = Admin)


@dp.message_handler(state = NewPost_new.user_caption, content_types = ContentType.TEXT)
async def get_caption(message: Message, state: FSMContext):
    text = message.text
    chat_id = message.from_id
    is_id = db.is_in_post(chat_id)
    data = await state.get_data()
    file_id = data.get("file_id")
    user_id = data.get("chat_id")
    is_admin = db.is_admin(chat_id)
    turi = data.get("turi")
    entities = message.entities
    sort = analiz.get("sort")
    analizing = analiz.get("yoqlama")

    if text == "Orqaga 🔙":
        await state.finish()
        await message.reply(text = "Yangi post tayyorlash to`xtatildi", reply_markup = keyboard)
    else:
        try:
            if turi == type_photo:
                if not(is_id):
                    if not(is_admin):
                        await state.finish()
                        db.for_post(user_id,file_id,text)
                        user_entity.update({"entity": f"{entities}", "turi": type_photo})
                        await state.update_data({"file_id": file_id,"caption": text, "entity": f"{entities}", "mention": message.from_user.get_mention(), "raqam": message.from_id})     ## btn o`zgartirish -- `
                        await message.reply_photo(photo = file_id, caption = text, caption_entities = entities, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)
                        await NewPost_new.Confirm.set()

                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.for_post(user_id,file_id,text)
                            user_entity.update({"entity": f"{message.entities}", "turi": type_photo})
                            await state.update_data({"caption": text, "entity": f"{entities}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_photo(photo = file_id, caption = text, caption_entities = entities, reply_markup = save_pst)

                else:
                    if not(is_admin):
                        await state.finish()
                        db.post_update(file_id,text,user_id)
                        user_entity.update({"entity": f"{entities}", "turi": type_photo})
                        await state.update_data({"file_id": file_id,"caption": text, "entity": f"{entities}", "mention": message.from_user.get_mention(), "raqam": message.from_id})     ## btn o`zgartirish -- `
                        await message.reply_photo(photo = file_id, caption = text, caption_entities = entities, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)
                        await NewPost_new.Confirm.set()
                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.post_update(file_id,text,user_id)
                            user_entity.update({"entity": f"{entities}", "turi": type_photo})
                            await state.update_data({"file_id": file_id,"caption": text, "entity": f"{entities}"})     ## btn o`zgartirish -- `
                            await message.reply_photo(photo = file_id, caption = text, caption_entities = entities, reply_markup = save_pst)


            elif turi == type_document:
                if not(is_id):
                    if not(is_admin):
                        await state.finish()
                        db.for_post(user_id,file_id,text)
                        user_entity.update({"entity": f"{entities}", "turi": type_document})
                        await state.update_data({"caption": text, "entity": f"{entities}","mention": message.from_user.get_mention()})     ## btn o`zgartirish -- `
                        await message.reply_document(document = file_id, caption = text, caption_entities = entities, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)

                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.for_post(user_id,file_id,text)
                            user_entity.update({"entity": f"{entities}", "turi": type_document})
                            await state.update_data({"caption": text, "entity": f"{entities}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_document(document = file_id, caption = text, caption_entities = entities, reply_markup = save_pst)

                
                else:
                    if not(is_admin):
                        await state.finish()
                        db.post_update(file_id,text,user_id)
                        user_entity.update({"entity": f"{entities}", "turi": type_document})
                        await state.update_data({"caption": text, "entity": f"{entities}","mention": message.from_user.get_mention()})     ## btn o`zgartirish -- `
                        await message.reply_document(document = file_id, caption = text, caption_entities = entities, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)
                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.post_update(file_id,text,user_id)
                            user_entity.update({"entity": f"{entities}", "turi": type_document})
                            await state.update_data({"file_id": file_id,"caption": text, "entity": f"{entities}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_document(document = file_id, caption = text, caption_entities = entities, reply_markup = save_pst)


            elif turi == type_video:
                if not(is_id):
                    if not(is_admin):
                        await state.finish()
                        db.for_post(user_id,file_id,text)
                        user_entity.update({"entity": f"{entities}", "turi": type_video})
                        await state.update_data({"file_id": file_id,"caption": text, "entity": f"{entities}","mention": message.from_user.get_mention(), "raqam": message.from_id})     ## btn o`zgartirish -- `
                        await message.reply_video(video = file_id, caption = text, caption_entities = entities, reply_markup = keyboard)
                        await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                            reply_markup=confirmation_keyboard)
                        await NewPost_new.Confirm.set()

                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":
                            await state.finish()
                            db.for_post(user_id,file_id,text)
                            user_entity.update({"entity": f"{entities}", "turi": type_video})
                            await state.update_data({"caption": text, "entity": f"{entities}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_video(video = file_id, caption = text, caption_entities = entities, reply_markup = save_pst)
                
                else:
                    if not(is_admin):
                            await state.finish()
                            db.post_update(file_id,text,user_id)
                            user_entity.update({"entity": f"{entities}", "turi": type_video})
                            await state.update_data({"file_id": file_id,"caption": text, "entity": f"{entities}","mention": message.from_user.get_mention(), "raqam": message.from_id})     ## btn o`zgartirish -- `
                            await message.reply_video(video = file_id, caption = text, caption_entities = entities, reply_markup = keyboard)
                            await message.answer(f"Postni tekshirish uchun yuboraymi?",
                                                reply_markup=confirmation_keyboard)
                            await NewPost_new.Confirm.set()
                    else:
                        if sort == "first_chanel" or sort == "in_bot" or analizing == "bor":    
                            await state.finish()
                            db.post_update(file_id,text,user_id)
                            user_entity.update({"entity": f"{entities}", "turi": type_video})
                            await state.update_data({"file_id": file_id,"caption": text, "entity": f"{entities}"})     ## btn o`zgartirish -- `
                            await message.answer(text = "Shu postni chop etasizmi?", reply_markup = Admin)
                            await message.reply_video(video = file_id, caption = text, caption_entities = entities, reply_markup = save_pst)
            

            else:                                                           ## btn o`zgartirish` --
                await message.reply(text = "Xato turdagi fayl tashlandi!! Boshidan  boshlang!", reply_markup = keyboard)
                await state.finish()
        except:
            await state.finish()
            for i in ADMINS:
                await bot.send_message(chat_id = i, text = "newpost.py xatolik bor postni yig`ishda!! [ Line: 326 ]", reply_markup = Admin)


@dp.message_handler(Command("yangi_post"))
async def create_post(message: Message):
    await message.answer("Chop etish uchun post yuboring.")
    await NewPost_new.NewMessage.set()


@dp.message_handler(state = NewPost_new.new_btn_text, content_types = ContentType.TEXT,user_id = ADMINS)                                       ## yangi btn text
async def create_btn_txt(message: Message, state: FSMContext):
    text = message.text
    if text == "Orqaga 🔙":
        await state.finish()
        await message.reply(text = "Yangi tugmacha qo`shish to`xtatildi!", reply_markup = keyboard)
    
    elif text == "/stop" and not(analiz.get("sort") == "in_bot"):
        get_text = tugmalar
        turi = user_entity.get("turi")
        analizing = analiz.get("yoqlama")
        kanal_id = analiz.get('channel_id')
        try:
            user_entity.update({'entity': user_entity.get("entity").replace("<MessageEntity","").replace(">","")})
            enti = ast.literal_eval(user_entity.get('entity'))
        except:
            pass

        if turi == type_photo:
            if not(analizing == "bor"):
                for post in db.for_post_view(message.from_id):
                    await bot.send_photo(chat_id = CHANNELS[0], photo = post[0], caption = post[1], caption_entities = enti, reply_markup = btn_create(get_text))
            else:
                for post in db.for_post_view(message.from_id):
                    await bot.send_photo(chat_id = kanal_id, photo = post[0], caption = post[1], caption_entities = enti, reply_markup = btn_create(get_text))
        
        elif turi == type_document:
            if not(analizing == "bor"):
                for post in db.for_post_view(message.from_id):
                    await bot.send_document(chat_id = CHANNELS[0], document = post[0], caption = post[1], caption_entities = enti, reply_markup = btn_create(get_text))
            else:
                for post in db.for_post_view(message.from_id):
                        await bot.send_document(chat_id = kanal_id, document = post[0], caption = post[1], caption_entities = enti, reply_markup = btn_create(get_text))
        
        elif turi == type_video:
            if not(analizing == "bor"):
                for post in db.for_post_view(message.from_id):
                    await bot.send_video(chat_id = CHANNELS[0], video = post[0], caption = post[1], caption_entities = enti, reply_markup = btn_create(get_text))
            else:
                for post in db.for_post_view(message.from_id):
                    await bot.send_video(chat_id = kanal_id, video = post[0], caption = post[1], caption_entities = enti, reply_markup = btn_create(get_text))
        
        elif turi == type_text:
            if not(analizing == "bor"):
                for post in db.for_elon_view(message.from_id):
                    await bot.send_message(chat_id = CHANNELS[0], text = post,entities = enti, reply_markup = btn_create(get_text))
            else:                
                for post in db.for_elon_view(message.from_id):
                    await bot.send_message(chat_id = kanal_id, text = post,entities = enti, reply_markup = btn_create(get_text))

        await message.answer(text = "Post kanalda chop etildi!", reply_markup = Admin)
        await state.finish()
        tugmalar.clear()
        analiz.clear()
        user_entity.clear()

    elif (text == "/stop") and (analiz.get("sort") == "in_bot"):
        get_text = tugmalar
        turi = user_entity.get("turi")
        try:
            user_entity.update({'entity': user_entity.get("entity").replace("<MessageEntity","").replace(">","")})
            enti = ast.literal_eval(user_entity.get('entity'))
        except:
            pass

        if turi == type_photo:
            try:
                for post in db.for_post_view(message.from_id):
                    for i in list(*zip(*db.user_view())):
                        await bot.send_photo(chat_id = i, photo = post[0], caption = post[1], caption_entities = enti, reply_markup = btn_create(get_text))
            except:
                pass
        elif turi == type_document:
            try:
                for post in db.for_post_view(message.from_id):
                    for i in list(*zip(*db.user_view())):
                        await bot.send_document(chat_id = i, document = post[0], caption = post[1], caption_entities = enti, reply_markup = btn_create(get_text))
            except:
                pass
        elif turi == type_video:
            try:
                for post in db.for_post_view(message.from_id):
                    for i in list(*zip(*db.user_view())):
                        await bot.send_video(chat_id = i, video = post[0], caption = post[1], caption_entities = enti, reply_markup = btn_create(get_text))
            except:
                pass
        elif turi == type_text:
            try:
                for post in db.for_elon_view(message.from_id):
                    for i in list(*zip(*db.user_view())):
                        await bot.send_message(chat_id = i, text = post,entities = enti, reply_markup = btn_create(get_text))
            except:
                pass
        await message.answer(text = "Post botda chop etildi!", reply_markup = Admin)
        await state.finish()

        user_entity.clear()
        tugmalar.clear()

    else:
        await state.update_data(btn_txt = text)
        btn_text.update(btn_txt = text)
        await message.reply(text = "Endi yangi havola uchun <b>url</b> yoki 🆔 raqamini kiriting:(Kiritgan zahoti chop etiladi!)\n/post_stop")
        if not(analiz.get("sort") == "in_bot"):
            await NewPost_new.new_btn_url.set()
        else:
            await NewPost_new.inbot_url.set()

@dp.message_handler(state = NewPost_new.new_btn_url, content_types = ContentType.TEXT, user_id = ADMINS)  # first channel uchun                                     ## yangi btn text
async def create_btnn_txt(message: Message, state: FSMContext):
    text = message.text
    get_text = btn_text.get("btn_txt")
    if text == "Orqaga 🔙" or text == "/post_stop":
        await state.finish()
        await message.reply(text = "Yangi tugmacha qo`shish to`xtatildi!", reply_markup = Admin)
    else:
        if text.isdigit():
            txt = int(text)
            if 99999999 < txt:
                user_url = f"tg://user?id={txt}"
                tugmalar.update({get_text: user_url})
                await message.answer(text = "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:/stop", reply_markup = back)
                await NewPost_new.new_btn_text.set()
            else:
                await message.reply(text = f"<b>{txt}</b> siz kiritgan raqam telegram foydalanuvchilar 🆔 raqami orasida topilmadi ‼️", reply_markup = Admin)
                await state.finish()

        elif text.startswith("@"):
            user_url = f"https://t.me/{text[1:]}"                
            tugmalar.update({get_text: user_url})
            await message.answer(text = "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:/stop", reply_markup = back)
            await NewPost_new.new_btn_text.set()

        elif "/" in text:
            user_url = f"{text}"
            tugmalar.update({get_text: user_url})
            await message.answer(text = "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:/stop", reply_markup = back)
            await NewPost_new.new_btn_text.set() 
        
        elif text.endswith(".com") or text.endswith(".uz") or text.endswith(".ru"):
            user_url = f"https://{text}"
            tugmalar.update({get_text: user_url})
            await message.answer(text = "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:/stop", reply_markup = back)
            await NewPost_new.new_btn_text.set()

        else:
            await message.answer(text = "Siz kiritgan text havola emas !!", reply_markup = Admin)
            await state.finish()


@dp.message_handler(state = NewPost_new.inbot_url, content_types = ContentType.TEXT, user_id = ADMINS)  # bot uchun                                     ## yangi btn text
async def create_bon_txt(message: Message, state: FSMContext):
    text = message.text
    if text == "Orqaga 🔙" or text == "/post_stop":
        await state.finish()
        await message.reply(text = "Yangi tugmacha qo`shish to`xtatildi!", reply_markup = Admin)
    else:
        get_text = btn_text.get("btn_txt")
        if text.isdigit():
            txt = int(text)
            if 99999999 < txt:
                user_url = f"tg://user?id={txt}"
                tugmalar.update({get_text: user_url})
                await message.answer(text = "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:/stop", reply_markup = back)
                await NewPost_new.new_btn_text.set()

        elif text.startswith("@"):
            user_url = f"https://t.me/{text[1:]}"
            tugmalar.update({get_text: user_url})
            await message.answer(text = "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:/stop", reply_markup = back)
            await NewPost_new.new_btn_text.set()
        
        elif "/" in text:
            user_url = f"{text}"
            tugmalar.update({get_text: user_url})
            await message.answer(text = "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:/stop", reply_markup = back)
            await NewPost_new.new_btn_text.set()
        
        elif text.endswith(".com") or text.endswith(".uz") or text.endswith(".ru"):
            user_url = f"https://{text}"
            tugmalar.update({get_text: user_url})
            await message.answer(text = "➕ Yangi havola qo`shish uchun avval havola <b>yozuvini</b> kiriting!:/stop", reply_markup = back)
            await NewPost_new.new_btn_text.set()

        else:
            await message.answer(text = "Siz kiritgan text havola emas !!", reply_markup = Admin)
            await state.finish()


@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost_new.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        caption = data.get("caption")
        mention = data.get("mention")
        file_id = data.get("file_id")
        text = data.get("text")
        foy_id = data.get("raqam")
    turi = user_entity.get("turi")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post Adminga yuborildi")
    try:
        user_entity.update({'entity': user_entity.get("entity").replace("<MessageEntity","").replace(">","")})
        enti = ast.literal_eval(user_entity.get('entity'))
    except:
        pass
    try:
        if turi == type_photo:
            for user in list(*zip(*db.admin_view())):
                await bot.send_message(chat_id = user,text = f"Foydalanuvchi {mention} (<pre>{foy_id}</pre>) quyidagi postni chop etmoqchi:")
                await bot.send_photo(chat_id = user, photo = file_id, caption = f"{caption}", caption_entities = enti, reply_markup = confirmation_keyboard)

        elif turi == type_document:
            for user in list(*zip(*db.admin_view())):
                await bot.send_message(chat_id = user,text = f"Foydalanuvchi {mention} (<pre>{foy_id}</pre>) quyidagi postni chop etmoqchi:")
                await bot.send_document(chat_id = user, document = file_id, caption = f"{caption}", caption_entities = enti, reply_markup = confirmation_keyboard)

        elif turi == type_video:
            for user in list(*zip(*db.admin_view())):
                await bot.send_message(chat_id = user,text = f"Foydalanuvchi {mention} (<pre>{foy_id}</pre>) quyidagi postni chop etmoqchi:")
                await bot.send_video(chat_id = user, video = file_id, caption = f"{caption}", caption_entities = enti, reply_markup = confirmation_keyboard)

        elif turi == type_text:
            for user in list(*zip(*db.admin_view())):
                await bot.send_message(chat_id = user,text = f"Foydalanuvchi {mention} (<pre>{foy_id}</pre>) quyidagi postni chop etmoqchi:")
                await bot.send_message(chat_id = user, text = text, entities = enti, reply_markup = confirmation_keyboard)

        else:
            for i in ADMINS:
                await bot.send_message(chat_id = i, text = "Malumotlarni adminga yuborishda xatolik! [newpost.py Line: 140 ]", reply_markup = Admin)
    except:
        for i in ADMINS:
            await bot.send_message(chat_id = i, text = "Malumotlarni Adminga yuborishda xatolik! [ newpost.py Line: 137 ]", reply_markup = Admin)


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=NewPost_new.Confirm)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post rad etildi.")


@dp.message_handler(state=NewPost_new.Confirm)
async def post_unknown(message: Message):
    await message.answer("Chop etish yoki rad etishni tanlang")

#########################    takliflar uchun
@dp.callback_query_handler(post_callback.filter(action="post"), user_id=ADMINS)
async def approve_post(call: CallbackQuery):
    channel = await bot.get_chat(CHANNELS[0])
    await call.answer(text = f"{channel.title} -- shu kanalda chop etildi!", show_alert = True) 
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id = CHANNELS[0])

@dp.callback_query_handler(post_callback.filter(action="cancel"), user_id=ADMINS)
async def decline_post(call: CallbackQuery):
    await call.answer("Post rad etildi.", show_alert=True)
    await call.message.edit_reply_markup()


@dp.callback_query_handler(for_channel.filter(), user_id = ADMINS)
async def btn_control(call: CallbackQuery, callback_data: dict):
    left_right = callback_data.get("action")
    id = callback_data.get("id")
    id = int(id)

    if id == 0:
        await call.answer()
        await call.message.delete()

    elif not(left_right == "orqaga") and not(left_right == "oldinga") and not(id == 0):
        await call.answer()
        chan = db.get_malumot(id)
        analiz.update({"channel_id": chan, "yoqlama": "bor"})
        await call.message.answer(text = "Yangi postni yoki E`loningizni kanalga tashlash uchun <b>Qulaylik uchun Tayyor post tashlang</b>❕ yoki rasmdan boshlab post yasang:", reply_markup = back)
        await NewPost_new.NewMessage.set()
        await call.message.delete()


    elif left_right == "oldinga":
        for_btn = []
        ismlar = str()
        k = int(id)+1
        b = int(id)+8
        if not(db.is_max() == id):
            await call.answer()
            for a in db.view(k,b):
                channel = await bot.get_chat(a[1])
                invite_link = await channel.export_invite_link()
                ismlar += f"\n{a[0]} - <b><a href = '{invite_link}'>{channel.title}</a></b>\n➖➖➖➖➖➖➖➖"
                for_btn.append(a[0])
            await call.message.edit_text(ismlar)
            await call.message.edit_reply_markup(num_btn(for_btn))
        else:
            await call.answer(text = "Siz so`ngi sahifadasiz!", show_alert = True)

    elif left_right == "orqaga":
        if id == 1:
            await call.answer(text = "Siz 1-sahifadasiz", show_alert = True)
        else:
            for_btn = []
            ismlar = str()
            for a in db.view(int(id)-8,int(id)-1):
                channel = await bot.get_chat(a[1])
                invite_link = await channel.export_invite_link()
                ismlar += f"\n{a[0]} - <b><a href = '{invite_link}'>{channel.title}</a></b>\n➖➖➖➖➖➖➖➖"
                for_btn.append(a[0])
            await call.message.edit_text(ismlar)
            await call.message.edit_reply_markup(num_btn(for_btn))

    else:
        await call.answer(text = "Xatolik callbackqueryda [ LINE: 814 ]", show_alert = True)



