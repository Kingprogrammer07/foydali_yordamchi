"""CallbackData sinflari (aiogram 3)."""
from aiogram.filters.callback_data import CallbackData


class PostCB(CallbackData, prefix="create_post"):
    action: str          # post | cancel


class TaklifCB(CallbackData, prefix="taklif"):
    action: str          # new_post


class AdminPostCB(CallbackData, prefix="new_post"):
    action: str          # first_chanel | first_url | first_back | first_oddiy |
    #                      first_new_btn | in_bot | one_chanel


class ChannelCB(CallbackData, prefix="channel"):
    action: str          # number | orqaga | oldinga | delete
    id: int


class DeleteCB(CallbackData, prefix="delete"):
    action: str          # number
    id: int
    kind: str            # admin | kanal


class BotPostCB(CallbackData, prefix="for_bot"):
    action: str          # ishla
