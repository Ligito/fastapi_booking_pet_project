from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.dao.base import BaseDAO
from sqlalchemy import select, and_, or_, func

from datetime import date


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def search_for_rooms(cls, hotel_id: int, date_from: date, date_to: date):
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
            r.id,
            r.hotel_id,
            r.name,
            r.description,
            r.services,
            r.price,
            r.quantity,
            r.image_id,
            ((DATE '2025-05-25' - DATE '2025-05-05') * price) AS total_cost,
            SUM(r.quantity - COALESCE(br.booked_count, 0)) AS rooms_left
            FROM rooms r
            LEFT JOIN booked_rooms br ON r.id = br.room_id
            WHERE r.hotel_id = 1
            GROUP BY
                r.id,
                r.hotel_id,
                r.name,
                r.description,
                r.price,
                r.quantity,
                r.image_id,
                ((DATE '2025-05-25' - DATE '2025-05-05') * price)
        """
        async with (async_session_maker() as session):

            # Подзапрос: количество забронированных комнат
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

            # Подзапрос: total_cost и rooms_left
            subq_total_cost_and_rooms_left = select(Rooms.id.label("room_id"),
                                                ((date_to - date_from).days * Rooms.price).label("total_cost"),
                                                func.sum(Rooms.quantity - func.coalesce(booked_rooms.c.booked_count, 0)).label("rooms_left")
            ).join(
                booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).group_by(
                Rooms.id,
                Rooms.price
            ).subquery()

            final_query = (
                select(
                    Rooms.id,
                    Rooms.hotel_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                    Rooms.price,
                    Rooms.quantity,
                    Rooms.image_id,
                    subq_total_cost_and_rooms_left.c.total_cost,
                    subq_total_cost_and_rooms_left.c.rooms_left
                ).join(
                    subq_total_cost_and_rooms_left,
                    Rooms.id == subq_total_cost_and_rooms_left.c.room_id
                ).where(
                    Rooms.hotel_id == hotel_id
                )
            )
            get_rooms_in_hotel_result = await session.execute(final_query)
            return get_rooms_in_hotel_result.mappings().all()

            # final_query = (
            #     select(
            #         Rooms.id,
            #         Rooms.hotel_id,
            #         Rooms.name,
            #         Rooms.description,
            #         Rooms.services,
            #         Rooms.price,
            #         Rooms.quantity,
            #         Rooms.image_id,
            #         ((date_to - date_from) * Rooms.price).label("total_cost"),  # ✅ Без подзапроса
            #         func.sum(Rooms.quantity - func.coalesce(booked_rooms.c.booked_count, 0)).label("rooms_left")
            #     )
            #     .join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
            #     .where(Rooms.hotel_id == hotel_id)
            #     .group_by(
            #         Rooms.id,
            #         Rooms.hotel_id,
            #         Rooms.name,
            #         Rooms.description,
            #         Rooms.services,
            #         Rooms.price,
            #         Rooms.quantity,
            #         Rooms.image_id
            #     )
            # )
            #
            # get_rooms_in_hotel_result = await session.execute(final_query)
            # return get_rooms_in_hotel_result.mappings().all()