"""
Сервисы для работы с менеджерами.
"""
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Manager

async def get_all_managers(session: AsyncSession) -> List[Manager]:
    """
    Получение списка всех менеджеров.
    """
    result = await session.execute(select(Manager))
    return result.scalars().all()
