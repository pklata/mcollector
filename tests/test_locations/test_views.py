from dataclasses import asdict

import pytest

from mcollector.locations.repository import BuildingsRepository


@pytest.mark.asyncio
@pytest.mark.usefixtures("nested_session")
class TestBuildingViews:
    async def test_get_buildings(self, async_app, building, nested_session):
        nested_session.add(building(id=1))
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

    async def test_get_building(self, async_app, building, nested_session):
        nested_session.add(building(id=1))
        async with async_app as app:
            response = await app.get("/building/1")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "country": "Polska",
            "address": "Towarowa 365",
            "zip_code": "02-200",
            "city": "Warszawa",
            "county": "mazowieckie",
            "locals": [],
        }

    async def test_get_not_existing_building(self, async_app):
        async with async_app as app:
            response = await app.get("/building/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Building with id: 1 not found."}

    async def test_create_building(self, async_app):
        payload = {
            "country": "Polska",
            "address": "Towarowa 365",
            "zip_code": "02-200",
            "city": "Warszawa",
            "county": "mazowieckie",
            "locals": [],
        }
        async with async_app as app:
            response = await app.post("/building", json=payload)
        assert response.json() == {"id": 1}
        assert response.status_code == 200

    async def test_update_building(self, nested_session, async_app, building):
        nested_session.add(building(id=1))
        payload = {
            "country": "Anglia",
            "address": "Graniczna 17",
        }
        async with async_app as app:
            response = await app.patch("/building/1", json=payload)
        assert response.status_code == 200
        assert response.json() == {"id": 1}
        building = await BuildingsRepository(nested_session).get(1)
        assert asdict(building) == {
            "id": 1,
            "country": "Anglia",
            "address": "Graniczna 17",
            "zip_code": "02-200",
            "city": "Warszawa",
            "county": "mazowieckie",
            "locals": [],
        }

    async def test_update_not_existing_building(self, async_app):
        payload = {
            "country": "Anglia",
            "address": "Graniczna 17",
        }
        async with async_app as app:
            response = await app.patch("/building/1", json=payload)
        assert response.status_code == 404
        assert response.json() == {"detail": "Building with id: 1 not found."}

    async def test_delete_building(self, async_app, building, nested_session):
        nested_session.add(building(id=1))
        async with async_app as app:
            response = await app.delete("/building/1")
        assert response.status_code == 200
        assert response.json() == {}

    async def test_delete_not_existing_building(self, async_app):
        async with async_app as app:
            response = await app.delete("/building/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Building with id: 1 not found."}
