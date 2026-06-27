from aiogram import types
from loader import dp, bot 
from aiogram.types import ContentType
from data.post_data import db
from keyboards.keyboard.all_button import (
    keyboard, Admin, 
    admin_min_plus, orqaga, 
    foydalanuvchilar, 
    sinf11, sinf10, sinf9, sinf8, sinf7,
    pc, booknomy, grafik_dasturlar,
    windows_turlari, video_montaj,
    office, windows_orginal, windows_liteos)
from states.for_admin import Admin_manager
from keyboards.inline.bot_post_ctr import bot_post, ishlatish
from aiogram.dispatcher import FSMContext
from keyboards.inline.newpst import delete_btn, for_delete

is_admin = lambda chat_id: db.is_admin(chat_id)

muloqot = ['parol', 'password', "pass", 'kod', 'zip paroli', 'kodi', 'buni kodi nima', 'kodi nima', 'paroli nima', 'nima kod', 'nima buni kodi', 'paroli nima buni', 'buni paroli nima']
muloqot2 = ['yordam', 'help', 'yordam berish', 'yordam bervoringla', 'yordam beringlar', 'yordam bervoringlar']
muloqot3 = ['kerak', 'topib bering', 'telegram bot', 'bot']

xabarlar: dict= {}
for_delete_user = {}

bot_linki = "🤖<a href='https://t.me/foydali_dastur_kitobbot'>Foydali yordamchi [PC Mexanics]</a>"
kanal_link = "<a href='https://t.me/windowsuzprogrammaa'>📲Telegram</a> | <a href='https://www.instagram.com/invites/contact/?i=m95peeh67d9u&utm_content=o9912bw'>📷instagram</a> | <a href='http://youtube.com/channel/UCKhQtK94Fh5RrxOzlKr6asQ'>🎥Youtube</a>"



