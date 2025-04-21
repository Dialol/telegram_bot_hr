"""
Клавиатуры для интерфейса менеджера.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_manager_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура основного меню менеджера.
    """
    keyboard = [
        [InlineKeyboardButton(text="Просмотр всех анкет", callback_data="view_all_candidates")],
        [InlineKeyboardButton(text="Поиск кандидатов", callback_data="search_candidates")],
        [InlineKeyboardButton(text="Статистика", callback_data="view_statistics")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_candidate_actions_keyboard(candidate_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура действий с конкретной анкетой кандидата.
    
    Args:
        candidate_id: Идентификатор кандидата
    """
    keyboard = [
        [InlineKeyboardButton(text="Принять", callback_data=f"approve_candidate:{candidate_id}")],
        [InlineKeyboardButton(text="Отклонить", callback_data=f"reject_candidate:{candidate_id}")],
        [InlineKeyboardButton(text="Связаться", callback_data=f"contact_candidate:{candidate_id}")],
        [InlineKeyboardButton(text="Назад к списку", callback_data="back_to_candidates")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_pagination_keyboard(
    page: int, total_pages: int, prefix: str = "candidates"
) -> InlineKeyboardMarkup:
    """
    Клавиатура для пагинации списков.
    
    Args:
        page: Текущая страница
        total_pages: Всего страниц
        prefix: Префикс для callback_data
    """
    keyboard = []
    
    nav_buttons = []
    
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(text="Назад", callback_data=f"{prefix}_page:{page-1}")
        )
    
    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(text="Вперед", callback_data=f"{prefix}_page:{page+1}")
        )
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton(text="В главное меню", callback_data="manager_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
