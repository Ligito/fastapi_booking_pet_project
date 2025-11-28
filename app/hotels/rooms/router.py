from fastapi import APIRouter

from typing import List

from fastapi import Query

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRooms

from datetime import date, datetime, timedelta

router = APIRouter(
    prefix="/hotels",
    tags=["Комнаты"]
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}")
) -> List[SRooms]:
    return await RoomsDAO.search_for_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)