@dp.message_handler(content_types = ContentType.TEXT)        ## ASOSIY QISIM
async def admin_part(message: types.Message):
    text = message.text
    chat_id = message.from_id
    if message.chat.type == "private":
        if text == "👤Foydalanuvchi bo`limi👥" and is_admin(chat_id):                         ## Foydalanuvchi bo`lim
            await message.reply(text = "Siz Foydalanuvchi bo`limidasiz!\n<b>Admin bo`limiga o`tish uchun /start buyrug`ini bering!</b>", reply_markup = keyboard)

        elif text == "Admin menejer🎛" and is_admin(chat_id):                              ## admin manager
            await message.reply(text = 'Bo`limni tanlang👇', reply_markup = admin_min_plus)
            
        elif text == "Admin qo`shish➕" and is_admin(chat_id):                            ## admin qo`shish`
            await message.reply(text = 'Qo`shmoqchi bo`lgan foydalanuvchi 🆔 sini kiriting:', reply_markup = orqaga)
            await Admin_manager.admin_qosh.set()

        elif text == "Adminni olib tashlash➖" and is_admin(chat_id):                   ## adminlarni olib tashlash
            for_delete_user.clear()
            tartib = str()
            for_btn = []
            for ega in db.vkm_stili_admin():
                tartib += f"\n<b>{ega[0]}</b>. 🆔 raqami: <pre><b>{ega[1]}</b></pre>\nProfili: <a href='tg://user?id={ega[1]}'>Ko`rish uchun bosing!</a>\n➖➖➖➖➖➖➖➖➖➖➖\n"
                for_btn.append(ega[0])
            if len(for_btn) > 1:
                await message.reply(text = 'Adminlikdan bo`shatadigan odamning\n<b> - ustiga bosing:</b>')
                await message.reply(text = tartib, reply_markup = delete_btn(for_btn))
                for_delete_user.update(admin = "yes")
            else:
                await message.answer(text = "‼️ <b>Kamida 1 kishi botga admin bo`lishi kerak\nSiz admin o`chirolmaysiz</b> ‼️", reply_markup = admin_min_plus)
                


        elif text == 'Admin asosiy':                                 ## admin manager asosiy bo`lim`
            await message.answer(text = 'Siz asosiy bo`limdasiz Admin', reply_markup = Admin)

        elif text == "Kanal qo`shish➕" and is_admin(chat_id):                              ##  Kanal qoshish
            await message.reply(text = "Qo`shmoqchi bo`lgan <b>Kanalingizni</b> 🆔 sini (Kanallarning ID raqami (-)manfiy bo`ladi) kiriting:", reply_markup = orqaga)
            await message.answer(text = "‼️  <b>Avval Botni kanalga qo`shib admin qiling</b>  ‼️")
            await Admin_manager.channel_add.set()

        elif text == "Kanalni olib tashlash➖" and is_admin(chat_id):                       #  kanalni olib  tashlsh
            for_delete_user.clear()
            for_btn = []
            malumotlar = str()
            for i in db.vkm_stili():
                channel = await bot.get_chat(i[1])
                invite_link = await channel.export_invite_link()
                for_btn.append(i[0])
                malumotlar += f"\n{i[0]} - <b><a href = '{invite_link}'>{channel.title}</a></b>\n➖➖➖➖➖➖➖➖"
            
            if len(for_btn) > 1:
                await message.reply(text = "Qaysi kanalni olib tashlamoqchi bo`lsangiz o`shani\n<b>ustiga bosing:</b>")
                await message.answer(text = f"{malumotlar}", reply_markup = delete_btn(for_btn))
                for_delete_user.update(kanal = "yes")

            else:
                await message.answer(text = "‼️ <b>Kamida 1 ta kanal botga ulangan bo`lishi kerak\nSiz kanal o`chirolmaysiz</b> ‼️", reply_markup = admin_min_plus)

        elif text == "Foydalanuvchilarga yozish" and is_admin(chat_id):
            await message.reply(text = "Botning Foydalanuvchilariga yozish uchun <b>ularning 🆔 raqamini kiriting:</b>", reply_markup = orqaga)
            await Admin_manager.users_text.set()

                                                    ## foydalanuvchilar bo`limi`

        elif text == "🆔 orqali topish" or text == "/id_orqali_topish":
            await message.reply(text = '✅ Telegram Foydalanuvchilarini 🆔 raqami orqali topish🔎\n📝 To`liq ma`lumot uchun: <b>/search_about</b>', reply_markup = ishlatish)
        

        elif text == "📚Maktab darsliklari📚":
            await message.reply(text = "Siz maktab darsliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply_markup = foydalanuvchilar)

        elif text == "PDF ochadigan dastur(apk) va (exe)🎛":
            await message.answer_document("https://t.me/baza_java_strong/18",
                caption = "📲Telefon uchun")
            await message.answer_document("https://t.me/baza_java_strong/21",
                caption = "💻Kompyuter uchun")

        elif text == "📚11-Sinf darsliklar📚":
            await message.answer(text = "11-sinf dasrliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply_markup = sinf11)
        
        elif text == "📚10-Sinf yangi darsliklar📚":
            await message.answer(text = "10-sinf darsliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply_markup = sinf10)

        elif text == "📚9-Sinf darsliklar📚":
            await message.answer(text = "9-sinf darsliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply_markup = sinf9)

        elif text == "📚8-Sinf darsliklar📚":
            await message.answer(text = "8-sinf darsliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply_markup = sinf8)

        elif text == "📚7-Sinf yangi darsliklar📚":
            await message.answer(text = "7-sinf bo`limidasiz ➡️ Menuni Tanlang!👇", reply_markup = sinf7)

        elif text == "Asosiy Bo`lim⬅️":
            await message.answer(text = "Siz asosiy bo`limdasiz! Menyuni tanlang👇", reply_markup = keyboard)

                                                                            ## 11- sinf

        elif text == "11-Sinf Matematika 1-qism📘":
            await message.answer_document("https://t.me/baza_java_strong/81?single")

        elif text == "11-Sinf Rus tili📘":
            await message.answer_document("https://t.me/baza_java_strong/82?single")

        elif text == "11-Sinf Adabiyot 1-qism📘":
            await message.answer_document("https://t.me/baza_java_strong/83?single")

        elif text == "11-Sinf Adabiyot 2-qism📘":
            await message.answer_document("https://t.me/baza_java_strong/84?single" )

        elif text == "11-Sinf Ona tili 2-qism📘":
            await message.answer_document("https://t.me/baza_java_strong/85?single")

        elif text == "11-Sinf Kimyo📘":
            await message.answer_document("https://t.me/baza_java_strong/86?single")

                                                                                ##  10 sinf

        elif text == "10-Sinf Biologiya📘":
            await message.answer_document("https://t.me/baza_java_strong/2",
                caption = "Biologiya Kitob apk fayl olish:\n/apk_b1")

        elif text == "10-Sinf Kimyo📘":
            await message.answer_document("https://t.me/baza_java_strong/3",
                caption = "Kimyo Kitob apk fayl olish:\n/apk_k1")

        elif text == "10-Sinf Informatika📘":
            await message.answer_document("https://t.me/baza_java_strong/4")

        elif text == "10-Sinf Ingliz Tili📘":
            await message.answer_document("https://t.me/baza_java_strong/5" )

        elif text == "10-Sinf Fizika📘":
            await message.answer_document("https://t.me/baza_java_strong/6",
                caption = "Fizika Kitob apk fayl olish:\n/apk_f1")

        elif text == "10-Sinf Geometriya📘":
            await message.answer_document("https://t.me/baza_java_strong/7",
                caption = "Geometriya Kitob apk fayl olish:\n/apk_g1")

        elif text == "10-Sinf Algebra📘":
            await message.answer_document("https://t.me/baza_java_strong/8",
                caption = "Algebra Kitob apk fayl olish:\n/apk_a1")

        elif text == "10-Sinf Geografiya📘":
            await message.answer_document("https://t.me/baza_java_strong/9",
                caption = "Geografiya Kitob apk fayl olish:\n/apk_g2")

        elif text == "10-Sinf Ona tili📘":
            await message.answer_document("https://t.me/baza_java_strong/20",
                caption = "Ona tili Kitob apk fayl olish:\n/apk_o1")

        elif text == "10-Sinf Kimyo Nazorat ishi📖":
            await message.answer_document("https://t.me/baza_java_strong/10")

                                                                    ## 9 - sinf

        elif text == "9-Sinf Fizika📘":
            await message.answer_document("https://t.me/baza_java_strong/65?single")

        elif text == "9-Sinf Rus tili📘":
            await message.answer_document("https://t.me/baza_java_strong/70?single")

        elif text == "9-Sinf Informatika📘":
            await message.answer_document("https://t.me/baza_java_strong/66?single")

        elif text == "9-Sinf Geometriya📘":
            await message.answer_document("https://t.me/baza_java_strong/67?single")

        elif text == "9-Sinf Algebra📘":
            await message.answer_document("https://t.me/baza_java_strong/68?single")

        elif text == "9-Sinf Geografiya📘":
            await message.answer_document("https://t.me/baza_java_strong/69?single")

        elif text == "9-Sinf Tarbiya📘":
            await message.answer_document("https://t.me/baza_java_strong/71?single")

                                                                                ##  8 - sinf

        elif text == "8-Sinf Ona tili📘":
            await message.answer_document("https://t.me/baza_java_strong/58?single")

        elif text == "8-Sinf Rus tili📘":
            await message.answer_document("https://t.me/baza_java_strong/61?single")

        elif text == "8-Sinf Informatika📘":
            await message.answer_document("https://t.me/baza_java_strong/55?single")

        elif text == "8-Sinf Geometriya📘":
            await message.answer_document("https://t.me/baza_java_strong/57?single")

        elif text == "8-Sinf Algebra📘":
            await message.answer_document("https://t.me/baza_java_strong/56?single")

        elif text == "8-Sinf Geografiya📘":
            await message.answer_document( "https://t.me/baza_java_strong/60?single" )

        elif text == "8-Sinf Tarbiya📘":
            await message.answer_document("https://t.me/baza_java_strong/59?single")

                                                                            ##  7- sinf

        elif text == "7-Sinf Biologiya📘":
            await message.answer_document("https://t.me/baza_java_strong/42?single")

        elif text == "7-Sinf Kimyo📘":
            await message.answer_document("https://t.me/baza_java_strong/39?single")

        elif text == "7-Sinf Informatika📘":
            await message.answer_document("https://t.me/baza_java_strong/38?single")

        elif text == "7-Sinf Ingliz Tili📘":
            await message.answer_document("https://t.me/baza_java_strong/45?single")

        elif text == "7-Sinf Fizika📘":
            await message.answer_document("https://t.me/baza_java_strong/37?single")

        elif text == "7-Sinf Geometriya📘":
            await message.answer_document("https://t.me/baza_java_strong/44?single" )

        elif text == "7-Sinf Algebra📘":
            await message.answer_document("https://t.me/baza_java_strong/41?single")

        elif text == "7-Sinf Geografiya📘":
            await message.answer_document("https://t.me/baza_java_strong/43?single")

        elif text == "7-Sinf Ona tili📘":
            await message.answer_document("https://t.me/baza_java_strong/47?single")

        elif text == "7-Sinf Musiqa📘":
            await message.answer_document("https://t.me/baza_java_strong/46?single" )

        elif text == "7-Sinf Rus tili📘":
            await message.answer_document("https://t.me/baza_java_strong/48?single")

        elif text == "7-Sinf Tasviriy san`at📘":
            await message.answer_document("https://t.me/baza_java_strong/49?single")

                                                                        ##    apk 10 - sinf

        elif text == "/apk_b1":
            await message.answer_document("https://t.me/baza_java_strong/12?single")

        elif text == "/apk_k1":
            await message.answer_document("https://t.me/baza_java_strong/16?single")

        elif text == "/apk_f1":
            await message.answer_document("https://t.me/baza_java_strong/13?single")

        elif text == "/apk_g1":
            await message.answer_document("https://t.me/baza_java_strong/15?single")

        elif text == "/apk_a1":
            await message.answer_document("https://t.me/baza_java_strong/11?single")

        elif text == "/apk_g2":
            await message.answer_document("https://t.me/baza_java_strong/14?single")

        elif text == "/apk_o1":
            await message.answer_document("https://t.me/baza_java_strong/17?single")

                                                                                ## hamma kitoblar 11-9-8-7

        elif text == "Hamma 11-sinf kitobni yuklash📚":
            await message.answer_document("https://t.me/baza_java_strong/87" )

        elif text == "Hamma 9-sinf kitobni yuklash📚":
            await message.answer_document("https://t.me/baza_java_strong/72" )

        elif text == "Hamma 8-sinf kitobni yuklash📚":
            await message.answer_document("https://t.me/baza_java_strong/62")

        elif text == "Hamma 7-sinf kitobni yuklash📚":
            await message.answer_document("https://t.me/baza_java_strong/93")

                                                                        ##  Kompyuter dasturlari-- asosiy bo`lim

        elif text == "Kompyuter Dasturlari🖥🛠" or text == "/pc_mexanics":
            await message.answer(text = "Siz asosiy menudasiz!👇", reply_markup = pc)

                                                                        ##  pc mexanics

        elif text == "Grafik dasturlar🎛":
            await message.answer(text = "Siz grafik dasturlar bo`limidasiz!", reply_markup = grafik_dasturlar)

        elif text == "Windows sistemalar✳️":
            await message.answer(text = "Windows turini Tanlang!👇\n‼️Windowslarni Rufus(Fleshkaga) yoki UltraIso(fleshka yoki diskka) dasturi orqali yoziladi‼️\nRufus va UltraIso asosiy menuda Windows yozish bo`limida!", reply_markup = windows_turlari)

        elif text == "Office dasturlar":
            await message.answer(text = "Office dasturlardan Tanlang!👇", reply_markup = office)

        elif text == "Video montaj dasturlar🎥":
            await message.answer(text = "Video montaj dasturlarini Tanlang!👇", reply_markup = video_montaj)

        elif text == "Orqaga🔧":
            await message.answer(text = "Windows turini Tanlang!👇\n‼️Windowslarni Rufus(Fleshkaga) yoki UltraIso(fleshka yoki diskka) dasturi orqali yoziladi‼️\nRufus va UltraIso asosiy menuda Windows yozish bo`limida!", reply_markup = windows_turlari)

        elif text == "Asosiy bo`lim💡":
            await message.answer(text = "Siz asosiy menudasiz!👇\nMaktab bo`limiga o`tish uchun /start bering!", reply_markup = pc)

        elif text == "🔙Orqaga⬅️":
            await message.answer(text = "Siz maktab darsliklari bo`limidasiz ➡️ Menuni Tanlang!👇", reply_markup = foydalanuvchilar)

                                                                        ## grafik dasturlar

        elif text == "3Ds Max":
            await message.answer_document(
                "https://t.me/baza_java_strong/109?single",
                caption = f"3Ds Max\n🗂Part 1\n\n{bot_linki}\n\n{kanal_link}")

            await message.answer_document(
                "https://t.me/baza_java_strong/110?single",
                caption = f"""3Ds Max\n🗂Part 2\n\n{bot_linki}\n\n{kanal_link}"""
            )
            await message.answer_document(
                "https://t.me/baza_java_strong/111?single",
                caption = f"""3Ds Max\n🗂Part 3\n\n{bot_linki}\n\n{kanal_link}"""
            )

            await message.answer_document(
                "https://t.me/baza_java_strong/112?single",
                caption = f"""3Ds Max\n🗂Part 4\n\n{bot_linki}\n\n{kanal_link}"""
            )

            await message.answer_document(
                "https://t.me/baza_java_strong/113",
                caption = f"""Autodesk Collection 2020 X-ForCe KeyGeN Activator\nLicense\n\n{bot_linki}\n\n{kanal_link}"""
            )

        elif text == "Unity Pro":
            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/242",
                caption = f"""Unity Pro\n🗂Part 1\n\n{bot_linki}\n\n{kanal_link}"""
            )

            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/243",
                caption = f"""Unity Pro\n🗂Part 2\n\n{bot_linki}\n\n{kanal_link}"""
            )

            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/244",
                caption = f"""Unity Pro\n🗂Part 3\n\n{bot_linki}\n\n{kanal_link}"""
            )

        elif text == "Corel Draw":
            await message.answer_document(
                "https://t.me/baza_java_strong/114",
                caption = f"""Corel Draw 2020 dasturi\nWindows x32/x64\n\n{bot_linki}\n\n{kanal_link}"""
            )

        elif text == "Blender dasturi":
            await message.answer_document(
                "https://t.me/baza_java_strong/115",
                caption = f"""Blender - bu bepul 3D grafik va animatsiya muharriri.\n3ds max qiladigan ishni blenderda ham qilsa bo`ladi\n💻 Windows 64 bit\n\n{bot_linki}\n\n{kanal_link}"""
            )

        elif text == "Adobe Photoshop Lightroom":
            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/327",
                caption = f"""🖥 Adobe Photoshop Lightroom\n⚙️ Password:  parol yo`q\n💾 Hajmi: 1.1gb \n🛡 Version: 8.4\n😀 x64 (64 bitlik)\n\n📝✅Photoshop bilan bellashadigan ranglar va slaydshovlar mutaxasisi\n⬇️Windows  8|8.1|10|11 da ishlaydi\n\n🎯 #lightroom #photoshoplight\n\n{bot_linki}\n\n{kanal_link}"""
            )

        elif text == "Adobe Photoshop":
            await message.answer_document(
                "https://t.me/baza_java_strong/117",
                caption = f"""🖥 Adobe Photoshop\n⚙️ Password:  parol yo`q\n💾 Hajmi: 1.8gb \n🛡 Version: 2019\n😀 x64 (64 bitlik)\n\n📝✅Adobe Photoshop Mukammal photo muxarriri\n⬇️Windows  8.1|10|11 da ishlaydi\n\n{bot_linki}\n\n{kanal_link}
                """
            )

                                                                        ## windows sistemalar
        
        elif text == "Game Windows🎮":
            await message.answer_document("BQACAgIAAxkBAAM_Y8WIk0I17y7138IxfPyNH7lquo8AAmkeAAL6umBITN7FLj0DzG4tBA",
            caption = f"""<b>Windows 10 Game Edition🎮</b>\n⚙️ Password:  parol yõq📢\n💾 Hajmi: 2.5 gb 😱\n👍 x64 (64 bitlik)\n🌎Language: english\n<b>🎮Windows 10 Home (Game Edition Lite os)🎮</b>\n\n📝Slabiy(kuchsiz) kompyuterlar uchun Maxsus windows 10 Game Edition Os operatsion tizimi. 2 gb ramliklarga ham zòr ishlaydi.. Ortiqcha programmalari õchirib tashlangan\n📹Windowsni tilini ozgartirish <a href='http://youtube.com/channel/UCKhQtK94Fh5RrxOzlKr6asQ'>youtube</a>  kanalimizda\n\n🎯 #win10game #win10gameedition #windows10 #windows10game #windows10gameedition  #win10 #win10liteos #os\n\n{bot_linki}\n\n{kanal_link}""")

        elif text == "Orginal Windowslar🤖":
            await message.answer(text = "Orginal Windowslarni Tanlang!👇\n‼️Windowslarni Rufus(Fleshkaga) yoki UltraIso(fleshka yoki diskka) dasturi orqali yoziladi‼️\nRufus va UltraIso asosiy menuda Windows yozish bo`limida!", reply_markup = windows_orginal)

        elif text == "LiteOs Windowslar🤖":
            await message.answer(text = "Yengil ishlaydigan lite os windowslarni Tanlang!👇\n‼️Windowslarni Rufus(Fleshkaga) yoki UltraIso(fleshka yoki diskka) dasturi orqali yoziladi‼️\nRufus va UltraIso asosiy menuda Windows yozish bo`limida!", reply_markup = windows_liteos)

                                                                        ## orginal windowslar

        elif text == "Windows 11":
            await message.answer_photo("https://t.me/baza_java_strong/94",
                caption = f"""Microsoft Windows 11\n\n📀 Razryadi: x64 bit\n🇷🇺 Tili: rus\n\nTizim talablari: CPU - 1ghz\nRAM - 4gb\nHDD - 64gb\nVideo - DirectX 12\nTPM- 2.0\n\nWindows 11 ning rasmiy versiyasi.\n#windows11\n{bot_linki}\n\n{kanal_link}\nparol: <pre>@ultrasoft_uz</pre>
                """)

            await message.answer_document("https://t.me/windowsuzprogrammaa/63",
                caption = """Windows 11\n\n📦1-qism
                """)

            await message.answer_document("https://t.me/windowsuzprogrammaa/64",
                caption = """Windows 11\n\n📦2-qism""")

            await message.answer_document("https://t.me/windowsuzprogrammaa/65",
                caption = f"""Windows 11\n\n📦3-qism\n\n{bot_linki}\n\n{kanal_link}""")

        elif text == "Windows 10":
            await message.answer_document("https://t.me/windowsuzprogrammaa/53",
                caption = f"""
📀 Windows 10 (v2004) RUS-ENG x86-x64 -28in1- HWID-act (AIO)   ✔️
🖥Платформа: 86x(32-bit)\64x(64-bit)
📦1-part

{bot_linki}\n\n{kanal_link}
parol: <pre>windowsuzprogramm</pre>
""")
            await message.answer_document("https://t.me/windowsuzprogrammaa/54",
                caption = f"""📀 Windows 10 (v2004) RUS-ENG x86-x64 -28in1- HWID-act (AIO)   ✔️
🖥Платформа: 86x(32-bit)\64x(64-bit)
📦2-part
{bot_linki}\n\n{kanal_link}
parol: <pre>windowsuzprogramm</pre>""")
            await message.answer_document("https://t.me/windowsuzprogrammaa/52",
                caption = f"""📀 Windows 10 (v2004) RUS-ENG x86-x64 -28in1- HWID-act (AIO)   ✔️
🖥Платформа: 86x(32-bit)\64x(64-bit)
📦3-part

parol: <pre>windowsuzprogramm</pre>
{bot_linki}\n\n{kanal_link}""")

        elif text == "Windows 8.1":
            await message.answer_document("https://t.me/windowsuzprogrammaa/45",
                caption = f"""\n📀Windоws 8.1 Professional VL with Update Оригинальные образы\n🖥Платформа: 86х(32-bit) \n📦1-part\n\n{bot_linki}\n\n{kanal_link}\nparol: <pre>windowsuzprogramm</pre>
                """)

            await message.answer_document("https://t.me/windowsuzprogrammaa/54",
                caption = f"""📀Windоws 8.1 Professional VL with Update Оригинальные образы\n🖥Платформа: 86х(32-bit) \n📦2-part\n\n{bot_linki}\n\n{kanal_link}\nparol: <pre>windowsuzprogramm</pre>""")

        elif text == "Windows 7":
            await message.answer_document("https://t.me/windowsuzprogrammaa/43",
                caption = f"""📀Оригинальные образы от Microsoft Windows 7 Home Basic with SP1\n🖥Платформа: 86х(32-bit)\n📦1-part\n\n{bot_linki}\n\n{kanal_link}\nparol: <pre>windowsuzprogramm</pre>
                """)

            await message.answer_document("https://t.me/windowsuzprogrammaa/54",
                caption = f"""📀Оригинальные образы от Microsoft Windows 7 Home Basic with SP1🖥Платформа: 86х(32-bit)\n📦2-part\n\n{bot_linki}\n\n{kanal_link}\nparol: <pre>windowsuzprogramm</pre>""")

                                                                        ## Liteos Windowslar

    #search_about
        elif text == "Windows 11 LiteOs":
            await message.answer_document("https://t.me/windowsuzprogrammaa/350",caption = f"""🔋 Windows 11 Ultra LiteOs\n🛠 Version: 22000.493\n⚙️ Password:  parol yõq\n💾 Hajmi: 1.4 gb 😱\n⌨️ x64 (64 bit)\n🌎Language: english\n\n📝✅Slabiy(kuchsiz) kompyuterlar uchun Maxsus windows 11 ultra lite os operatsion tizimi. 2 gb ramliklarga ham zòr ishlaydi.. Ortiqcha programmalari õchirib tashlangan\nWindowsni tilini ozgartirish youtube kanalimizda\n\n🎯  #win11ultra #win11ultraliteos #windows11  #win11 #win11liteos #os\nWindowsni tilini o`zgartirishni <a href="http://youtube.com/channel/UCKhQtK94Fh5RrxOzlKr6asQ">youtube</a> kanalimizdagi videodan topishingiz mumkin\n\n{bot_linki}\n\n{kanal_link}
                """)

        elif text == "Windows 10 LiteOs":
            await message.answer_document("BQACAgIAAxkBAANDY8WJKM5ko6n_lqQL06bdYFji7HcAAx8AAovhyUt9yxjMnkiRhy0E",
            caption = f"""🔋Windows 10 Home Nexus LiteOs\n⚙️ Password:  Parol yo`q\n💾 Hajmi: 2.6 gb \n🛡 Version: 21H2\n⌨️ x64 (64 bitlik)\n📝 ✅Slabiy(kuchsiz) kompyuterlar uchun Maxsus windows 10 lite os operatsion tizimi. Ortiqcha programmalari õchirib tashlangan\n\n🎯 #win10Nexus #win10Nexusos #windows10  #win10 #win10liteos\nWindowsni tilini o`zgartirishni youtube kanalimizdagi videodan topishingiz mumkin\n\n{bot_linki}\n\n{kanal_link}
                """)

        elif text == "Windows 8.1 LiteOs":
            await message.answer_document("BQACAgIAAxkBAANBY8WJChGQ3RKK2KcQylsfY4sMBIIAAusbAAKASLlLCsLVFM3I8rstBA",caption = f"""🔋Windows 8.1 Xtrame Lite Os Superlite\n⚙️ Password:  parol yo`q\n🧰 Hajmi: 2.6 gb\n⌨️ x64 (64 bitlik)\n\n📝 ✅Slabiy(kuchsiz) kompyuterlar uchun Maxsus windows 8.1 lite os operatsion tizimi. Ortiqcha programmalari õchirib tashlangan\n\n🎯 #win8_1xtrame #win8_1Xtrameos #windows8_1 #win8_1 #win8_1liteos\nWindowsni tilini o`zgartirishni youtube kanalimizdagi videodan topishingiz mumkin\n\n{bot_linki}\n\n{kanal_link}
                """)

        elif text == "Windows 7 LiteOs":
            await message.answer_document("https://t.me/windowsuzprogrammaa/330",
                caption = f"""🔋Windows 7 Xtreme LiteOs\n⚙️ Password:  WPC-7\n💾 Hajmi: 1.7 gb 😱\n👍 x64 (64 bitlik)\n🌎 Language: english\n\n📝 ✅Slabiy(kuchsiz) kompyuterlar uchun Maxsus windows 7 lite os operatsion tizimi. Ortiqcha programmalari õchirib tashlangan\n\n🎯 #win7Xtrame #win7xtreme #windows7  #win7 #win7liteos\nWindowsni tilini o`zgartirishni youtube kanalimizdagi videodan topishingiz mumkin\n\n{bot_linki}\n\n{kanal_link}
                """)

                                                                        ## Video montaj

        elif text == "Adobe Premiere Pro":
            await message.answer_document(
                "https://t.me/baza_java_strong/116",
                caption = f"""Premiere Pro - bu televideniya va film uchun video-tahrirlash sohasidagi yetakchi dastur. Ijodiy vositalar, boshqa dasturlar va xizmatlar bilan integratsiya, filmlar va videofilmlarda kadrlar tayyorlashda yordam beradi.

Minimal tizim talablari:

Protsessor: Intel® 6- chi  avlod yoki undan yuqori - yoki AMD Ryzen ™ 1000 yoki undan yuqori 
Operatsion tizim: Microsoft Windows 10 (64-bit)
RAM: 8 GB
Video karta: 2 GB GPU VRAM
Qattiq diskdagi bo'sh joy: 8GB
Monitor o'lchamlari:1280 x 800

{bot_linki}\n\n{kanal_link}"""
        )

        elif text == "Adobe after effects":
            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/278",
                caption = f"""<b>After Effects yordamida yaratib bo'lmaydigan narsa yo'q.</b>

Kinematik filmlarning sarlavhalarini, kirish so'zlarini va o'tish joylarini yarating. Obyektni klipdan olib tashlang. Olovni yoqing yoki yomg'ir yog'diring. Logotip yoki belgini jonlantirish. Hatto 3D maydonida harakatlaning va dizayn qiling.

Tizim talablari: Windows 10 32/64 bit
OZU DDR4 8GB, CPU Core i5 7gen+, Grafik karta 2GB, HDD 1TB, SSD 250GB
Yili: 2020-yil
Turi: Repack
Hajmi: 1130.9 MB

{bot_linki}\n\n{kanal_link}"""
        )

        elif text == "Proshow Producer Pro":
            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/335",
                caption = f"""<b>Proshow Producer Pro</b>
©️ Proshow Producer 
⚙️ Password:<pre>sh093352300</pre>
💾 Hajmi: 66 mb
🛡 Version: 9.0

📝✅ Proshow producer rasmlarni pro darajasida tayyorlaydigan dastur videolarni ham tayyorlaydi
⬇️Windows  7|8|8.1|10|11

🎯 #proshow #proshow_producer #proshowproducer #photoedit

{bot_linki}\n\n{kanal_link}"""
        )

        elif text == "Edius 8.53":
            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/98",
                caption = f"""<b>Edius 8.53</b>
Edius 8.5  professional video muharriri . Bu programmani kôp video montajchilar ishlatishadi.

{bot_linki}\n\n{kanal_link}"""
            )
            await message.answer_document("https://t.me/windowsuzprogrammaa/103", caption = f"Ediusni  8.53 aktivlashtirish videosi!!\nVideo xira chiqdi lekin kõrsa bõladi. Muammolar uchun uzr sõrayman.\n☢️ parol: @windowsuzprogrammaa\n\n{bot_linki}\n{kanal_link}")

                                                                        ## Office dasturlar

        elif text == "Office activator":
            await message.answer_document(
                "https://t.me/baza_java_strong/104", 
                caption = f"""KMS Matrix - bu Windows va Office dasturlarini tezda faollashtiradigan oddiy aktivator.

Faollashtira oladi:
• Windows: 7, 8, 8.1, 10
• Ofis: 2010, 2013, 2016, 2019.

Ushbu versiya haqida
📁 toifasi: #aktivatsiya
🆚 Versiya: v5.5
🖥 OS: Windows
📀 OS Razryadi: x86 / x64
🇷🇺 Interfeys tili: ingliz tili
🔑 Aktivatsiya: talab qilinmaydi

{bot_linki}\n\n{kanal_link}""")

        elif text == "Office 2016":
            await message.answer_document(
                "https://t.me/baza_java_strong/98",
                caption = f"""Mana sizlarga mahsus Microsoft Office 2016 dasturi maqulini yuklab oling! 

{bot_linki}\n\n{kanal_link}"""
            )

        elif text == "Office 2019":
            await message.answer_photo(
                "https://t.me/baza_java_strong/101",
                caption = f"""
Microsoft office 2019

Word, excel, power point, outlook express kabi offis dasturlari mavjud.

Pastdagi 2ta faylni ham yuklab olish shart, shundagina kompyuteringizga o'rnata olasiz!!!

Windows 7|10| 64 - bit

{bot_linki}\n\n{kanal_link}
parol: <pre>@UltraSoft_uz</pre>
            """
            )
            await message.answer_document(
                "https://t.me/baza_java_strong/99?single",
                caption = f"""Microsoft office 2019
📦1-qism

{bot_linki}\n\n{kanal_link}
parol: <pre>@UltraSoft_uz</pre>
"""
        )
            await message.answer_document(
                "https://t.me/baza_java_strong/100?single",
                caption = f"""Microsoft office 2019
📦2-qism

{bot_linki}\n\n{kanal_link}
parol: <pre>@UltraSoft_uz</pre>
"""
        )

        elif text == "Office 2021":
            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/167",
                caption = f"""💾 Microsoft Office 2021 LTSC Professional Plus 16.0.14332.20176 RePack by MLRY
☑️
🖥 Системные требования:ОС: Windows 10 (32/64 bit)

#MSOffice #Word #Excel #Visio #Project #PowerPoint #Office #Офис #Microsoft #Office2021 #Pro #Редактор
📦1-part

{bot_linki}\n\n{kanal_link}"""
            )
            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/167",
                caption = f"""💾 Microsoft Office 2021 LTSC Professional Plus 16.0.14332.20176 RePack by MLRY
☑️
🖥 Системные требования:ОС: Windows 10 (32/64 bit)

#MSOffice #Word #Excel #Visio #Project #PowerPoint #Office #Офис #Microsoft #Office2021 #Pro #Редактор
📦2-part

{bot_linki}\n\n{kanal_link}"""
        )

        elif text == "WPS office":
            await message.answer_document(
                "https://t.me/baza_java_strong/103",
                caption = f"""WPS Office dasturining Kompyuter versiyasi.

WPS Office - bu matnlarni yoki elektron jadvallarni yozish va tahrirlash uchun bepul dasturlar to'plami. 

{bot_linki}\n\n{kanal_link}"""
            )

        elif text == "Office 2013":
            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/70",
                caption = f"""Microsoft Office 2013 x64

Marhamat yuklab olishingiz mumkin!
#office #office2013 #word #exel #powerpoint 

{bot_linki}\n\n{kanal_link}"""
        )

                                                        ## Aktivator

        elif text == "Aktivator⚡️":
            await message.answer_document(
                "https://t.me/baza_java_strong/104",
                caption = f"""🔐 Windows 11 Uchun Активатор.

💾 Fayl hajmi: 4 MB.

📝 Izoh: Ushbu dastur yordamida Windows 11 tizimini aktivatsiya qilishingiz mumkin.
kopincha qolgan windowslarni ham qilsa bo`ladi


•┈•┈•┈•┈•❁✿❁•┈•┈•┈•┈•
#aktivator
📢Bizning kanal:
{bot_linki}\n\n{kanal_link}
            """
            )

                                                    ## arxiv dasturlar

        elif text == "Arxiv dasturlar📚":
            await message.answer_document(
                "https://t.me/baza_java_strong/107",
                caption = f"""7-Zip x64

ℹ️ 7-Zip - bu Windows uchun ajoyib arxivlovchi, uning afzalliklari qulay tezlik, barcha zamonaviy formatlarni qo'llab-quvvatlash va yuqori siqishni nisbati yaxshiroq.

{bot_linki}\n\n{kanal_link}"""
        )
            await message.answer_document(
                "https://t.me/baza_java_strong/108",
                caption = f"""WinRAR 5.71

ℹ️ Arxiv bilan ishlash uchun WinRAR dasturi. x32 (x86) razryadli kompyuterlar uchun.

{bot_linki}\n\n{kanal_link}
            """
            )

                                                            ## Converter

        elif text == "Converter dasturi🔄":
            await message.answer_document(
                "https://t.me/windowsuzprogrammaa/336",
                caption = f"""🛒HD Video Converter Factory Pro
⚙️ Password:  parol yo`q
💾 Hajmi: 93 mb 
👍 x64 (64 bitlik)

📝✅Xohlagan video,rasm, muzika va hokazilarni converter qiladigan va internetdan fayl yuklaydigan qoshimcha funksiyalari kop dastur
⬇️Windows  7|8|8.1|10|11 da ishlaydi

{bot_linki}\n\n{kanal_link}
""")

                                                            ## windows yozish

        elif text == "Windowslarni yozish📀📼":
            await message.answer_document(
                "https://t.me/baza_java_strong/105",
                caption = f"""<b>UltraIso</b>
Bu dastur yordamida windowsni fleshkaga📼 yoki diskka📀 yozsangiz bo`ladi

🖥 Kompyuterlar  kanaliga ulanish uchun:
📢Bizning kanal:
{bot_linki}\n\n{kanal_link}
            """
        )
            await message.answer_document(
                "https://t.me/baza_java_strong/106",
                caption = f"""💾 <b>Rufus 3.10 (Build 1642) Beta Portable</b>☑️
🖥 Windowslarni fleshkaga yozadigan dastur📼 (x32\ x64-bit)

🖥 Kompyuterlar  kanaliga ulanish uchun:
📢Bizning kanal:
{bot_linki}\n\n{kanal_link}
            """
        )

        elif text == "🔐 Windows 10 hack password":
            await message.reply_document(document = "https://t.me/windowsuzprogrammaa/320", caption = f"🖼 Videoni oxirigacha ko`ring birinchi\nshoshilib ishni boshlamang kerakli narsalarni olib keyin boshlashni maslahat beramiz\n100% Working✅\n🛡Video HD formatda\n🎯 #Passwordbreak #password #parolbuzish\n#windowspassword\n\n{bot_linki}\n{kanal_link}\n\n/hajmi_kichik_video")

        elif text == "/hajmi_kichik_video":
            await message.reply_document(document = "https://t.me/windowsuzprogrammaa/321", caption = f"🖼 Videoni oxirigacha ko`ring birinchi\nshoshilib ishni boshlamang kerakli narsalarni olib keyin boshlashni maslahat beramiz\n100% Working✅\n🛡Video HD formatda\n🎯 #Passwordbreak #password #parolbuzish\n#windowspassword\n\n{bot_linki}\n{kanal_link}")
                                                                        ## BOOKNOMY -- asosiy bo`lim`

        elif text == "🎧Booknomy kitoblar🎧":
            await message.answer(text = "Siz <b>Booknomy</b> bo`limidasiz tilni tanlang!👇", reply_markup = booknomy)
        
                                                                ## booknomy -- in
        elif text == "🏴󠁧󠁢󠁥󠁮󠁧󠁿Ingliz tili📕🎧":
            await message.answer_document("https://t.me/baza_java_strong/23?single")
            await message.answer_document("https://t.me/baza_java_strong/24?single")
            await message.answer_document("https://t.me/baza_java_strong/25?single")
            await message.answer_document("https://t.me/baza_java_strong/26?single")
            await message.answer_document("https://t.me/baza_java_strong/27?single")
            await message.answer_document("https://t.me/baza_java_strong/28?single")

        elif text == "🇰🇷Koreys tili📗🎧":
            await message.answer_document("https://t.me/baza_java_strong/89?single" )
            await message.answer_document("https://t.me/baza_java_strong/90?single")

        elif text == "🇷🇺Rus tili📘🎧":
            await message.answer_document("https://t.me/baza_java_strong/32?single")
            await message.answer_document("https://t.me/baza_java_strong/33?single")


        else:
            await message.reply(text = F"<b>Botda ** {text} ** buyrug`i topilmadi!</b>\n⚙️Berilgan parametrlardan birini tanlang!\n🎛Menyudan foydalaning yoki /help 🆘tugmasini bosing!")

    else:
        if text in muloqot:
            await message.reply(text = "📁 <b>Hamma fayllarni 🔐paroli o`sha faylni pastiga yozib qo`yilgan..</b>\nAgar yozilmagan bo`lsa, Buni sinab ko`ring: <pre>@windowsuzprogrammaa</pre> yoki <pre>@windowsuzprogramm</pre>\n\n<b>Shularda ham xatolik bersa /admin bilan bog`laning </b>‼️")

        elif text in  muloqot2:
            await message.reply(text = "🤔 <b>Muammolaringiz bo`lsa screenshot qilib tashlasangiz tezroq muammoyizga yechim topasiz </b>😉")

        elif text in muloqot3:
            await message.reply(text = "<b>Birorta Programma yoki dastur kerak bo`lsa 🧑🏼‍💻 adminga yozavering(/admin)</b>")
        
        else:
            pass

