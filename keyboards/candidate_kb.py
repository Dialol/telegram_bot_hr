"""
Клавиатуры для пользовательских интерфейсов.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_shift_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора предпочтительного графика работы.
    """
    keyboard = [
            [InlineKeyboardButton(text="Дневной график", callback_data="day")],
            [InlineKeyboardButton(text="Ночной график", callback_data="night")]
            ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)




     
