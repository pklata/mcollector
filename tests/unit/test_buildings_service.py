from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory

from mcollector.locations import service
from mcollector.locations.repository import BuildingNotFoundError


@pytest.mark.asyncio
@pytest.mark.usefixtures("session")
class TestBuildingsService:
    async def test_list(self, building):
        building1 = await building()
        building2 = await building()
        buildings = await service.list()
        assert buildings == [asdict(building1), asdict(building2)]

    async def test_get(self, building):
        building1 = await building(id=1)
        building_ = await service.get(1)
        assert building_ == asdict(building1)

    async def test_get_non_existing(self):
        with pytest.raises(BuildingNotFoundError):
            await service.get(1)

    async def test_add(self):
        building1 = BuildingFactory()
        result = await service.add(asdict(building1))
        buildings = await service.list()
        building1.id = result["id"]
        assert result == {"id": 1}
        assert buildings == [asdict(building1)]

    async def test_delete(self, building):
        await building(id=1)
        await service.delete(1)
        buildings = await service.list()
        assert buildings == []

    async def test_delete_non_existing(self, building):
        with pytest.raises(BuildingNotFoundError):
            await service.delete(1)

    async def test_update(self, building):
        _building = await building(id=1)
        result = await service.update(
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
            await service.update(1, {"country": "Anglia", "address": "Graniczna 11"})
