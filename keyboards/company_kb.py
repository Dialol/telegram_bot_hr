"""
Клавиатуры для информационного раздела о компании.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_about_job_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для раздела "Узнать про работу".
    """
    keyboard = [
        [InlineKeyboardButton(text="О нас подробнее", callback_data="about_us")],
        [InlineKeyboardButton(text="Местоположение кофеен", callback_data="locations")],
        [InlineKeyboardButton(text="Зарплата", callback_data="salary")],
        [InlineKeyboardButton(text="Официальное трудоустройство", callback_data="official_job")],
        [InlineKeyboardButton(text="Наши контакты", callback_data="contacts")],
        [InlineKeyboardButton(text="Заполнить анкету", callback_data="fill_form")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_return_to_job_info_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для возврата в раздел о работе или перехода к анкете.
    """
    keyboard = [
        [InlineKeyboardButton(text="Узнать про работу ещё", callback_data="return_to_job_info")],
        [InlineKeyboardButton(text="Заполнить анкету", callback_data="fill_form")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
