"""
Обработчики для команд менеджера/рекрутера.
"""
import math

from aiogram import Router, F
from aiogram.types import (
        Message, 
        CallbackQuery, 
        InlineKeyboardMarkup, 
        InlineKeyboardButton)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.manager_kb import (
    get_manager_menu_keyboard,
    get_candidate_actions_keyboard,
    get_pagination_keyboard
)

from db import get_session
from utils.access import ManagerFilter
from services.candidate import (
    get_all_candidates,
    get_candidate_by_id,
    count_candidates,
    update_candidate_status
)


router = Router()
CANDIDATES_PER_PAGE = 10 

manager_filter = ManagerFilter()


@router.message(Command("menu"), manager_filter)
async def cmd_menu(message: Message) -> None:
    """
    Обработчик команды /menu для менеджера.
    """
    await message.answer(
        "Меню менеджера:\n\n"
        "Выберите действие из списка ниже:",
        reply_markup=get_manager_menu_keyboard()
    )


@router.callback_query(F.data == "manager_menu")
async def process_manager_menu(callback: CallbackQuery) -> None:
    """
    Обработчик для возврата в главное меню менеджера.
    """
    await callback.answer()
    await callback.message.edit_text(
        "Меню менеджера:\n\n"
        "Выберите действие из списка ниже:",
        reply_markup=get_manager_menu_keyboard()
    )


@router.callback_query(F.data == "view_all_candidates")
async def process_view_all_candidates(callback: CallbackQuery) -> None:
    """
    Обработчик для просмотра всех кандидатов (первая страница).
    """
    await callback.answer()
    await show_candidates_page(callback, 1)


@router.callback_query(F.data.startswith("candidates_page:"))
async def process_candidates_page(callback: CallbackQuery) -> None:
    """
    Обработчик для пагинации по списку кандидатов.
    """
    await callback.answer()
    page = int(callback.data.split(":")[1])
    await show_candidates_page(callback, page)


async def show_candidates_page(callback: CallbackQuery, page: int) -> None:
    """
    Показывает страницу со списком кандидатов.
    """
    session = await get_session()
    
    total_candidates = await count_candidates(session)
    total_pages = math.ceil(total_candidates / CANDIDATES_PER_PAGE)
    
    if total_candidates == 0:
        await callback.message.edit_text(
            "В базе данных пока нет ни одного кандидата.",
            reply_markup=get_pagination_keyboard(1, 1)
        )
        return
    
    offset = (page - 1) * CANDIDATES_PER_PAGE
    candidates = await get_all_candidates(
        session,
        offset=offset,
        limit=CANDIDATES_PER_PAGE
    )
    
    text = f"Список кандидатов (страница {page} из {total_pages}):\n\n"
    
    for i, candidate in enumerate(candidates, 1):
        text += (
            f"{i}. {candidate.first_name} {candidate.last_name}\n"
            f"   Телефон: {candidate.phone}\n"
            f"   График: {'Дневной' if candidate.shift.value == 'day' else 'Ночной'}\n"
            f"   ID: {candidate.id}\n\n"
        )
    
    text += "Для просмотра детальной информации, выберите кандидата:"
    
    keyboard = []
    for candidate in candidates:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{candidate.first_name} {candidate.last_name}",
                callback_data=f"view_candidate:{candidate.id}"
            )
        ])
    
    pagination = get_pagination_keyboard(page, total_pages)
    keyboard.extend(pagination.inline_keyboard)
    
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )


