from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


like_bot_yes = InlineKeyboardButton(text="Yes", callback_data="yes")
like_bot_no = InlineKeyboardButton(text="No", callback_data="no")

like_bot_keyboard_builder = InlineKeyboardBuilder()
like_bot_keyboard_builder.add(like_bot_yes, like_bot_no)
like_bot_keyboard_builder.adjust(2)


