from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List


class SHotelBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    location: str
    services: Optional[List[str]] = None
    rooms_quantity: int
    image_id: int | None

# Модель для ответа API (с дополнительными полями), id вынесено в этот класс потому что при создании отеля (тогда id не нужен, он генерируется БД).
class SHotelsWithRooms(SHotelBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rooms_left: int


class SHotelsTarget(SHotelBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


