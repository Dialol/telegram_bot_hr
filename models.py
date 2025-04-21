"""Модель анкеты кандидата (таблица candidates)."""

import enum
import datetime

from sqlalchemy import String, Text, Date, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class WorkShift(str, enum.Enum):
    """
    Перечисление возможных графиков работы.

    Значения:
    - "day" - дневная смена
    - "night" - ночная смена
    """

    day = "day"
    night = "night"


class CandidateStatus(str, enum.Enum):
    """
    Перечисление статусов заявки кандидата

    Значение:
    - "new" - новая заявка
    - "approved" - принят
    - "rejected" - отклонен
    """

    new = "new"
    approved = "approved"
    rejected = "rejected"


class Candidate(Base):
    """
    Модель для хранения анкеты кандидата.
    
    Таблица: candidates
    """

    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(
            Integer, primary_key=True, autoincrement=True
            )
    first_name: Mapped[str] = mapped_column(
            String(50), nullable=False, doc="Имя кандидата"
            )
    last_name: Mapped[str] = mapped_column(
            String(50), nullable=False, doc="Фамилия кандидата"
            )
    birth_date: Mapped[datetime.date] = mapped_column(
            Date, nullable=False, doc="Дата рождения"
            )
    telegram_username: Mapped[str] = mapped_column(
            String(64), nullable=True, doc="Username в Telegram"
            )
    phone: Mapped[str] = mapped_column(
            String(20), nullable=False, doc="Номер телефона"
            )    
    shift: Mapped[WorkShift] = mapped_column(
            Enum(WorkShift), nullable=False, doc="Предпочтительный график работы"
            )
    location: Mapped[str] = mapped_column(
            String(100), nullable=False, doc="Желаемая локация для работы"
            )
    experience: Mapped[str] = mapped_column(
            Text, nullable=True, doc="Опыт работы кандидата"
            )
    motivation: Mapped[str] = mapped_column(
            Text, nullable=True, doc="Причина, почему хочет работать"
            )
    status: Mapped[CandidateStatus] = mapped_column(
            Enum(CandidateStatus), nullable=False,
            default=CandidateStatus.new, doc="Статус заявки кандидата"
            )


class ManagerRole(str, enum.Enum):
    """
    Перечисление ролей пользователей.

    Значения:
        - "admin" - управляет менеджерами
        - "manager" - может просматривать и обрабатывать акнкеты
    """
    admin = "admin"
    manager = "manager"


class Manager(Base):
    """
    Модель для хранения информации о менеджерах.
    """
    __tablename__ = "managers"

    id: Mapped[int] = mapped_column(
            Integer, primary_key=True, autoincrement=True
            )
    telegram_id: Mapped[int] = mapped_column(
            Integer, unique=True, nullable=False, doc="Telegram ID менеджера"
            )
    first_name: Mapped[str] = mapped_column(
            String(64), nullable=False, doc="Имя менеджера"
            )
    last_name: Mapped[str] = mapped_column(
            String(64), nullable=False, doc="Фамилия менеджера"
            )


