"""
Обработчики для формы анкеты кандидата.
"""
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.candidate_kb import get_shift_keyboard
from utils.states import CandidateForm
from db import get_session
from services.candidate import create_candidate


router = Router()


@router.callback_query(F.data == "fill_form")
async def process_fill_form(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик нажатия кнопки 'Заполнить анкету'.
    """
    await callback.answer()
    await state.set_state(CandidateForm.first_name)
    await state.update_data(telegram_id=callback.from_user.id)
    await callback.message.edit_text(
            "Начинаем заполнение анкеты на должность бариста.\n\n"
            "Как вас зовут (Имя)"
            )


@router.message(CandidateForm.first_name)
async def process_first_name(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения имени кандидата
    """
    if len(message.text) < 2 or len(message.text) > 50:
        await message.answer(
                "Имя должно быть от 2 до 50 символов. Пожалуйста, введите снова."
                )
        return
    
    await state.update_data(first_name=message.text)
    await state.set_state(CandidateForm.last_name)

    await message.answer("Отлично! Теперь введите вашу фамилию:")


@router.message(CandidateForm.last_name)
async def process_last_name(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения фамилии кандидата.
    """
    if len(message.text) < 2 or len(message.text) > 50:
        await message.answer(
                "Фамилия должна быть от 2 до 50 символов. Пожалуйста, введите снова."
                )
        return

    await state.update_data(last_name=message.text)
    await state.set_state(CandidateForm.birth_date)

    await message.answer(
            "Спасибо! теперь введите вашу дату рождения в формате ДД.ММ.ГГГГ:"
            )


@router.message(CandidateForm.birth_date)
async def process_birth_date(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения даты рождения
    """
    try:
        birth_date = datetime.strptime(message.text, "%d.%m.%Y").date()
        today = datetime.now().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        if age < 18 or age > 50:
            await message.answer(
                    "Возраст должен быть от 18 до 50 лет. Пожалуйста проверьте дату и введите снова"
                    )
            return

        await state.update_data(birth_date=birth_date)
        await state.set_state(CandidateForm.phone)

        await message.answer(
                "Отлично! Теперь введите ваш номер телефона в формате +7XXXXXXXXXX:"
                )
    except ValueError:
        await message.answer(
                "Некорректный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ (например, 01.01.1990)"
                )
        return


@router.message(CandidateForm.phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения номера телефона кандидата.
    """
    phone = message.text.strip()
    if not (phone.startswith("+7") and len(phone) == 12 and phone[1:].isdigit()):
        await message.answer(
                "Некорректный формат номера телефона. Пожалуйста, введите в формате +7XXXXXXXXXX."
                )
        return

    await state.update_data(phone=phone)
    await state.set_state(CandidateForm.shift)

    await message.answer(
            "Спасибо! Выберите предпочтительный график работы:",
            reply_markup=get_shift_keyboard()
            )


@router.callback_query(CandidateForm.shift, F.data.in_(["day", "night"]))
async def process_shift(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для получения предпочитаемого графика работы.
    """
    await callback.answer()

    await state.update_data(shift=callback.data)
    await state.set_state(CandidateForm.location)

    shift_name = "дневной" if callback.data == "day" else "ночной"
    await callback.message.edit_text(
            f"Вы выбрали {shift_name} график работы.\n\n"
            "Теперь укажите предпочтительную локацию для работы:"
            )


@router.message(CandidateForm.location)
async def process_location(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения желаеморй локации для работы.
    """
    await state.update_data(location=message.text)
    await state.set_state(CandidateForm.experience)

    await message.answer(
            "Спасибо! Расскажите о вашем опыте работы (если есть):"
            )


@router.message(CandidateForm.experience)
async def process_experience(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения опыта работы кандидата.
    """
    await state.update_data(experience=message.text)
    await state.set_state(CandidateForm.motivation)

    await message.answer(
            "Осталось совсем немного! Расскажите, почему вы хотите работать в нашей сети:"
            )


@router.message(CandidateForm.motivation)
async def process_motivation(message: Message, state: FSMContext) -> None:
    """
    Обработчик для получения мотивации кандидата.
    Финальный шаг анкеты.
    """
    await state.update_data(motivation=message.text)
    form_data = await state.get_data()
    form_data["telegram_username"] = message.from_user.username or ""
    
    session = await get_session() 
    try:
        candidate = await create_candidate(
                session=session, 
                first_name=form_data["first_name"],
                last_name=form_data["last_name"],
                birth_date=form_data["birth_date"],
                telegram_username=form_data["telegram_username"],
                phone=form_data["phone"],
                shift=form_data["shift"],
                location=form_data["location"],
                experience=form_data["experience"],
                motivation=form_data["motivation"],
                ) 
        
        await state.clear()
        await message.answer(
                f"Спасибо, {candidate.first_name}!\n\n"
                "Ваша анкета успешно сохранена. Наш менеджер свяжется с вами в ближайшее время."
                )
    except Exception as e:
        await message.answer(
                "Произошла ошибка при сохранении анкеты. Пожалуйста, попробуйте позже"
                )
        print(f"Error saving candidate: {e}")



