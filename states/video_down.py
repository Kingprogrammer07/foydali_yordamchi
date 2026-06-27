from aiogram.dispatcher.filters.state import StatesGroup, State


class video_url(StatesGroup):
    get_url = State()