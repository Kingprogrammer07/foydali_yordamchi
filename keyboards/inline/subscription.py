from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def btn(invite_link):
    check_button = InlineKeyboardMarkup(row_width = 1)
    for i in invite_link:
        check_button.insert(InlineKeyboardButton(text = "Obuna bo`lish", url = i),
    )
    check_button.add(InlineKeyboardButton(text="Obunani tekshirish ✅", callback_data="check_subs"))
    # retry = InlineKeyboardMarkup(row_width = 1).add(InlineKeyboardButton(text = "Obuna bo'ling", url = invite_link))
    
    return check_button
