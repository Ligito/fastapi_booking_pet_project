from fastapi import APIRouter, Depends, BackgroundTasks
from datetime import date
from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.config import settings
from app.tasks.tasks import send_booking_confirmation_email, send_booking_confirmation_telegram

from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exeptions import RoomCannotBeBooked, ThereIsNotDataToDelete

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post("")
async def add_booking(
        background_tasks: BackgroundTasks,
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(
        user.id,
        room_id,
        date_from,
        date_to
    )
    if not booking:
        raise RoomCannotBeBooked
    # Можно и так, но легче как ниже, но в pydantic моделе должен быть атрибут from_attributes=True
    #booking_dict = TypeAdapter(SBooking).validate_python(booking).model_dump()
    booking_dict = SBooking.model_validate(booking).model_dump()
    # вариант с celery
    #send_booking_confirmation_email.delay(booking_dict, user.email)
    # вариант встроенный background tasks
    # background_tasks.add_task(send_booking_confirmation_email, booking_dict, user.email)

    # вариант с celery отправка письма в телегу. CHAT_ID захардкожен на мой что бы не обновлять БС(возможная доработка)
    #send_booking_confirmation_telegram.delay(booking_dict, settings.TELEGRAM_BOT_CHAT_ID)

    return booking_dict

@router.delete("/{booking_id}")
async def delete_booking(
        booking_id: int,
        user: Users = Depends(get_current_user),
):
    # Сначала проверяем, существует ли бронирование у этого пользователя
    bookings = await BookingDAO.find_one_or_none(id=booking_id, user_id=user.id)

    if not bookings:
        raise ThereIsNotDataToDelete

    # Удаляем бронирование
    await BookingDAO.delete_object(id=booking_id, user_id=user.id)








