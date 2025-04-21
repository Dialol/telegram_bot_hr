"""
Обработчики для команд администратора.
"""
from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select

from db import get_session
from models import Manager
from utils.access import AdminFilter
from keyboards.admin_kb import get_admin_menu_keyboard
from keyboards.manager_kb import get_manager_menu_keyboard


router = Router()
admin_filter = AdminFilter()


class AdminStates(StatesGroup):
    """
    Состояния для работы с формами администратора.
    """
    add_manager_id = State()
    add_manager_first_name = State()
    add_manager_last_name = State()


@router.message(Command("admin"), admin_filter)
async def cmd_admin(message: Message) -> None:
    """
    Обработчик команды /admin для администратора.
    """
    await message.answer(
            "Панель администратора:\n\n"
            "Выберите действие из списка ниже:",
            reply_markup=get_admin_menu_keyboard()
            )


@router.callback_query(F.data == "add_manager", admin_filter)
async def process_add_manager(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для добавления нового менеджера.
    """
    await callback.answer()
    await state.set_state(AdminStates.add_manager_id)
    await callback.message.edit_text(
            "Введите Telegram ID нового менеджера:",
            reply_markup=get_admin_menu_keyboard()
            )


@router.message(AdminStates.add_manager_id, admin_filter)
async def process_manager_id(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения ID менеджера.
    """
    try:
        telegram_id = int(message.text.strip())
        await state.update_data(telegram_id=telegram_id)
        await state.set_state(AdminStates.add_manager_first_name)
        await message.answer("Введите имя менеджера:")
    except ValueError:
        await message.answer(
                "Некорректный ID. Пожалуйста, введите числовой Telegram ID:"
                )


@router.message(AdminStates.add_manager_first_name, admin_filter)
async def process_manager_first_name(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения имени менеджера.
    """
    first_name = message.text.strip()
    if len(first_name) < 2 or len(first_name) > 50:
        await message.answer(
                "Имя должно быть от 2 до 50 символов. Пожалуйста, введите снова:"
                )
        return
    
    await state.update_data(first_name=first_name)
    await state.set_state(AdminStates.add_manager_last_name)
    await message.answer("Введите фамилию менеджера:")


@router.message(AdminStates.add_manager_last_name, admin_filter)
async def process_manager_last_name(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения фамилии менеджера.
    """
    last_name = message.text.strip()
    if len(last_name) < 2 or len(last_name) > 50:
        await message.answer(
                "Фамилия должна быть от 2 до 50 символов Пожалуйста, введите снова:"
                )
        return

    data = await state.get_data()
    telegram_id = data.get("telegram_id")
    first_name = data.get("first_name")

    session = await get_session()

    query = select(Manager).where(Manager.telegram_id == telegram_id) 
    result = await session.execute(query)
    existing_manager = result.scalar_one_or_none()

    if existing_manager:
        await message.answer(
                f"Менеджер c ID {telegram_id} уже существует!"
                )
    else:
        new_manager = Manager(
                telegram_id=telegram_id, 
                first_name=first_name,
                last_name=last_name
                )
        session.add(new_manager)
        await session.commit()

        await message.answer(
                f"Менеджер {first_name} {last_name} (ID: {telegram_id}) успешно добавлен!"
                )

    await state.clear()
    await message.answer(
            "Панель администратора:",
            reply_markup=get_admin_menu_keyboard()
            )


@router.callback_query(F.data == "list_managers", admin_filter)
async def process_list_managers(callback: CallbackQuery) -> None:
    """
    Обработчик для просмотра списка всех менеджеров.
    """
    await callback.answer()

    session = await get_session()
    query = select(Manager)
    result = await session.execute(query)
    managers = result.scalars().all()

    if not managers:
        text = "Список менеджеров пуст."
    else:
        text = "Список менеджеров:\n\n"
        for i, manager in enumerate(managers, 1):
            text += f"{i}. {manager.last_name} {manager.first_name} (id: {manager.telegram_id})\n"

    await callback.message.edit_text(
            text,
            reply_markup=get_admin_menu_keyboard()
            )


@router.callback_query(F.data == "admin_menu", admin_filter)
async def process_admin_menu(callback: CallbackQuery) -> None:
    """
    Обработчик для возврата в меню администратора.
    """
    await callback.answer()
    await callback.message.edit_text(
            "Панель администратора:\n\n"
            "Выберите действие из списка ниже:",
            reply_markup=get_admin_menu_keyboard()
            )


@router.callback_query(F.data == "manager_menu", admin_filter)
async def process_to_manager_menu(callback: CallbackQuery) -> None:
    """
    Обработчик для перехода в меню менеджера.
    """
    await callback.answer()
    await callback.message.edit_text(
            "Меню менеджера:\n\n"
            "Выберите действие из списка ниже:",
            reply_markup=get_manager_menu_keyboard()
            )
