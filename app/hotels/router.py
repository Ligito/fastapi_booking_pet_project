import asyncio
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exeptions import HotelIncorrectParameters, ThereIsNotHotelWithThisID
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotelsTarget, SHotelsWithRooms

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
# @cache(expire=30) # Явно указываем operation_id(что бы избежать предупреждения "UserWarning: Duplicate Operation ID")
async def get_hotels(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}")
) -> list[SHotelsWithRooms]:
    if date_from >= date_to or (date_to - date_from).days > 30:
        raise HotelIncorrectParameters

    return await HotelDAO.find_all(location=location, date_from=date_from, date_to=date_to)