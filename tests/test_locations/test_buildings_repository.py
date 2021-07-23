from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory

from mcollector.errors import NotFoundError
from mcollector.locations.repository import BuildingsRepository


@pytest.mark.asyncio
async def test_buildings_list(nested_session, building):
    building1 = building()
    building2 = building()
    nested_session.add(building1)
    nested_session.add(building2)
    buildings = await BuildingsRepository(nested_session).list()
    assert buildings == [building1, building2]


@pytest.mark.asyncio
async def test_buildings_get(nested_session, building):
    building1 = building(id=1)
    nested_session.add(building1)
    building_ = await BuildingsRepository(nested_session).get(1)
    assert building_ == building1


@pytest.mark.asyncio
async def test_buildings_get_non_existing(nested_session):
    with pytest.raises(NotFoundError):
        await BuildingsRepository(nested_session).get(1)


@pytest.mark.asyncio
async def test_buildings_add(nested_session):
    building1 = BuildingFactory()
    _id = await BuildingsRepository(nested_session).add(asdict(building1))
    buildings = await BuildingsRepository(nested_session).list()
    building1.id = _id
    assert _id == 1
    assert buildings == [building1]


@pytest.mark.asyncio
async def test_building_delete(nested_session, building):
    nested_session.add(building(id=1))
    await BuildingsRepository(nested_session).delete(1)
    buildings = await BuildingsRepository(nested_session).list()
    assert buildings == []


@pytest.mark.asyncio
async def test_building_delete_non_existing(nested_session, building):
    with pytest.raises(NotFoundError):
        await BuildingsRepository(nested_session).delete(1)


@pytest.mark.asyncio
async def test_buildings_update(nested_session, building):
    _building = building(id=1)
    nested_session.add(_building)
    _id = await BuildingsRepository(nested_session).update(
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
async def test_buildings_update_non_existing(nested_session):
    with pytest.raises(NotFoundError):
        await BuildingsRepository(nested_session).update(
            1, country="Anglia", address="Graniczna 11"
        )
