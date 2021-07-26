from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory

from mcollector.errors import NotFoundError
from mcollector.locations.repository import BuildingsRepository


@pytest.mark.asyncio
async def test_buildings_list(session, building):
    building1 = building()
    building2 = building()
    session.add(building1)
    session.add(building2)
    buildings = await BuildingsRepository(session).list()
    assert buildings == [building1, building2]


@pytest.mark.asyncio
async def test_buildings_get(session, building):
    building1 = building(id=1)
    session.add(building1)
    session.commit()
    building_ = await BuildingsRepository(session).get(1)
    assert building_ == building1


@pytest.mark.asyncio
async def test_buildings_get_non_existing(session):
    with pytest.raises(NotFoundError):
        await BuildingsRepository(session).get(1)


@pytest.mark.asyncio
async def test_buildings_add(session):
    building1 = BuildingFactory()
    _id = await BuildingsRepository(session).add(asdict(building1))
    buildings = await BuildingsRepository(session).list()
    building1.id = _id
    assert _id == 1
    assert buildings == [building1]


@pytest.mark.asyncio
async def test_building_delete(session, building):
    session.add(building(id=1))
    session.commit()
    await BuildingsRepository(session).delete(1)
    buildings = await BuildingsRepository(session).list()
    assert buildings == []


@pytest.mark.asyncio
async def test_building_delete_non_existing(session, building):
    with pytest.raises(NotFoundError):
        await BuildingsRepository(session).delete(1)


@pytest.mark.asyncio
async def test_buildings_update(session, building):
    _building = building(id=1)
    session.add(_building)
    session.commit()
    _id = await BuildingsRepository(session).update(
        1, country="Anglia", address="Graniczna 11"
    )
    assert _id == 1
    assert asdict(_building) == {
        "address": "Graniczna 11",
        "city": "Warszawa",
        "country": "Anglia",
        "county": "mazowieckie",
        "id": 1,
        "locals": [],
        "zip_code": "02-200",
    }


@pytest.mark.asyncio
async def test_buildings_update_non_existing(session):
    with pytest.raises(NotFoundError):
        await BuildingsRepository(session).update(
            1, country="Anglia", address="Graniczna 11"
        )
