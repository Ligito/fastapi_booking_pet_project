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


@router.get("/id/{hotel_id}", operation_id="get_hotel_detail")
async def find_by_hotel_id(hotel_id: int) -> SHotelsTarget:
    result_hotel =  await HotelDAO.find_one_or_none(id=hotel_id)
    if not result_hotel:
        raise ThereIsNotHotelWithThisID
    else:
        return result_hotel


@router.get("/{location}")
@cache(expire=30) # Явно указываем operation_id(что бы избежать предупреждения "UserWarning: Duplicate Operation ID")
async def get_hotels(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}")
) -> list[SHotelsWithRooms]:
    return await HotelDAO.search_for_hotels(location=location, date_from=date_from, date_to=date_to)