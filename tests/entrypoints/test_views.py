import pytest


@pytest.mark.asyncio
async def test_get_buildings(session, async_app, building):
    async with session.begin():
        session.add(building)
        await session.commit()
    async with async_app as app:
        response = await app.get("/building")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "country": "Polska",
            "address": "Towarowa 365",
            "zip_code": "02-200",
            "city": "Warszawa",
            "county": "mazowieckie",
            "locals": [],
        }
    ]
