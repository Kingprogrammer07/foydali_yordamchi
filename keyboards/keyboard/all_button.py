from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

Admin = ReplyKeyboardMarkup(
    keyboard = [[
            KeyboardButton(text = "👤Foydalanuvchi bo`limi👥"), 
            KeyboardButton(text = "📎Yangi post✏️"),
        ],
        [
            KeyboardButton(text = 'Admin menejer🎛')
        ],
        [
            KeyboardButton(text = "Statistika📶"),
            KeyboardButton(text = "Foydalanuvchilarga yozish"),
        ],
        ], 
        resize_keyboard = True, 
        # one_time_keyboard = True
        )

havola = InlineKeyboardMarkup(row_width = 1).add(InlineKeyboardButton(text = "👨‍💻Admin👨‍💻", url = "https://t.me/java_strong"))

keyboard = ReplyKeyboardMarkup(
    keyboard = [[
            KeyboardButton(text = "📚Maktab darsliklari📚"), 
            KeyboardButton(text ="🎧Booknomy kitoblar🎧")
        ],
        [
            KeyboardButton(text = "Kompyuter Dasturlari🖥🛠"),
            KeyboardButton(text = "🆔 orqali topish"),
        ],
        [
            KeyboardButton(text = "📹 Video yuklash"),
        ],
        [
            KeyboardButton(text = "Qo`llanma📃"), 
            KeyboardButton(text = "Statistika📶"),
            KeyboardButton(text = "Taklif")
        ]], 
        resize_keyboard = True, 
        # one_time_keyboard = True
        )

foydalanuvchilar = ReplyKeyboardMarkup(row_width=2, resize_keyboard = True)
foydalanuvchilar.row(
    KeyboardButton(text = "PDF ochadigan dastur(apk) va (exe)🎛")
)
foydalanuvchilar.add(
            KeyboardButton(text ="📚11-Sinf darsliklar📚"),
            KeyboardButton(text = "📚10-Sinf yangi darsliklar📚"), 
            KeyboardButton(text ="📚9-Sinf darsliklar📚"),
            KeyboardButton(text = "📚8-Sinf darsliklar📚"), 
            KeyboardButton(text ="📚7-Sinf yangi darsliklar📚"),
            KeyboardButton(text ="Asosiy Bo`lim⬅️")
)

sinf11 = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "PDF ochadigan dastur(apk) va (exe)🎛")
        ],
        [
            KeyboardButton(text = "11-Sinf Matematika 1-qism📘"), 
            KeyboardButton(text ="11-Sinf Adabiyot 1-qism📘")
        ],
        [
            KeyboardButton(text = "11-Sinf Adabiyot 2-qism📘"), 
            KeyboardButton(text = "11-Sinf Kimyo📘")
        ],
        [
            KeyboardButton(text = "11-Sinf Rus tili📘"), 
            KeyboardButton(text ="Hamma 11-sinf kitobni yuklash📚")
        ],
        [
            KeyboardButton(text = "🔙Orqaga⬅️"), 
            KeyboardButton(text = "Asosiy Bo`lim⬅️")
        ]
        ], 
        resize_keyboard = True, 
        # one_time_keyboard = True
        )

sinf10 = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "PDF ochadigan dastur(apk) va (exe)🎛")
        ],
        [
            KeyboardButton(text = "10-Sinf Ona tili📘"), 
            KeyboardButton(text ="10-Sinf Biologiya📘")
        ],
        [
            KeyboardButton(text = "10-Sinf Kimyo📘"), 
            KeyboardButton(text = "10-Sinf Informatika📘")
        ],
        [
            KeyboardButton(text = "10-Sinf Ingliz Tili📘"), 
            KeyboardButton(text ="10-Sinf Fizika📘")
        ],
                [
            KeyboardButton(text = "10-Sinf Geometriya📘"), 
            KeyboardButton(text ="10-Sinf Algebra📘")
        ],
        [
            KeyboardButton(text = "10-Sinf Geografiya📘"), 
            KeyboardButton(text ="10-Sinf Kimyo Nazorat ishi📖")
        ],
        [
            KeyboardButton(text = "🔙Orqaga⬅️"), 
            KeyboardButton(text = "Asosiy Bo`lim⬅️")
        ]
        ], 
        resize_keyboard = True, 
        # one_time_keyboard = True
        )

sinf9 = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "PDF ochadigan dastur(apk) va (exe)🎛")
        ],
        [
            KeyboardButton(text = "9-Sinf Informatika📘"), 
            KeyboardButton(text ="9-Sinf Tarbiya📘")
        ],
        [
            KeyboardButton(text = "9-Sinf Fizika📘"), 
            KeyboardButton(text = "9-Sinf Geometriya📘")
        ],
        [
            KeyboardButton(text = "9-Sinf Algebra📘"), 
            KeyboardButton(text ="9-Sinf Geografiya📘")
        ],
                [
            KeyboardButton(text = "9-Sinf Rus tili📘"), 
        ],
        [
            KeyboardButton(text = "Hamma 9-sinf kitobni yuklash📚"), 
        ],
        [
            KeyboardButton(text = "🔙Orqaga⬅️"), 
            KeyboardButton(text = "Asosiy Bo`lim⬅️")
        ]
        ], 
        resize_keyboard = True, 
        # one_time_keyboard = True
        )

