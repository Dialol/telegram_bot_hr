"""
Обработчики для информационного раздела о компании.
"""
from aiogram import Router, F  
from aiogram.types import CallbackQuery

from keyboards.company_kb import get_about_job_keyboard, get_return_to_job_info_keyboard


router = Router()


@router.callback_query(F.data == 'about_job')
async def process_about_job(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки 'Узнать про работу'.
    """
    await callback.answer()
    await callback.message.edit_text(
            "О работе в сети кофеен \"Кофемашина\":\n\n"
            "Что вас интересует?",
            reply_markup=get_about_job_keyboard()
            )


@router.callback_query(F.data == "about_us")
async def process_about_us(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки 'О нас подробнее'.
    """
    await callback.answer()
    await callback.message.edit_text(
            "О сети кофеен \"Кофемашина\":\n\n"
            "инфа о кофейне",
            reply_markup=get_return_to_job_info_keyboard()
            )


@router.callback_query(F.data == "locations")
async def process_locations(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки 'Местоположение кофеен'.
    """
    await callback.answer()
    await callback.message.edit_text(
            "Наши кофейни расположены в следующих районах города:\n\n"
            "тут инфа про кофейни",
            reply_markup=get_return_to_job_info_keyboard()
            )


@router.callback_query(F.data == "salary")
async def process_salary(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки 'Зарплата'.
    """
    await callback.answer()
    await callback.message.edit_text(
            "Информация о заработной плате:\n\n"
            "Мы предлагаем гибкий график работы и возможность совмещать работу с учебой.",
            reply_markup=get_return_to_job_info_keyboard()
            )


@router.callback_query(F.data == "official_job")
async def process_official_job(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки 'Официальное трудоустройство'.
    """
    await callback.answer()
    await callback.message.edit_text(
            "Официальное трудоустройство в \"Кофемашине\":\n\n"
            "• Оформление по ТК РФ\n",
            reply_markup=get_return_to_job_info_keyboard()
            )


@router.callback_query(F.data == "contacts")
async def process_contacts(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки 'Наши контакты'.
    """
    await callback.answer()
    await callback.message.edit_text(
            "Контактная информация:\n\n"
            "Если у вас остались вопросы, вы можете связаться с нами любым удобным способом.",
            reply_markup=get_return_to_job_info_keyboard()
            )


@router.callback_query(F.data == "return_to_job_info")
async def process_return_to_job_info(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия кнопки 'Узнать про работу еще'
    """
    await callback.answer()
    await callback.message.edit_text(
            "О работе в сети кофеен \"Кофемашина\":\n\n"
            "Что вас интересует?",
            reply_markup=get_about_job_keyboard()
            )


