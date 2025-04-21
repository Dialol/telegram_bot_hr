"""
Клавиатура для общих функций бота.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для стартового меню.
    """
    keyboard = [
            [InlineKeyboardButton(text="Заполнить анкету", callback_data="fill_form")],
            [InlineKeyboardButton(text="Узнать про работу", callback_data="about_job")]
            ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


