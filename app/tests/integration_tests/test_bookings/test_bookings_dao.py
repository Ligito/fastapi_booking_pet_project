from datetime import datetime

import pytest

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10","%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24","%Y-%m-%d"),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None

@pytest.mark.parametrize("user_id, room_id", [
    (2,2),
    (2,3),
    (1,4),
    (1,4),
])
async def test_booking_crud(user_id, room_id):
    # добавление брони
    new_booking = await BookingDAO.add(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime("2025-07-15","%Y-%m-%d"),
        date_to=datetime.strptime("2025-07-28","%Y-%m-%d"),
    )
    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    new_booking = await BookingDAO.find_one_or_none(id=new_booking.id)

    # Удаление брони
    await BookingDAO.delete_object(id=new_booking.id)

    # проверка удаления брони
    deleted_booking = await BookingDAO.find_one_or_none(id=new_booking.id)

    assert deleted_booking is None

