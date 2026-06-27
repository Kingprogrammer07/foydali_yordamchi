"""Statik kontent katalogi — tugma matni -> yuboriladigan fayllar.

creator.py'dagi ulkan if/elif zanjiri shu yerga data sifatida ajratildi.
books.py va software.py shu lug'atdan generic yuboradi.

Item.method: "document" | "photo"
Item.file:   Telegram URL (t.me/...) yoki file_id
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    method: str
    file: str
    caption: str | None = None


bot_linki = "🤖<a href='https://t.me/foydali_dastur_kitobbot'>Foydali yordamchi [PC Mexanics]</a>"
kanal_link = (
    "<a href='https://t.me/windowsuzprogrammaa'>📲Telegram</a> | "
    "<a href='https://www.instagram.com/invites/contact/?i=m95peeh67d9u&utm_content=o9912bw'>📷instagram</a> | "
    "<a href='http://youtube.com/channel/UCKhQtK94Fh5RrxOzlKr6asQ'>🎥Youtube</a>"
)

_FOOTER = f"\n\n{bot_linki}\n\n{kanal_link}"


def _doc(url: str, caption: str | None = None) -> Item:
    return Item("document", url, caption)


def _photo(url: str, caption: str | None = None) -> Item:
    return Item("photo", url, caption)


# ── MAKTAB DARSLIKLARI (books.py) ─────────────────────────────────
BOOKS: dict[str, list[Item]] = {
    "PDF ochadigan dastur(apk) va (exe)🎛": [
        _doc("https://t.me/baza_java_strong/18", "📲Telefon uchun"),
        _doc("https://t.me/baza_java_strong/21", "💻Kompyuter uchun"),
    ],
    # 11-sinf
    "11-Sinf Matematika 1-qism📘": [_doc("https://t.me/baza_java_strong/81?single")],
    "11-Sinf Rus tili📘": [_doc("https://t.me/baza_java_strong/82?single")],
    "11-Sinf Adabiyot 1-qism📘": [_doc("https://t.me/baza_java_strong/83?single")],
    "11-Sinf Adabiyot 2-qism📘": [_doc("https://t.me/baza_java_strong/84?single")],
    "11-Sinf Ona tili 2-qism📘": [_doc("https://t.me/baza_java_strong/85?single")],
    "11-Sinf Kimyo📘": [_doc("https://t.me/baza_java_strong/86?single")],
    # 10-sinf
    "10-Sinf Biologiya📘": [_doc("https://t.me/baza_java_strong/2", "Biologiya Kitob apk fayl olish:\n/apk_b1")],
    "10-Sinf Kimyo📘": [_doc("https://t.me/baza_java_strong/3", "Kimyo Kitob apk fayl olish:\n/apk_k1")],
    "10-Sinf Informatika📘": [_doc("https://t.me/baza_java_strong/4")],
    "10-Sinf Ingliz Tili📘": [_doc("https://t.me/baza_java_strong/5")],
    "10-Sinf Fizika📘": [_doc("https://t.me/baza_java_strong/6", "Fizika Kitob apk fayl olish:\n/apk_f1")],
    "10-Sinf Geometriya📘": [_doc("https://t.me/baza_java_strong/7", "Geometriya Kitob apk fayl olish:\n/apk_g1")],
    "10-Sinf Algebra📘": [_doc("https://t.me/baza_java_strong/8", "Algebra Kitob apk fayl olish:\n/apk_a1")],
    "10-Sinf Geografiya📘": [_doc("https://t.me/baza_java_strong/9", "Geografiya Kitob apk fayl olish:\n/apk_g2")],
    "10-Sinf Ona tili📘": [_doc("https://t.me/baza_java_strong/20", "Ona tili Kitob apk fayl olish:\n/apk_o1")],
    "10-Sinf Kimyo Nazorat ishi📖": [_doc("https://t.me/baza_java_strong/10")],
    # 9-sinf
    "9-Sinf Fizika📘": [_doc("https://t.me/baza_java_strong/65?single")],
    "9-Sinf Rus tili📘": [_doc("https://t.me/baza_java_strong/70?single")],
    "9-Sinf Informatika📘": [_doc("https://t.me/baza_java_strong/66?single")],
    "9-Sinf Geometriya📘": [_doc("https://t.me/baza_java_strong/67?single")],
    "9-Sinf Algebra📘": [_doc("https://t.me/baza_java_strong/68?single")],
    "9-Sinf Geografiya📘": [_doc("https://t.me/baza_java_strong/69?single")],
    "9-Sinf Tarbiya📘": [_doc("https://t.me/baza_java_strong/71?single")],
    # 8-sinf
    "8-Sinf Ona tili📘": [_doc("https://t.me/baza_java_strong/58?single")],
    "8-Sinf Rus tili📘": [_doc("https://t.me/baza_java_strong/61?single")],
    "8-Sinf Informatika📘": [_doc("https://t.me/baza_java_strong/55?single")],
    "8-Sinf Geometriya📘": [_doc("https://t.me/baza_java_strong/57?single")],
    "8-Sinf Algebra📘": [_doc("https://t.me/baza_java_strong/56?single")],
    "8-Sinf Geografiya📘": [_doc("https://t.me/baza_java_strong/60?single")],
    "8-Sinf Tarbiya📘": [_doc("https://t.me/baza_java_strong/59?single")],
    # 7-sinf
    "7-Sinf Biologiya📘": [_doc("https://t.me/baza_java_strong/42?single")],
    "7-Sinf Kimyo📘": [_doc("https://t.me/baza_java_strong/39?single")],
    "7-Sinf Informatika📘": [_doc("https://t.me/baza_java_strong/38?single")],
    "7-Sinf Ingliz Tili📘": [_doc("https://t.me/baza_java_strong/45?single")],
    "7-Sinf Fizika📘": [_doc("https://t.me/baza_java_strong/37?single")],
    "7-Sinf Geometriya📘": [_doc("https://t.me/baza_java_strong/44?single")],
    "7-Sinf Algebra📘": [_doc("https://t.me/baza_java_strong/41?single")],
    "7-Sinf Geografiya📘": [_doc("https://t.me/baza_java_strong/43?single")],
    "7-Sinf Ona tili📘": [_doc("https://t.me/baza_java_strong/47?single")],
    "7-Sinf Musiqa📘": [_doc("https://t.me/baza_java_strong/46?single")],
    "7-Sinf Rus tili📘": [_doc("https://t.me/baza_java_strong/48?single")],
    "7-Sinf Tasviriy san`at📘": [_doc("https://t.me/baza_java_strong/49?single")],
    # apk (10-sinf)
    "/apk_b1": [_doc("https://t.me/baza_java_strong/12?single")],
    "/apk_k1": [_doc("https://t.me/baza_java_strong/16?single")],
    "/apk_f1": [_doc("https://t.me/baza_java_strong/13?single")],
    "/apk_g1": [_doc("https://t.me/baza_java_strong/15?single")],
    "/apk_a1": [_doc("https://t.me/baza_java_strong/11?single")],
    "/apk_g2": [_doc("https://t.me/baza_java_strong/14?single")],
    "/apk_o1": [_doc("https://t.me/baza_java_strong/17?single")],
    # hamma kitoblar
    "Hamma 11-sinf kitobni yuklash📚": [_doc("https://t.me/baza_java_strong/87")],
    "Hamma 9-sinf kitobni yuklash📚": [_doc("https://t.me/baza_java_strong/72")],
    "Hamma 8-sinf kitobni yuklash📚": [_doc("https://t.me/baza_java_strong/62")],
    "Hamma 7-sinf kitobni yuklash📚": [_doc("https://t.me/baza_java_strong/93")],
    # Booknomy audio kitoblar
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿Ingliz tili📕🎧": [
        _doc("https://t.me/baza_java_strong/23?single"),
        _doc("https://t.me/baza_java_strong/24?single"),
        _doc("https://t.me/baza_java_strong/25?single"),
        _doc("https://t.me/baza_java_strong/26?single"),
        _doc("https://t.me/baza_java_strong/27?single"),
        _doc("https://t.me/baza_java_strong/28?single"),
    ],
    "🇰🇷Koreys tili📗🎧": [
        _doc("https://t.me/baza_java_strong/89?single"),
        _doc("https://t.me/baza_java_strong/90?single"),
    ],
    "🇷🇺Rus tili📘🎧": [
        _doc("https://t.me/baza_java_strong/32?single"),
        _doc("https://t.me/baza_java_strong/33?single"),
    ],
}


# ── KOMPYUTER DASTURLARI (software.py) ────────────────────────────
SOFTWARE: dict[str, list[Item]] = {
    # Grafik
    "3Ds Max": [
        _doc("https://t.me/baza_java_strong/109?single", f"3Ds Max\n🗂Part 1{_FOOTER}"),
        _doc("https://t.me/baza_java_strong/110?single", f"3Ds Max\n🗂Part 2{_FOOTER}"),
        _doc("https://t.me/baza_java_strong/111?single", f"3Ds Max\n🗂Part 3{_FOOTER}"),
        _doc("https://t.me/baza_java_strong/112?single", f"3Ds Max\n🗂Part 4{_FOOTER}"),
        _doc("https://t.me/baza_java_strong/113", f"Autodesk Collection 2020 X-ForCe KeyGeN Activator\nLicense{_FOOTER}"),
    ],
    "Unity Pro": [
        _doc("https://t.me/windowsuzprogrammaa/242", f"Unity Pro\n🗂Part 1{_FOOTER}"),
        _doc("https://t.me/windowsuzprogrammaa/243", f"Unity Pro\n🗂Part 2{_FOOTER}"),
        _doc("https://t.me/windowsuzprogrammaa/244", f"Unity Pro\n🗂Part 3{_FOOTER}"),
    ],
    "Corel Draw": [
        _doc("https://t.me/baza_java_strong/114", f"Corel Draw 2020 dasturi\nWindows x32/x64{_FOOTER}"),
    ],
    "Blender dasturi": [
        _doc("https://t.me/baza_java_strong/115",
             f"Blender - bu bepul 3D grafik va animatsiya muharriri.\n3ds max qiladigan ishni blenderda ham qilsa bo`ladi\n💻 Windows 64 bit{_FOOTER}"),
    ],
    "Adobe Photoshop Lightroom": [
        _doc("https://t.me/windowsuzprogrammaa/327",
             f"🖥 Adobe Photoshop Lightroom\n⚙️ Password:  parol yo`q\n💾 Hajmi: 1.1gb \n🛡 Version: 8.4\n😀 x64 (64 bitlik)\n\n📝✅Photoshop bilan bellashadigan ranglar va slaydshovlar mutaxasisi\n⬇️Windows  8|8.1|10|11 da ishlaydi\n\n🎯 #lightroom #photoshoplight{_FOOTER}"),
    ],
    "Adobe Photoshop": [
        _doc("https://t.me/baza_java_strong/117",
             f"🖥 Adobe Photoshop\n⚙️ Password:  parol yo`q\n💾 Hajmi: 1.8gb \n🛡 Version: 2019\n😀 x64 (64 bitlik)\n\n📝✅Adobe Photoshop Mukammal photo muxarriri\n⬇️Windows  8.1|10|11 da ishlaydi{_FOOTER}"),
    ],
    # Windows
    "Game Windows🎮": [
        _doc("BQACAgIAAxkBAAM_Y8WIk0I17y7138IxfPyNH7lquo8AAmkeAAL6umBITN7FLj0DzG4tBA",
             f"<b>Windows 10 Game Edition🎮</b>\n⚙️ Password:  parol yõq📢\n💾 Hajmi: 2.5 gb 😱\n👍 x64 (64 bitlik)\n🌎Language: english\n<b>🎮Windows 10 Home (Game Edition Lite os)🎮</b>\n\n📝Slabiy(kuchsiz) kompyuterlar uchun Maxsus windows 10 Game Edition Os operatsion tizimi. 2 gb ramliklarga ham zòr ishlaydi.. Ortiqcha programmalari õchirib tashlangan\n📹Windowsni tilini ozgartirish <a href='http://youtube.com/channel/UCKhQtK94Fh5RrxOzlKr6asQ'>youtube</a>  kanalimizda\n\n🎯 #win10game #win10gameedition #windows10 #windows10game #windows10gameedition  #win10 #win10liteos #os{_FOOTER}"),
    ],
    "Windows 11": [
        _photo("https://t.me/baza_java_strong/94",
               f"Microsoft Windows 11\n\n📀 Razryadi: x64 bit\n🇷🇺 Tili: rus\n\nTizim talablari: CPU - 1ghz\nRAM - 4gb\nHDD - 64gb\nVideo - DirectX 12\nTPM- 2.0\n\nWindows 11 ning rasmiy versiyasi.\n#windows11\n{bot_linki}\n\n{kanal_link}\nparol: <pre>@ultrasoft_uz</pre>"),
        _doc("https://t.me/windowsuzprogrammaa/63", "Windows 11\n\n📦1-qism"),
        _doc("https://t.me/windowsuzprogrammaa/64", "Windows 11\n\n📦2-qism"),
        _doc("https://t.me/windowsuzprogrammaa/65", f"Windows 11\n\n📦3-qism{_FOOTER}"),
    ],
    "Windows 10": [
        _doc("https://t.me/windowsuzprogrammaa/53",
             f"\n📀 Windows 10 (v2004) RUS-ENG x86-x64 -28in1- HWID-act (AIO)   ✔️\n🖥Платформа: 86x(32-bit)\\64x(64-bit)\n📦1-part\n{_FOOTER}\nparol: <pre>windowsuzprogramm</pre>"),
        _doc("https://t.me/windowsuzprogrammaa/54",
             f"📀 Windows 10 (v2004) RUS-ENG x86-x64 -28in1- HWID-act (AIO)   ✔️\n🖥Платформа: 86x(32-bit)\\64x(64-bit)\n📦2-part{_FOOTER}\nparol: <pre>windowsuzprogramm</pre>"),
        _doc("https://t.me/windowsuzprogrammaa/52",
             f"📀 Windows 10 (v2004) RUS-ENG x86-x64 -28in1- HWID-act (AIO)   ✔️\n🖥Платформа: 86x(32-bit)\\64x(64-bit)\n📦3-part\n\nparol: <pre>windowsuzprogramm</pre>{_FOOTER}"),
    ],
    "Windows 8.1": [
        _doc("https://t.me/windowsuzprogrammaa/45",
             f"\n📀Windоws 8.1 Professional VL with Update Оригинальные образы\n🖥Платформа: 86х(32-bit) \n📦1-part{_FOOTER}\nparol: <pre>windowsuzprogramm</pre>"),
        _doc("https://t.me/windowsuzprogrammaa/54",
             f"📀Windоws 8.1 Professional VL with Update Оригинальные образы\n🖥Платформа: 86х(32-bit) \n📦2-part{_FOOTER}\nparol: <pre>windowsuzprogramm</pre>"),
    ],
    "Windows 7": [
        _doc("https://t.me/windowsuzprogrammaa/43",
             f"📀Оригинальные образы от Microsoft Windows 7 Home Basic with SP1\n🖥Платформа: 86х(32-bit)\n📦1-part{_FOOTER}\nparol: <pre>windowsuzprogramm</pre>"),
        _doc("https://t.me/windowsuzprogrammaa/54",
             f"📀Оригинальные образы от Microsoft Windows 7 Home Basic with SP1🖥Платформа: 86х(32-bit)\n📦2-part{_FOOTER}\nparol: <pre>windowsuzprogramm</pre>"),
    ],
    "Windows 11 LiteOs": [
        _doc("https://t.me/windowsuzprogrammaa/350",
             f"🔋 Windows 11 Ultra LiteOs\n🛠 Version: 22000.493\n⚙️ Password:  parol yõq\n💾 Hajmi: 1.4 gb 😱\n⌨️ x64 (64 bit)\n🌎Language: english\n\n📝✅Slabiy(kuchsiz) kompyuterlar uchun Maxsus windows 11 ultra lite os operatsion tizimi. 2 gb ramliklarga ham zòr ishlaydi.. Ortiqcha programmalari õchirib tashlangan\nWindowsni tilini ozgartirish youtube kanalimizda\n\n🎯  #win11ultra #win11ultraliteos #windows11  #win11 #win11liteos #os{_FOOTER}"),
    ],
    "Windows 10 LiteOs": [
        _doc("BQACAgIAAxkBAANDY8WJKM5ko6n_lqQL06bdYFji7HcAAx8AAovhyUt9yxjMnkiRhy0E",
             f"🔋Windows 10 Home Nexus LiteOs\n⚙️ Password:  Parol yo`q\n💾 Hajmi: 2.6 gb \n🛡 Version: 21H2\n⌨️ x64 (64 bitlik)\n📝 ✅Slabiy(kuchsiz) kompyuterlar uchun Maxsus windows 10 lite os operatsion tizimi. Ortiqcha programmalari õchirib tashlangan\n\n🎯 #win10Nexus #win10Nexusos #windows10  #win10 #win10liteos{_FOOTER}"),
    ],
    "Windows 8.1 LiteOs": [
        _doc("BQACAgIAAxkBAANBY8WJChGQ3RKK2KcQylsfY4sMBIIAAusbAAKASLlLCsLVFM3I8rstBA",
             f"🔋Windows 8.1 Xtrame Lite Os Superlite\n⚙️ Password:  parol yo`q\n🧰 Hajmi: 2.6 gb\n⌨️ x64 (64 bitlik)\n\n📝 ✅Slabiy(kuchsiz) kompyuterlar uchun Maxsus windows 8.1 lite os operatsion tizimi. Ortiqcha programmalari õchirib tashlangan\n\n🎯 #win8_1xtrame #win8_1Xtrameos #windows8_1 #win8_1 #win8_1liteos{_FOOTER}"),
    ],
    "Windows 7 LiteOs": [
        _doc("https://t.me/windowsuzprogrammaa/330",
             f"🔋Windows 7 Xtreme LiteOs\n⚙️ Password:  WPC-7\n💾 Hajmi: 1.7 gb 😱\n👍 x64 (64 bitlik)\n🌎 Language: english\n\n📝 ✅Slabiy(kuchsiz) kompyuterlar uchun Maxsus windows 7 lite os operatsion tizimi. Ortiqcha programmalari õchirib tashlangan\n\n🎯 #win7Xtrame #win7xtreme #windows7  #win7 #win7liteos{_FOOTER}"),
    ],
    # Video montaj
    "Adobe Premiere Pro": [
        _doc("https://t.me/baza_java_strong/116",
             f"Premiere Pro - bu televideniya va film uchun video-tahrirlash sohasidagi yetakchi dastur. Ijodiy vositalar, boshqa dasturlar va xizmatlar bilan integratsiya, filmlar va videofilmlarda kadrlar tayyorlashda yordam beradi.\n\nMinimal tizim talablari:\n\nProtsessor: Intel® 6- chi  avlod yoki undan yuqori - yoki AMD Ryzen ™ 1000 yoki undan yuqori \nOperatsion tizim: Microsoft Windows 10 (64-bit)\nRAM: 8 GB\nVideo karta: 2 GB GPU VRAM\nQattiq diskdagi bo'sh joy: 8GB\nMonitor o'lchamlari:1280 x 800{_FOOTER}"),
    ],
    "Adobe after effects": [
        _doc("https://t.me/windowsuzprogrammaa/278",
             f"<b>After Effects yordamida yaratib bo'lmaydigan narsa yo'q.</b>\n\nKinematik filmlarning sarlavhalarini, kirish so'zlarini va o'tish joylarini yarating. Obyektni klipdan olib tashlang. Olovni yoqing yoki yomg'ir yog'diring. Logotip yoki belgini jonlantirish. Hatto 3D maydonida harakatlaning va dizayn qiling.\n\nTizim talablari: Windows 10 32/64 bit\nOZU DDR4 8GB, CPU Core i5 7gen+, Grafik karta 2GB, HDD 1TB, SSD 250GB\nYili: 2020-yil\nTuri: Repack\nHajmi: 1130.9 MB{_FOOTER}"),
    ],
    "Proshow Producer Pro": [
        _doc("https://t.me/windowsuzprogrammaa/335",
             f"<b>Proshow Producer Pro</b>\n©️ Proshow Producer \n⚙️ Password:<pre>sh093352300</pre>\n💾 Hajmi: 66 mb\n🛡 Version: 9.0\n\n📝✅ Proshow producer rasmlarni pro darajasida tayyorlaydigan dastur videolarni ham tayyorlaydi\n⬇️Windows  7|8|8.1|10|11\n\n🎯 #proshow #proshow_producer #proshowproducer #photoedit{_FOOTER}"),
    ],
    "Edius 8.53": [
        _doc("https://t.me/windowsuzprogrammaa/98",
             f"<b>Edius 8.53</b>\nEdius 8.5  professional video muharriri . Bu programmani kôp video montajchilar ishlatishadi.{_FOOTER}"),
        _doc("https://t.me/windowsuzprogrammaa/103",
             f"Ediusni  8.53 aktivlashtirish videosi!!\nVideo xira chiqdi lekin kõrsa bõladi. Muammolar uchun uzr sõrayman.\n☢️ parol: @windowsuzprogrammaa\n\n{bot_linki}\n{kanal_link}"),
    ],
    # Office
    "Office activator": [
        _doc("https://t.me/baza_java_strong/104",
             f"KMS Matrix - bu Windows va Office dasturlarini tezda faollashtiradigan oddiy aktivator.\n\nFaollashtira oladi:\n• Windows: 7, 8, 8.1, 10\n• Ofis: 2010, 2013, 2016, 2019.\n\nUshbu versiya haqida\n📁 toifasi: #aktivatsiya\n🆚 Versiya: v5.5\n🖥 OS: Windows\n📀 OS Razryadi: x86 / x64\n🇷🇺 Interfeys tili: ingliz tili\n🔑 Aktivatsiya: talab qilinmaydi{_FOOTER}"),
    ],
    "Office 2016": [
        _doc("https://t.me/baza_java_strong/98", f"Mana sizlarga mahsus Microsoft Office 2016 dasturi maqulini yuklab oling! {_FOOTER}"),
    ],
    "Office 2019": [
        _photo("https://t.me/baza_java_strong/101",
               f"\nMicrosoft office 2019\n\nWord, excel, power point, outlook express kabi offis dasturlari mavjud.\n\nPastdagi 2ta faylni ham yuklab olish shart, shundagina kompyuteringizga o'rnata olasiz!!!\n\nWindows 7|10| 64 - bit\n\n{bot_linki}\n\n{kanal_link}\nparol: <pre>@UltraSoft_uz</pre>"),
        _doc("https://t.me/baza_java_strong/99?single",
             f"Microsoft office 2019\n📦1-qism\n\n{bot_linki}\n\n{kanal_link}\nparol: <pre>@UltraSoft_uz</pre>"),
        _doc("https://t.me/baza_java_strong/100?single",
             f"Microsoft office 2019\n📦2-qism\n\n{bot_linki}\n\n{kanal_link}\nparol: <pre>@UltraSoft_uz</pre>"),
    ],
    "Office 2021": [
        _doc("https://t.me/windowsuzprogrammaa/167",
             f"💾 Microsoft Office 2021 LTSC Professional Plus 16.0.14332.20176 RePack by MLRY\n☑️\n🖥 Системные требования:ОС: Windows 10 (32/64 bit)\n\n#MSOffice #Word #Excel #Visio #Project #PowerPoint #Office #Офис #Microsoft #Office2021 #Pro #Редактор\n📦1-part{_FOOTER}"),
        _doc("https://t.me/windowsuzprogrammaa/167",
             f"💾 Microsoft Office 2021 LTSC Professional Plus 16.0.14332.20176 RePack by MLRY\n☑️\n🖥 Системные требования:ОС: Windows 10 (32/64 bit)\n\n#MSOffice #Word #Excel #Visio #Project #PowerPoint #Office #Офис #Microsoft #Office2021 #Pro #Редактор\n📦2-part{_FOOTER}"),
    ],
    "WPS office": [
        _doc("https://t.me/baza_java_strong/103",
             f"WPS Office dasturining Kompyuter versiyasi.\n\nWPS Office - bu matnlarni yoki elektron jadvallarni yozish va tahrirlash uchun bepul dasturlar to'plami. {_FOOTER}"),
    ],
    "Office 2013": [
        _doc("https://t.me/windowsuzprogrammaa/70",
             f"Microsoft Office 2013 x64\n\nMarhamat yuklab olishingiz mumkin!\n#office #office2013 #word #exel #powerpoint {_FOOTER}"),
    ],
    # Aktivator
    "Aktivator⚡️": [
        _doc("https://t.me/baza_java_strong/104",
             f"🔐 Windows 11 Uchun Активатор.\n\n💾 Fayl hajmi: 4 MB.\n\n📝 Izoh: Ushbu dastur yordamida Windows 11 tizimini aktivatsiya qilishingiz mumkin.\nkopincha qolgan windowslarni ham qilsa bo`ladi\n\n\n•┈•┈•┈•┈•❁✿❁•┈•┈•┈•┈•\n#aktivator\n📢Bizning kanal:{_FOOTER}"),
    ],
    # Arxiv
    "Arxiv dasturlar📚": [
        _doc("https://t.me/baza_java_strong/107",
             f"7-Zip x64\n\nℹ️ 7-Zip - bu Windows uchun ajoyib arxivlovchi, uning afzalliklari qulay tezlik, barcha zamonaviy formatlarni qo'llab-quvvatlash va yuqori siqishni nisbati yaxshiroq.{_FOOTER}"),
        _doc("https://t.me/baza_java_strong/108",
             f"WinRAR 5.71\n\nℹ️ Arxiv bilan ishlash uchun WinRAR dasturi. x32 (x86) razryadli kompyuterlar uchun.{_FOOTER}"),
    ],
    # Converter
    "Converter dasturi🔄": [
        _doc("https://t.me/windowsuzprogrammaa/336",
             f"🛒HD Video Converter Factory Pro\n⚙️ Password:  parol yo`q\n💾 Hajmi: 93 mb \n👍 x64 (64 bitlik)\n\n📝✅Xohlagan video,rasm, muzika va hokazilarni converter qiladigan va internetdan fayl yuklaydigan qoshimcha funksiyalari kop dastur\n⬇️Windows  7|8|8.1|10|11 da ishlaydi{_FOOTER}"),
    ],
    # Windows yozish
    "Windowslarni yozish📀📼": [
        _doc("https://t.me/baza_java_strong/105",
             f"<b>UltraIso</b>\nBu dastur yordamida windowsni fleshkaga📼 yoki diskka📀 yozsangiz bo`ladi\n\n🖥 Kompyuterlar  kanaliga ulanish uchun:\n📢Bizning kanal:{_FOOTER}"),
        _doc("https://t.me/baza_java_strong/106",
             f"💾 <b>Rufus 3.10 (Build 1642) Beta Portable</b>☑️\n🖥 Windowslarni fleshkaga yozadigan dastur📼 (x32\\ x64-bit)\n\n🖥 Kompyuterlar  kanaliga ulanish uchun:\n📢Bizning kanal:{_FOOTER}"),
    ],
    # Windows 10 hack password
    "🔐 Windows 10 hack password": [
        _doc("https://t.me/windowsuzprogrammaa/320",
             f"🖼 Videoni oxirigacha ko`ring birinchi\nshoshilib ishni boshlamang kerakli narsalarni olib keyin boshlashni maslahat beramiz\n100% Working✅\n🛡Video HD formatda\n🎯 #Passwordbreak #password #parolbuzish\n#windowspassword\n\n{bot_linki}\n{kanal_link}\n\n/hajmi_kichik_video"),
    ],
    "/hajmi_kichik_video": [
        _doc("https://t.me/windowsuzprogrammaa/321",
             f"🖼 Videoni oxirigacha ko`ring birinchi\nshoshilib ishni boshlamang kerakli narsalarni olib keyin boshlashni maslahat beramiz\n100% Working✅\n🛡Video HD formatda\n🎯 #Passwordbreak #password #parolbuzish\n#windowspassword\n\n{bot_linki}\n{kanal_link}"),
    ],
}

# Barcha kontent kalitlari (lookup uchun)
CATALOG: dict[str, list[Item]] = {**BOOKS, **SOFTWARE}
