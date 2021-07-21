from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory

from mcollector.repository.buildings_repository import BuildingNotFoundError
from mcollector.services import buildings_service


@pytest.mark.asyncio
class TestBuildingsService:
    async def test_list(self, building):
        building1 = await building()
        building2 = await building()
        buildings = await buildings_service.list()
        assert buildings == [asdict(building1), asdict(building2)]

    async def test_get(self, building):
        building1 = await building(id=1)
        building_ = await buildings_service.get(1)
        assert building_ == asdict(building1)

    async def test_get_non_existing(self):
        with pytest.raises(BuildingNotFoundError):
            await buildings_service.get(1)

    async def test_add(self):
        building1 = BuildingFactory()
        result = await buildings_service.add(asdict(building1))
        buildings = await buildings_service.list()
        building1.id = result["id"]
        assert result == {"id": 1}
        assert buildings == [asdict(building1)]

    async def test_delete(self, building):
        await building(id=1)
        await buildings_service.delete(1)
        buildings = await buildings_service.list()
        assert buildings == []

    async def test_delete_non_existing(self, building):
        with pytest.raises(BuildingNotFoundError):
            await buildings_service.delete(1)

    async def test_update(self, building):
        _building = await building(id=1)
        result = await buildings_service.update(
            1, {"country": "Anglia", "address": "Graniczna 11"}
        )
        assert result == {"id": 1}
        assert asdict(_building) == {
            "address": "Graniczna 11",
            "city": "Warszawa",
            "country": "Anglia",
            "county": "mazowieckie",
            "id": 1,
            "locals": [],
            "zip_code": "02-200",
        }

    async def test_buildings_update_non_existing(self):
        with pytest.raises(BuildingNotFoundError):
            await buildings_service.update(
                1, {"country": "Anglia", "address": "Graniczna 11"}
            )
