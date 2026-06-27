from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


bot_post = CallbackData('for_bot', 'action')

ishlatish = InlineKeyboardMarkup(row_width = 1).add(InlineKeyboardButton(text = 'Ishlatish', callback_data = bot_post.new(action = 'ishla')))