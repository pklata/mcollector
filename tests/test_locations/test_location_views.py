import pytest


@pytest.mark.asyncio
@pytest.mark.usefixtures("recreate_db")
class TestBuildingViews:
    async def test_get_buildings(self, async_app, building, session):
        session.add(building(id=1))
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
            }
        ]

    async def test_get_building(self, async_app, building, session):
        session.add(building(id=1))
        await session.commit()
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
        }
        async with async_app as app:
            response = await app.post("/building", json=payload)
        assert response.json() == {"id": 1}
        assert response.status_code == 200
        async with async_app as app:
            response = await app.get("/building")
        assert response.status_code == 200
        assert response.json() == [
            {
                "address": "Towarowa 365",
                "city": "Warszawa",
                "country": "Polska",
                "county": "mazowieckie",
                "id": 1,
                "zip_code": "02-200",
            }
        ]

    async def test_update_building(self, session, async_app, building):
        session.add(building(id=1))
        await session.commit()
        payload = {
            "country": "Anglia",
            "address": "Graniczna 17",
        }
        async with async_app as app:
            response = await app.patch("/building/1", json=payload)
        assert response.status_code == 200
        assert response.json() == {"id": 1}
        async with async_app as app:
            response = await app.get("/building")
        assert response.status_code == 200
        assert response.json() == [
            {
                "address": "Graniczna 17",
                "city": "Warszawa",
                "country": "Anglia",
                "county": "mazowieckie",
                "id": 1,
                "zip_code": "02-200",
            }
        ]

    async def test_update_not_existing_building(self, async_app):
        payload = {
            "country": "Anglia",
            "address": "Graniczna 17",
        }
        async with async_app as app:
            response = await app.patch("/building/1", json=payload)
        assert response.status_code == 404
        assert response.json() == {"detail": "Building with id: 1 not found."}

    async def test_delete_building(self, async_app, building, session):
        session.add(building(id=1))
        await session.commit()
        async with async_app as app:
            response = await app.delete("/building/1")
        assert response.status_code == 200
        assert response.json() == {}
        async with async_app as app:
            response = await app.get("/building")
        assert response.status_code == 200
        assert response.json() == []

    async def test_delete_not_existing_building(self, async_app):
        async with async_app as app:
            response = await app.delete("/building/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Building with id: 1 not found."}

    @pytest.mark.usefixtures("locals_setup")
    async def test_get_locals(self, async_app):
        async with async_app as app:
            response = await app.get("/building/1/local")
        assert response.status_code == 200
        assert response.json() == [
            {"description": None, "id": 2, "number": 2},
            {"description": None, "id": 1, "number": 7},
        ]

    @pytest.mark.usefixtures("locals_setup")
    async def test_get_local(self, async_app):
        async with async_app as app:
            response = await app.get("/local/1")
        assert response.status_code == 200
        assert response.json() == {"description": None, "id": 1, "number": 7}

    async def test_get_not_existing_local(self, async_app):
        async with async_app as app:
            response = await app.get("/local/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Local with id: 1 not found."}

    @pytest.mark.usefixtures("locals_setup")
    async def test_create_local(self, async_app):
        payload = {"number": "13"}
        async with async_app as app:
            response = await app.post("/building/1/local", json=payload)
        assert response.json() == {"id": 3}
        assert response.status_code == 200
        async with async_app as app:
            response = await app.get("/building/1/local")
        assert response.status_code == 200
        assert response.json() == [
            {"description": None, "id": 2, "number": 2},
            {"description": None, "id": 1, "number": 7},
            {"description": None, "id": 3, "number": 13},
        ]

    @pytest.mark.usefixtures("locals_setup")
    async def test_update_local(self, async_app):
        payload = {
            "number": "17",
        }
        async with async_app as app:
            response = await app.patch("/local/1", json=payload)
        assert response.status_code == 200
        assert response.json() == {"id": 1}
        async with async_app as app:
            response = await app.get("/building/1/local")
        assert response.status_code == 200
        assert response.json() == [
            {"description": None, "id": 2, "number": 2},
            {"description": None, "id": 1, "number": 17},
        ]

    async def test_update_not_existing_local(self, async_app):
        payload = {
            "number": "17",
        }
        async with async_app as app:
            response = await app.patch("/local/1", json=payload)
        assert response.status_code == 404
        assert response.json() == {"detail": "Local with id: 1 not found."}

    @pytest.mark.usefixtures("locals_setup")
    async def test_delete_local(self, async_app):
        async with async_app as app:
            response = await app.delete("/local/1")
        assert response.status_code == 200
        assert response.json() == {}
        async with async_app as app:
            response = await app.get("/building/1/local")
        assert response.status_code == 200
        assert response.json() == [{"description": None, "id": 2, "number": 2}]

    async def test_delete_not_existing_local(self, async_app):
        async with async_app as app:
            response = await app.delete("/local/1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Local with id: 1 not found."}
