from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory

from mcollector.errors import NotFoundError
from mcollector.locations import service
from mcollector.locations.models import Building


@pytest.mark.asyncio
@pytest.mark.usefixtures("recreate_db")
class TestBuildingsService:
    async def test_list(self, building, session):
        building1 = building()
        building2 = building()
        session.add(building1)
        session.add(building2)
        await session.commit()
        buildings = await service.list()
        assert buildings == [asdict(building1), asdict(building2)]

    async def test_get(self, building, session):
        building1 = building(id=1)
        session.add(building1)
        await session.commit()
        building_ = await service.get(1)
        assert building_ == asdict(building1)

    async def test_get_non_existing(self):
        with pytest.raises(NotFoundError):
            await service.get(1)

    async def test_add(self):
        building1 = BuildingFactory()
        result = await service.add(asdict(building1))
        buildings = await service.list()
        building1.id = result["id"]
        assert result == {"id": 1}
        assert buildings == [asdict(building1)]

    async def test_delete(self, building, session):
        session.add(building(id=1))
        await session.commit()
        await service.delete(1)
        buildings = await service.list()
        assert buildings == []

    async def test_delete_non_existing(self):
        with pytest.raises(NotFoundError):
            await service.delete(1)

    async def test_update(self, session, building):
        session.add(building(id=1))
        await session.commit()
        result = await service.update(
            1, {"country": "Anglia", "address": "Graniczna 11"}
        )
        assert result == {"id": 1}
        assert await session.get(Building, 1) == Building(
            address="Graniczna 11",
            city="Warszawa",
            country="Anglia",
            county="mazowieckie",
            id=1,
            locals=[],
            zip_code="02-200",
        )

    async def test_buildings_update_non_existing(self):
        with pytest.raises(NotFoundError):
            await service.update(1, {"country": "Anglia", "address": "Graniczna 11"})
