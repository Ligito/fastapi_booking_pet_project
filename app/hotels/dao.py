from datetime import date

from sqlalchemy import and_, func, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.logger import logger


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(
            cls,
            location: str,
            date_from: date,
            date_to: date
    ):
        """
        WITH booked_rooms AS (
        SELECT
            room_id,
            COUNT(*) as booked_count
        FROM bookings
        WHERE ((date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_from <= '2023-05-15' AND date_to > '2023-06-20')
            )
        GROUP BY room_id
        )
        SELECT
            h.id,
            h.name,
            h.location,
            h.services,
            h.rooms_quantity,
            h.image_id,
            SUM(r.quantity - COALESCE(br.booked_count, 0)) AS rooms_left
        FROM hotels h
        JOIN rooms r ON h.id = r.hotel_id
        LEFT JOIN booked_rooms br ON r.id = br.room_id
        WHERE h.location LIKE '%Алтай%'
        GROUP BY
            h.id, h.name, h.location, h.rooms_quantity, h.image_id
        HAVING SUM(r.quantity - COALESCE(br.booked_count, 0)) > 0;
        """
        try:
            async with async_session_maker() as session:

                booked_rooms = select(Bookings.room_id,
                                      func.count(Bookings.id).label("booked_count")
                                      ).where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        ),
                    )
                ).group_by(
                    Bookings.room_id
                ).cte("booked_rooms")

                # Подзапрос для hotel_id и rooms_left, без services, а потом джойни данные отеля.
                hotel_subq = (
                    select(
                        Hotels.id.label("hotel_id"),
                        func.sum(Rooms.quantity - func.coalesce(booked_rooms.c.booked_count, 0)).label("rooms_left")
                    )
                    .join(Rooms, Hotels.id == Rooms.hotel_id)
                    .join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
                    .where(Hotels.location.contains(location))
                    .group_by(Hotels.id)
                    .having(func.sum(Rooms.quantity - func.coalesce(booked_rooms.c.booked_count, 0)) > 0)
                    .subquery()
                )

                # Шаг 2: Джойним полные данные отеля
                query_get_hotels = (
                    select(
                        Hotels.id,
                        Hotels.name,
                        Hotels.location,
                        Hotels.services,  # ← теперь можно без агрегации!
                        Hotels.rooms_quantity,
                        Hotels.image_id,
                        hotel_subq.c.rooms_left
                    )
                    .join(hotel_subq, Hotels.id == hotel_subq.c.hotel_id)
                )

                get_hotels_result = await session.execute(query_get_hotels)
                return get_hotels_result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database"
            elif isinstance(e, Exception):
                msg = "Unknown"
            msg += " Exc: Cannot add booking"
            extra = {
                "location": location,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg,extra=extra,exc_info=True,)
