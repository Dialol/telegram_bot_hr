"""
Утилиты для отправки уведомлений менеджерам.
"""
from typing import List
from aiogram import Bot

from models import Candidate


async def notify_managers_about_new_candidate(
        bot: Bot,
        candidate: Candidate,
        manager_ids: List[int]
        ) -> None:
    """
    Отправляет уведомление всем менеджерам о новой анкете.
    Args:
        bot: экземпляр бота
        candidate: обьект кандидата
        manager_ids: список id telegram менеджеров
    """
    shift_text = "Дневной" if candidate.shift.value == "day" else "Ночной"
    message_text = (
            f"Новая анкета кандидата!\n\n"
            f"Имя: {candidate.first_name} {candidate.last_name}\n"
            f"Телефон: {candidate.phone}\n"
            f"График: {shift_text}\n"
            f"ID анкеты: {candidate.id}\n\n"
            f"Используйте команду /menu для просмотра анкеты."
            )

    for manager_id in manager_ids:
        try:
            await bot.send_message(
                    chat_id=manager_id,
                    text=message_text
                    )
        except Exception as e:
            print(f"Ошибка отправки оповещения менеджеру {manager_id}: {e}")
