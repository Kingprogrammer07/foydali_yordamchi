from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup , KeyboardButton,ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


for_taklif = CallbackData("taklif", "action")   ## foydalanuvchi  taklif va yangi post uchun
for_admin_post = CallbackData("new_post", "action") ## admin uchun yangi post
for_channel = CallbackData("channel", "action", "id") # kanal tugmalari uchun
for_delete = CallbackData("delete", "action", "id") # kanal o`shirish` uchun

taklif = InlineKeyboardMarkup(row_width = 1)
taklif.add(
    InlineKeyboardButton(text = "🆕 Fikr yoki Yangi post", callback_data = for_taklif.new(action = "new_post")),
)
                                                                ## orqaga tugmasi
back = ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
back.add(
    KeyboardButton(text = "Orqaga 🔙")
)

                                                                ## for admin
one_chanel = InlineKeyboardMarkup(row_width = 2)
one_chanel.add(
    InlineKeyboardButton(text = "📢 Kanalda", callback_data = for_admin_post.new(action = "first_chanel")),
    InlineKeyboardButton(text = "🤖 Bot ichida", callback_data = for_admin_post.new(action = "in_bot"))
)

all_chanel = InlineKeyboardMarkup(row_width = 2)         ##  kop kanallik tugma
all_chanel.add(
    InlineKeyboardButton(text = "📢 1 ta kanalda", callback_data = for_admin_post.new(action = "one_chanel")),
    InlineKeyboardButton(text = "🤖 Bot ichida", callback_data = for_admin_post.new(action = "in_bot")),
    InlineKeyboardButton(text = "📢 Hamma Kanallarda", callback_data = for_admin_post.new(action = "all_chanel"))
)

save_pst = InlineKeyboardMarkup(row_width = 2)    ## chop etish tugmalari
save_pst.add(
    InlineKeyboardButton(text = "🆗 Chop etish", callback_data = for_admin_post.new(action = "first_oddiy")),
    InlineKeyboardButton(text = "🆗 Tugmacha bilan", callback_data = for_admin_post.new(action = "first_url")),
)

save_pst_url = InlineKeyboardMarkup(row_width = 2)
save_pst_url.add(
    InlineKeyboardButton(text = "🆕 Yangi Tugma", callback_data = for_admin_post.new(action = "first_new_btn")),
    InlineKeyboardButton(text = "↪️ Orqaga", callback_data = for_admin_post.new(action = "first_back"))
)


def btn_create(lugat: dict):                          # tugma yaratish
    uzunligi = len(lugat)
    if uzunligi <= 3:
        create = InlineKeyboardMarkup(row_width = 2)
        for k,v in lugat.items():
            create.insert(
                InlineKeyboardButton(text = k, url = v)
            )
        return create
    
    elif uzunligi < 5:
        create = InlineKeyboardMarkup(row_width = 4)
        for k,v in lugat.items():
            create.insert(
                InlineKeyboardButton(text = k, url = v)
            )
        return create

    else:
        create = InlineKeyboardMarkup(row_width = 5)
        for k,v in lugat.items():
            create.insert(
                InlineKeyboardButton(text = k, url = v)
            )
        return create



                                                ## kanallar uchun btn

def num_btn(num_list):
    btn = InlineKeyboardMarkup(row_width = 4)
    first = None
    for i in num_list:
        if not first:
            first = i  
        btn.insert(
            InlineKeyboardButton(text = i, callback_data = for_channel.new(action = "number", id = i))
        )
    if len(num_list) > 8:
        btn.add(
            InlineKeyboardButton(text = "↩️", callback_data = for_channel.new(action = "orqaga", id = first)),
            InlineKeyboardButton(text = "❌", callback_data = for_channel.new(action = "delete", id = 0)),
            InlineKeyboardButton(text = "↪️", callback_data = for_channel.new(action = "oldinga", id = i)),
        )
    return btn

def delete_btn(num_list):
    btn = InlineKeyboardMarkup(row_width = 4)
    first = None
    for i in num_list:
        if not first:
            first = i  
        btn.insert(
            InlineKeyboardButton(text = i, callback_data = for_delete.new(action = "number", id = i))
        )
    if len(num_list) > 8:
        btn.add(
            InlineKeyboardButton(text = "↩️", callback_data = for_channel.new(action = "orqaga", id = first)),
            InlineKeyboardButton(text = "❌", callback_data = for_channel.new(action = "delete", id = 0)),
            InlineKeyboardButton(text = "↪️", callback_data = for_channel.new(action = "oldinga", id = i)),
        )
    return btn