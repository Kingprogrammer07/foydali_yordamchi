from aiogram.dispatcher.filters.state import StatesGroup, State



class Admin_manager(StatesGroup):                                                  ## admin manager
                                                ## admin + -
    admin_qosh = State()
    admin_remove = State()
                                                # kanal + -
    channel_add = State()
    channel_remove = State()
                                                ## bot ichida elon
    bot_in_elon = State()
    havola_btn = State()
    havola_text = State()

                                                ##     foydalanuvchilarga yozish

    users_text = State()
    foy_text = State()

                                            ##   id orqali topish
    odam_topish = State()