@dp.message_handler(state = Admin_manager.admin_qosh)      # admin qoshish
async def admin_qoshish(message: types.Message, state: FSMContext):
    text: str = message.text
    if text != 'Orqaga🔝' and text.isnumeric():
        txt = int(text)
        if is_admin(txt):
            if not(db.is_user(text)):
                await message.reply(text = f"{txt} -- Siz kiritgan ID raqam <b>obunachilaringiz orasida yo`q!!</b>", reply_markup = admin_min_plus)
                await state.finish()
            else:
                await message.reply(text = f'{txt} ushbu id adminlar orasida mavjud!!', reply_markup = admin_min_plus)
                await state.finish()

        else:
            if 99999999 < txt and db.is_user(txt):
                db.admin_plus(txt)
                await bot.send_message(chat_id = txt, text = 'Tabriklaymiz siz ushbu botga <b>Administrator</b> bo`ldingiz!🥳🥳', reply_markup = Admin)
                await message.answer(text = 'Admin qo`shish muvaffaqiyatli amalga oshdi✅', reply_markup = admin_min_plus)
                await state.finish()
            else:
                await message.reply(text = "🆔 raqam xato kiritildi..! yoki bot foydalanuvchilari orasida topilmadi")
                await state.finish()

    elif text == "Orqaga🔝":
        await state.finish()
        await message.reply(text = "Jarayon tugadi.. Orqaga qaytdingiz.", reply_markup = Admin)

    elif not(text.isnumeric()):
        await state.finish()
        await message.reply(text = "ID raqamda harflar bo`lmaydi‼️", reply_markup = admin_min_plus)

    else:
        await message.reply(text = 'Siz asosiy menyudasiz', reply_markup = Admin)


