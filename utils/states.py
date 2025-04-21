"""
Состояния для конечных автоматов (FSM) бота.
"""
from aiogram.fsm.state import State, StatesGroup


class CandidateForm(StatesGroup):
    """
    Группа состояний для формы анкеты кандидата.

    Каждое состояние представляет шаг заполнения анкеты
    """
    first_name = State()
    last_name = State()
    birth_date = State()
    telegram_username = State()
    phone = State()
    shift = State()
    location = State()
    experience = State()
    motivation = State()