@router.callback_query(F.data.startswith("view_candidate:"))
async def process_view_candidate(callback: CallbackQuery) -> None:
    """
    Обработчик для просмотра детальной информации о кандидате.
    """
    await callback.answer()
    
    candidate_id = int(callback.data.split(":")[1])
    session = await get_session()
    candidate = await get_candidate_by_id(session, candidate_id)
    
    if not candidate:
        await callback.message.edit_text(
            "Кандидат не найден. Возможно, анкета была удалена.",
            reply_markup=get_manager_menu_keyboard()
        )
        return
    
    shift_text = "Дневной" if candidate.shift.value == "day" else "Ночной"
    
    text = (
        f"Анкета кандидата #{candidate.id}:\n\n"
        f"Имя: {candidate.first_name} {candidate.last_name}\n"
        f"Телефон: {candidate.phone}\n"
        f"Дата рождения: {candidate.birth_date.strftime('%d.%m.%Y')}\n"
        f"График: {shift_text}\n"
        f"Локация: {candidate.location}\n\n"
        f"Опыт работы:\n{candidate.experience}\n\n"
        f"Мотивация:\n{candidate.motivation}\n\n"
    )
    
    if hasattr(candidate, "status"):
        status_mapping = {
            "new": "Новая",
            "approved": "Принят",
            "rejected": "Отклонен"
        }
        status_text = status_mapping.get(candidate.status.value, "Неизвестно")
        text += f"Статус: {status_text}\n\n"
    
    text += "Выберите действие:"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_candidate_actions_keyboard(candidate.id)
    )


@router.callback_query(F.data == "back_to_candidates")
async def process_back_to_candidates(callback: CallbackQuery) -> None:
    """
    Обработчик для возврата к списку кандидатов.
    """
    await callback.answer()
    await show_candidates_page(callback, 1)


@router.callback_query(F.data.startswith("approve_candidate:"))
async def process_approve_candidate(callback: CallbackQuery) -> None:
    """
    Обработчик для принятия кандидата.
    """
    await callback.answer()
    candidate_id = int(callback.data.split(":")[1])
    
    session = await get_session()
    await update_candidate_status(session, candidate_id, "approved")
    
    await callback.message.edit_text(
        f"Кандидат #{candidate_id} принят!\n\n"
        "Что вы хотите сделать дальше?",
        reply_markup=get_manager_menu_keyboard()
    )


@router.callback_query(F.data.startswith("reject_candidate:"))
async def process_reject_candidate(callback: CallbackQuery) -> None:
    """
    Обработчик для отклонения кандидата.
    """
    await callback.answer()
    candidate_id = int(callback.data.split(":")[1])
    
    session = await get_session()
    await update_candidate_status(session, candidate_id, "rejected")
    
    await callback.message.edit_text(
        f"Кандидат #{candidate_id} отклонен.\n\n"
        "Что вы хотите сделать дальше?",
        reply_markup=get_manager_menu_keyboard()
    )


@router.callback_query(F.data.startswith("contact_candidate:"))
async def process_contact_candidate(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для связи с кандидатом.
    """
    await callback.answer()
    candidate_id = int(callback.data.split(":")[1])
    
    session = await get_session()
    candidate = await get_candidate_by_id(session, candidate_id)
    
    if not candidate:
        await callback.message.edit_text(
            "Кандидат не найден.",
            reply_markup=get_manager_menu_keyboard()
        )
        return
    
    await callback.message.edit_text(
        f"Вы можете связаться с кандидатом "
        f"{candidate.first_name} {candidate.last_name}:\n\n"
        f"Телефон: {candidate.phone}\n"
        f"Telegram: @{candidate.telegram_username}\n\n"
        "После связи, вы можете обновить статус кандидата.",
        reply_markup=get_candidate_actions_keyboard(candidate.id)
    )


@router.callback_query(F.data == "search_candidates")
async def process_search_candidates(callback: CallbackQuery) -> None:
    """
    Обработчик для поиска кандидатов.
    """
    await callback.answer()
    await callback.message.edit_text(
            "Функция в разработке",
            reply_markup=get_manager_menu_keyboard()
            )


@router.callback_query(F.data == "view_statistics")
async def process_view_statistics(callback: CallbackQuery) -> None:
    """
    Обработчик для просмотра статистики.
    """
    await callback.answer()

    session = await get_session()
    total_count = await count_candidates(session)

    text = (
            "Статистика по кандидатам:\n\n"
            f"Всего анкет: {total_count}\n\n"
            "Подробная статистика находится в разработке"
            )

    await callback.message.edit_text(
            text,
            reply_markup=get_manager_menu_keyboard()
            )
