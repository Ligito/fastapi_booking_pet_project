from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class SRoomsBase(BaseModel):
    hotel_id: int
    name: str
    description: str
    price: int
    services: Optional[List[str]] = None
    quantity: int
    image_id: int | None

class SRooms(SRoomsBase):
    id: int
    rooms_left: int # количество оставшихся номеров
    total_cost: int # стоимость бронирования номера за весь период

    class Config:
        from_attributes = True