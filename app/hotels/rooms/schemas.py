from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class SRoomsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    hotel_id: int
    name: str
    description: str
    price: int
    services: Optional[List[str]] = None
    quantity: int
    image_id: int | None

class SRooms(SRoomsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rooms_left: int # количество оставшихся номеров
    total_cost: int # стоимость бронирования номера за весь период

