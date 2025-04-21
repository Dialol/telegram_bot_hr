"""
Клавиатура для интерфейса администратора.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для основного меню администратора.
    """
    keyboard = [
            [InlineKeyboardButton(text="Меню менеджера", callback_data="manager_menu")],
            [InlineKeyboardButton(text="Список менеджеров", callback_data="list_managers")],
            [InlineKeyboardButton(text="Добавить менеджера", callback_data="add_manager")]
            ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