@dp.message_handler(state = Admin_manager.users_text, content_types = ContentType.TEXT)  ##  users uchun id olish
async def write(message: types.Message, state: FSMContext):
    text = message.text
    if text.isdigit():
        txt = int(text)
        if db.is_user(txt):
            await state.update_data(id_raqam = txt)
            await message.answer(text = "🆔 raqam saqlandi ✅\nEndi 📝 <b>Yozmoqchi bo`lgan textni kiriting:</b>", reply_markup = orqaga)
            await Admin_manager.foy_text.set()
        else:
            await message.reply(text = f"<b>** {txt} ** siz bazada yo`q odamni kiritdingiz</b> ‼️", reply_markup = Admin)
            await state.finish()
    
    elif text == "Orqaga🔝":
        await message.reply(text = "Jarayon yakunlandi..! Orqaga aytdingiz.", reply_markup = Admin)
        await state.finish()

    else:
        await message.reply(text = "Jarayon yakunlandi..! Orqaga aytdingiz.", reply_markup = Admin)
        await state.finish()


@dp.message_handler(state = Admin_manager.channel_add)                        # kanal qoshish
async def chanel_plus(message: types.Message, state: FSMContext):
    text: str = message.text
    if text.startswith("-"):
        if text[1:].isdigit():
            txt: int = int(text)
            if (txt < 0) and (-99999999999 > txt):
                try:
                    db.channel_plus(txt)
                    await message.reply(text = "Kanal ➕qo`shish <b>muvaffaqiyatli amalga oshdi</b>✅", reply_markup = admin_min_plus)
                    await state.finish()
                except:
                    await message.reply(text = "<b>Kanalga botni qo`shib admin qiling!!</b>", reply_markup = admin_min_plus)
                    await state.finish()
            else:
                await state.finish()
                await message.reply(text = f"<b>ID raqam ** +{txt} ** Musbat ishorali bo`lmaydi ‼️", reply_markup = admin_min_plus)

        else:
            await state.finish()
            await message.reply(text = f"<b>Siz ** {text} ** 🆔 raqam harflar bilan bo`lmaydi va Musbat ishorali bo`ladi </b>‼️", reply_markup = admin_min_plus)

    elif text == "Orqaga🔝":
        await state.finish()
        await message.reply(text = "Jarayon yakunlandi..! Orqaga qaytdingiz.", reply_markup = admin_min_plus)

    else:
        await state.finish()
        await message.reply(text = "ID raqamda harflar bo`lmaydi‼️", reply_markup = admin_min_plus)


