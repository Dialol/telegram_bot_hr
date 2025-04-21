"""Инициализация подключения к базе данных (async SQLAlchemy + PostgreSQL)"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
        )


class Base(DeclarativeBase):
    """Базовый класс, от которого наследуются все модели."""
    pass

async def get_session() -> AsyncSession:
    """
    Создает асинхронную сессию с базой данных.

    Используется как зависимость или утилита для запросов к базе.
    """
    session = async_session()
    try:
        return session
    finally:
        await session.close()
