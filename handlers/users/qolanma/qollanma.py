          
from loader import dp
from aiogram.dispatcher.filters import Text
from keyboards.inline.kanal_va_bot_url import btn_url
from aiogram import types

@dp.message_handler(commands = "qollanma")
async def qollanma(message: types.Message):
    if message.chat.type == "private":
        await message.reply(text = """Bot xizmatlari:
1️⃣ --> Maktab darsliklarini yuklab olishingiz mumkin😉
2️⃣--> Booknomy kitoblarni 3xil tilda yuklab olishingiz mumkin😱
3️⃣--> Qiyin bo`lmasa Bot haqidagi fikringizni ham qoldiring!!
4️⃣--> Botdagi yangi kompyuterlar Bo`limi: bunda siz kompyuterga kerak bolgan kop dasturlarni yuklab olishingiz mumkin

🖥Bizning kompyuter dasturlari kanalimizga va instagram, Youtube kanallarimizga obuna bo`ling!
""", reply_markup = btn_url)


@dp.message_handler(Text(equals = "Qo`llanma📃"))
async def qollanma(message: types.Message):
    if message.chat.type == "private":
        await message.reply(text = """Bot xizmatlari:
1️⃣ --> Maktab darsliklarini yuklab olishingiz mumkin😉
2️⃣--> Booknomy kitoblarni 3xil tilda yuklab olishingiz mumkin😱
3️⃣--> Qiyin bo`lmasa Bot haqidagi fikringizni ham qoldiring!!
4️⃣--> Botdagi yangi kompyuterlar Bo`limi: bunda siz kompyuterga kerak bolgan kop dasturlarni yuklab olishingiz mumkin

🖥Bizning kompyuter dasturlari kanalimizga va instagram, Youtube kanallarimizga obuna bo`ling!
""", reply_markup = btn_url)