@dp.message_handler(state = Admin_manager.foy_text, content_types = ContentType.TEXT)  ## userga yozish
async def foy_text(message: types.Message, state: FSMContext):
    try:
        if message.text != "Orqaga🔝":
            data = await state.get_data()
            id_num = data.get('id_raqam')
            await bot.send_message(chat_id = id_num, text = f"Sizga 👤admindan xabar keldi:\n\n{message.text}", entities = message.entities, reply_markup = Admin)
            await message.reply(text = f"<a href = 'tg://user?id={id_num}'>Foydalanuvchiga</a> muvaffaqiyatli yuborildi✅", reply_markup = Admin)
            await state.finish()
        else:
            await message.reply(text = "Jarayon yakunlandi..! Orqaga qaytdingiz.", reply_markup = Admin)
            await state.finish()
    except:
        await message.answer(text = "Siz yuborgan xabar foydalanuvchiga yetib bormadi..\n<b>Sababi u botni bloklagan</b>", reply_markup = Admin)

@dp.callback_query_handler(bot_post.filter(action = 'ishla'))
async def found(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer(text = 'ID topish ilovasi ishlashni boshladi!')
    await callback.message.answer(text = "<b>Topmoqchi bo`lgan telegram foydalanuvchisining [Telegram ID] raqamini kiriting:</b>", reply_markup = orqaga)
    await Admin_manager.odam_topish.set()

@dp.message_handler(state = Admin_manager.odam_topish, content_types = ContentType.TEXT)
async def not_found(message: types.Message, state: FSMContext):
    msg = message.text
    if (msg != 'Orqaga🔝') and (msg.isnumeric()):
        msg = int(msg)
        if msg > 99999999:
            await state.update_data({'foydalanuvchi_id': msg})
            data: dict = await state.get_data()
            await message.reply(text = f"<a href = 'tg://user?id={data.get('foydalanuvchi_id')}'>Foydalanuvchi</a> 👈🏻<b>Ko`rish uchun ustiga bosing!</b>\n\n/id_orqali_topish", reply_markup = keyboard)
            await state.finish()
        else:
            await message.reply(text = "<b>Kiritilgan ID raqam telegramda Topilmadi‼️</b>\n\n/id_orqali_topish", reply_markup = keyboard)
            await state.finish()

    elif msg == 'Orqaga🔝':
        await message.reply(text = 'Bekor qilindi!', reply_markup = keyboard)
        await state.finish()

    else:
        await message.reply(text = f"<b>{msg}</b> -- Ushbu ID raqamiga tegishli Telegram Foydalanuvchisi topilmadi\n‼️<b>ID raqan xato bo`lishi mumkin</b>‼️\n\n/id_orqali_topish",reply_markup = keyboard)
        await state.finish()

@dp.callback_query_handler(for_delete.filter())
async def udalit(call: types.CallbackQuery, callback_data: dict):
    id = callback_data.get('id')
    id = int(id)
    need_admin = for_delete_user.get('admin')
    need_kanal = for_delete_user.get('kanal')

    try:
        if not(need_kanal is None):
            channel = await bot.get_chat(db.get_malumot(id))
            await call.answer(text = f"{channel.title} -- shu kanal botdan olib tashlandi!", show_alert = True)
            db.get_malumot_del(id)
            await call.message.delete()

        elif not(need_admin is None) and id != 1:
            await call.answer(text = f"{db.get_admin(id)} -- shu raqamli admin lavozimidan olib tashlandi!", show_alert = True)
            db.del_admin(id)
            try:
                await bot.send_message(chat_id = db.get_admin(id), text = f"Siz <b>Administrator</b> lavozimidan bo`shatildingiz😒", reply_markup = keyboard)
                await call.message.delete()
            except:
                await call.message.answer(text = f"<b> ** {db.get_admin(id)} **</b> Ushbu ID raqami bot foydalanuvchilari orasida topilmadi!")
                await call.message.delete()

        elif need_kanal is None and id != id:
            await call.answer(text = "Botga eng kamida 1 ta kanal ulangan bo`lishi kerak 😉", show_alert = True)
            await call.message.delete()

        elif need_admin is None and id != id:
            await call.answer(text = "Avval admin o`chirish bo`limiga kirib keyin qayta urinib ko`ring! 😉", show_alert = True)
            await call.message.delete()
        
        elif  (need_admin is None) and (need_kanal is None) and (id > 1):
            await call.answer(text = "Siz o`chirilgan ma`lumotni qayta o`chirolmaysiz ‼️", show_alert = True)
            await call.message.delete()
        else:
            await call.answer(text = "Siz Bot yaratuvchisini o`chirib tashlayolmaysiz! 😡", show_alert = True)
            await call.message.delete()
    except:
        await call.answer(text = "Admin menejer bo`limiga kirib qayta urining ‼️", show_alert = True)
        await call.message.delete()

