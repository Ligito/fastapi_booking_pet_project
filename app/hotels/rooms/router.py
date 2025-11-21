from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRooms

from app.hotels.router import router

from datetime import date


# @router.get("/{location}")
# async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotels]:
#     return await HotelDAO.find_all(location=location, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRooms]:
    return await RoomsDAO.search_for_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)