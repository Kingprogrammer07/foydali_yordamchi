from aiogram.dispatcher.filters.state import StatesGroup, State


class NewPost_new(StatesGroup):
    NewMessage = State()            #oddiy odamlar uchun
    Confirm = State()
    fikr = State()
    user_caption = State()

                                    ##  yangi btn
    new_btn_text = State()
    new_btn_url = State()
    inbot_url = State()
