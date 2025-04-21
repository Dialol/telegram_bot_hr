"""
Утилиты для проверки прав доступаю.
"""
import os
from typing import Union
from sqlalchemy import select

from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from db import get_session
from models import Manager


ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID", 0))


async def is_admin(user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором.
    """
    return user_id == ADMIN_TELEGRAM_ID


async def is_manager(user_id: int) -> bool:
    """
    Проверяет, является ли пользователь менеджером.
    """
    if await is_admin(user_id):
        return True
        
    session = await get_session()

    query = select(Manager).where(Manager.telegram_id == user_id)
    result = await session.execute(query)
    manager = result.scalar_one_or_none()
    return manager is not None


class AdminFilter(BaseFilter):
    """
    Фильтр для проверки, является ли пользователь администратором.
    """
    async def __call__(self, event: Union[Message, CallbackQuery], bot: Bot) -> bool:
        user_id = event.from_user.id 
        return await is_admin(user_id)


class ManagerFilter(BaseFilter):
    """
    Фильтр для проверки, является ли пользователь менеджером.
    """
    async def __call__(self, event: Union[Message, CallbackQuery], bot: Bot) -> bool:
        user_id = event.from_user.id 
        return await is_manager(user_id)

    




