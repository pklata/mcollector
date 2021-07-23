from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory

from mcollector.errors import NotFoundError
from mcollector.locations import service


@pytest.mark.asyncio
class TestBuildingsService:
    async def test_list(self, nested_session, building):
        building1 = building()
        building2 = building()
        nested_session.add(building1)
        nested_session.add(building2)
        buildings = await service.list()
        assert buildings == [asdict(building1), asdict(building2)]

    async def test_get(self, nested_session, building):
        building1 = building(id=1)
        nested_session.add(building1)
        building_ = await service.get(1)
        assert building_ == asdict(building1)

    @pytest.mark.usefixtures("nested_session")
    async def test_get_non_existing(self):
        with pytest.raises(NotFoundError):
            await service.get(1)

    @pytest.mark.usefixtures("nested_session")
    async def test_add(self):
        building1 = BuildingFactory()
        result = await service.add(asdict(building1))
        buildings = await service.list()
        building1.id = result["id"]
        assert result == {"id": 1}
        assert buildings == [asdict(building1)]

    async def test_delete(self, building, nested_session):
        nested_session.add(building(id=1))
        await service.delete(1)
        buildings = await service.list()
        assert buildings == []

    @pytest.mark.usefixtures("nested_session")
    async def test_delete_non_existing(self):
        with pytest.raises(NotFoundError):
            await service.delete(1)

    async def test_update(self, nested_session, building):
        _building = building(id=1)
        nested_session.add(_building)
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

    @pytest.mark.usefixtures("nested_session")
    async def test_buildings_update_non_existing(self):
        with pytest.raises(NotFoundError):
            await service.update(1, {"country": "Anglia", "address": "Graniczna 11"})
