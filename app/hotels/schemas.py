from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class SHotelBase(BaseModel):
    name: str
    location: str
    services: Optional[List[str]] = None
    rooms_quantity: int
    image_id: int | None

# Модель для ответа API (с дополнительными полями), id вынесено в этот класс потому что при создании отеля (тогда id не нужен, он генерируется БД).
class SHotelsWithRooms(SHotelBase):
    id: int
    rooms_left: int

    class Config:
        from_attributes = True


class SHotelsTarget(SHotelBase):
    id: int

    class Config:
        from_attributes = True