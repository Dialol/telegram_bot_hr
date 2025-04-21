"""
Общие обработчики, не относящиеся к конкретной функциональности.
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.common_kb import get_start_keyboard


router = Router()


def get_welcome_text(name: str) -> str:
    """
    Текст приветствия с именем пользователя.

    Args:
        name
    Returns:
        str: текст приветствия
    """
    return (
            f"Привет, {name}! \n\n"
            "Я бот для поиска бариста в сеть кофеен \"Кофемашина\".\n"
            "Чем могу помочь?"
            )


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /start. Приветствует пользователя и показывает основное меню.

    Args:
        message: Обьект сообщения
        state: Контекст FSM
    """
    await state.clear()
    await message.answer(
            get_welcome_text(message.from_user.first_name),
            reply_markup=get_start_keyboard()
            )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """
    Обработчик команды /help. Показывает справку по использованию бота.
    """
    await message.answer(
            "Справка по использованию бота\n\n"
            "/start - Начать заново\n"
            "/help - Показать эту справку\n\n"
            "Используйте кнопки в меню для навигации по боту."
            )


@router.callback_query(F.data == "back_to_start")
async def process_back_to_start(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик нажатия кнопки 'Назад' для возврата в главное меню.
    """
    await callback.answer()
    await state.clear()

    await callback.message.edit_text(
            get_welcome_text(callback.from_user.first_name),
            reply_markup=get_start_keyboard()
            )
