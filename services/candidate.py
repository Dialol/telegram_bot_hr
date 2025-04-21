"""
Сервисы для работы с кандидатами.
"""
from typing import List, Optional
from datetime import date 
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Candidate, WorkShift, CandidateStatus

async def create_candidate(
        session: AsyncSession,
        first_name: str,
        last_name: str,
        birth_date: date, 
        telegram_username: str,
        phone: str,
        shift: str,
        location: str,
        experience: str,
        motivation: str,
        ) -> Candidate:
    """
    Создание новой записи кандидата в базе данных.
    """
    candidate = Candidate(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            telegram_username=telegram_username,
            phone=phone,
            shift=WorkShift(shift),
            location=location,
            experience=experience,
            motivation=motivation,
            status=CandidateStatus.new
            )
    session.add(candidate)
    await session.commit()
    await session.refresh(candidate)

    return candidate


async def get_candidate_by_id(
        session: AsyncSession, 
        candidate_id: int) -> Optional[Candidate]:
    """
    Получение кандидата по ID.
    """
    result = await session.execute(
            select(Candidate).where(Candidate.id == candidate_id)
            )
    return result.scalar_one_or_none()


async def get_all_candidates(
        session: AsyncSession,
        offset: int = 0,
        limit: int = 10
        ) -> List[Candidate]: 
    """
    Получени списка всех кандидатов с пагинацией

    Args:
        offset: Смещение для пагинации
        limit: Максимальное количество записей
    """
    result = await session.execute(
            select(Candidate)
            .order_by(Candidate.id.desc())
            .offset(offset)
            .limit(limit)
            )
    return result.scalars().all()


async def count_candidates(session: AsyncSession) -> int:
    """
    Получение общего количества кандидатов
    """
    result = await session.execute(
            select(func.count())
            .select_from(Candidate)
            )
    return result.scalar_one()


async def update_candidate_status(
        session: AsyncSession,
        candidate_id: int,
        status: str
        ) -> Optional[Candidate]:
    """
    Обновление статуса кандидата.

    Args:
        candidate_id: ID кандидата
        status: Новый статус (значение из CandidateStatus)
    
    Returns:
        Обновленный обьект кандидата или None, если не найден
    """

    candidate = await get_candidate_by_id(session, candidate_id)
    if not candidate:
        return None

    candidate.status = CandidateStatus(status)

    await session.commit()
    await session.refresh(candidate)

    return candidate


async def get_candidates_by_status(
        session: AsyncSession,
        status: str,
        offset: int = 0,
        limit: int = 10
        ) -> List[Candidate]:
    """
    Получение списка кандидатов с определенным статусом

    Args:
        status: Статус для фильтрации (значение из CandidateStatus)
        offset: Смещение для пагинации
        limit: Максимальное количество записей
        
    Returns:
        Список объектов кандидатов с указанным статусом
    """
    result = await session.execute(
            select(Candidate)
            .where(Candidate.status == CandidateStatus(status))
            .order_by(Candidate.id.desc())
            .offset(offset)
            .limit(limit)
            )
    return result.scalars().all()


async def count_candidates_by_status(session: AsyncSession, status: str) -> int:
    """
    Получение количества кандидатов с определенным статусом.
    """
    result = await session.execute(
            select(func.count())
            .select_from(Candidate)
            .where(Candidate.status == CandidateStatus(status))
            )
    return result.scalar_one()








