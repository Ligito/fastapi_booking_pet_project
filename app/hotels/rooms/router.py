from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, Query

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRooms

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
    return await RoomsDAO.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)