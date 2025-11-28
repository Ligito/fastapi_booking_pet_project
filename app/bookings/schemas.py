from pydantic import BaseModel, ConfigDict
from datetime import date


class SBooking(BaseModel):
    # позволяет Pydantic читать данные напрямую из атрибутов ORM-объектов
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
