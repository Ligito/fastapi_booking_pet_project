import asyncio
from fastapi_cache.decorator import cache
from fastapi import APIRouter, Query

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotelsWithRooms, SHotelsTarget
from app.exeptions import ThereIsNotHotelWithThisID

from datetime import date, datetime, timedelta

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

@router.get("/{location}")
@cache(expire=30)
async def get_hotels(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}")
) -> list[SHotelsWithRooms]:
    return await HotelDAO.search_for_hotels(location=location, date_from=date_from, date_to=date_to)

@router.get("/id/{hotel_id}")
async def find_by_hotel_id(hotel_id: int) -> SHotelsTarget:
    result_hotel =  await HotelDAO.find_by_id(hotel_id)
    if not result_hotel:
        raise ThereIsNotHotelWithThisID
    else:
        return result_hotel
