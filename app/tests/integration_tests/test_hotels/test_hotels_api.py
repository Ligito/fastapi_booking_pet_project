import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("location, date_from, date_to, status_code",[
    ("Алтай", "2030-05-15", "2030-05-25", 200),
    ("Алтай", "2030-06-15", "2030-06-27", 200),
    ("Коми", "2030-05-15", "2030-05-25", 200),
    ("Алтай", "2030-05-25", "2030-05-15", 400),
    ("Алтай", "2030-05-01", "2030-06-15", 400),
])
async def test_get_hotels_time_and_location(
    location,
    date_from,
    date_to,
    status_code,
    authenticated_ac: AsyncClient
):
    response = await authenticated_ac.get(f"/hotels/{location}", params={
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code