sinf8 = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "PDF ochadigan dastur(apk) va (exe)🎛")
        ],
        [
            KeyboardButton(text = "8-Sinf Ona tili📘"), 
            KeyboardButton(text ="8-Sinf Rus tili📘")
        ],
        [
            KeyboardButton(text = "8-Sinf Informatika📘"), 
            KeyboardButton(text = "8-Sinf Tarbiya📘")
        ],
        [
            KeyboardButton(text = "8-Sinf Geometriya📘"), 
            KeyboardButton(text ="8-Sinf Algebra📘")
        ],
        [
            KeyboardButton(text = "8-Sinf Geografiya📘"),
        ],
        [ 
            KeyboardButton(text ="Hamma 8-sinf kitobni yuklash📚")
        ],
        [
            KeyboardButton(text = "🔙Orqaga⬅️"), 
            KeyboardButton(text = "Asosiy Bo`lim⬅️")
        ]
        ], 
        resize_keyboard = True, 
        # one_time_keyboard = True
        )

sinf7 = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "PDF ochadigan dastur(apk) va (exe)🎛")
        ],
        [
            KeyboardButton(text = "7-Sinf Ona tili📘"), 
            KeyboardButton(text ="7-Sinf Biologiya📘")
        ],
        [
            KeyboardButton(text = "7-Sinf Kimyo📘"), 
            KeyboardButton(text = "7-Sinf Informatika📘")
        ],
        [
            KeyboardButton(text = "7-Sinf Ingliz Tili📘"), 
            KeyboardButton(text ="7-Sinf Fizika📘")
        ],
                [
            KeyboardButton(text = "7-Sinf Geometriya📘"), 
            KeyboardButton(text ="7-Sinf Algebra📘")
        ],
        [
            KeyboardButton(text = "7-Sinf Geografiya📘"), 
            KeyboardButton(text ="7-Sinf Musiqa📘")
        ],
        [
            KeyboardButton(text = "7-Sinf Tasviriy san`at📘"), 
            KeyboardButton(text ="7-Sinf Rus tili📘")
        ],
        [
            KeyboardButton(text = "Hamma 7-sinf kitobni yuklash📚")
        ],
        [
            KeyboardButton(text = "🔙Orqaga⬅️"), 
            KeyboardButton(text = "Asosiy Bo`lim⬅️")
        ]
        ], 
        resize_keyboard = True, 
        # one_time_keyboard = True
        )

pc = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
pc.insert(
    KeyboardButton("🔐 Windows 10 hack password")
)
pc.add(
    KeyboardButton("Windows sistemalar✳️"),
    KeyboardButton("Office dasturlar"),
    KeyboardButton("Grafik dasturlar🎛"),
    KeyboardButton("Video montaj dasturlar🎥"),
    KeyboardButton("Aktivator⚡️"),
    KeyboardButton("Arxiv dasturlar📚"),
    KeyboardButton("Converter dasturi🔄"),
    KeyboardButton("Windowslarni yozish📀📼")
)
pc.row(
    KeyboardButton("Asosiy Bo`lim⬅️")
)

grafik_dasturlar = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
grafik_dasturlar.add(
    KeyboardButton("Adobe Photoshop"),
    KeyboardButton("Blender dasturi"),
    KeyboardButton("3Ds Max"),
    KeyboardButton("Corel Draw"),
    KeyboardButton("Adobe Photoshop Lightroom"),
    KeyboardButton("Unity Pro")
)
grafik_dasturlar.row(
    KeyboardButton("Asosiy bo`lim💡")
)

calcel = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
calcel.add(KeyboardButton("Orqaga qaytish"))

video_montaj = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
video_montaj.add(
    KeyboardButton("Adobe Premiere Pro"),
    KeyboardButton("Adobe after effects"),
    KeyboardButton("Edius 8.53"),
    KeyboardButton("Proshow Producer Pro"),
)
video_montaj.row(
    KeyboardButton("Asosiy bo`lim💡")
)

office = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
office.add(
    KeyboardButton("Office 2013"),
    KeyboardButton("Office 2019"),
    KeyboardButton("Office 2016"),
    KeyboardButton("Office 2021"),
    KeyboardButton("WPS office"),
    KeyboardButton("Office activator"),
)
office.row(
    KeyboardButton("Asosiy bo`lim💡")
)

windows_orginal = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
windows_orginal.add(
    KeyboardButton("Windows 11"),
    KeyboardButton("Windows 10"),
    KeyboardButton("Windows 8.1"),
    KeyboardButton("Windows 7"),
    KeyboardButton("Orqaga🔧"),
    KeyboardButton("Asosiy bo`lim💡")
)

windows_liteos = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
windows_liteos.add(
    KeyboardButton("Windows 11 LiteOs"),
    KeyboardButton("Windows 10 LiteOs"),
    KeyboardButton("Windows 8.1 LiteOs"),
    KeyboardButton("Windows 7 LiteOs"),
    KeyboardButton("Orqaga🔧"),
    KeyboardButton("Asosiy bo`lim💡")
)

windows_turlari = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
windows_turlari.add(
    KeyboardButton("Orginal Windowslar🤖"),
    KeyboardButton("LiteOs Windowslar🤖"),
    KeyboardButton("Game Windows🎮")
)
windows_turlari.row(
    KeyboardButton("Asosiy bo`lim💡")
)

booknomy = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
booknomy.add(
            KeyboardButton(text = "🏴󠁧󠁢󠁥󠁮󠁧󠁿Ingliz tili📕🎧"), 
            KeyboardButton(text = "🇷🇺Rus tili📘🎧"), 
            KeyboardButton(text ="🇰🇷Koreys tili📗🎧"),
            KeyboardButton(text ="Asosiy Bo`lim⬅️")
)

admin_min_plus = ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
admin_min_plus.add(
    KeyboardButton(text = "Admin qo`shish➕"),
    KeyboardButton(text = "Adminni olib tashlash➖"),
    KeyboardButton(text = "Kanal qo`shish➕"),
    KeyboardButton(text = "Kanalni olib tashlash➖"),
    KeyboardButton(text = 'Admin asosiy')
)

orqaga = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1).add(KeyboardButton(text = 'Orqaga🔝'))
