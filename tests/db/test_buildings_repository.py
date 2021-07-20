from dataclasses import asdict

import pytest
from mcollector_tests.factories import BuildingFactory

from mcollector.repository.buildings_repository import (
    BuildingNotFoundError,
    BuildingsRepository,
)


@pytest.mark.asyncio
async def test_buildings_list(session, building):
    building1 = await building()
    building2 = await building()
    buildings = await BuildingsRepository(session).list()
    assert buildings == [building1, building2]


@pytest.mark.asyncio
async def test_buildings_get(session, building):
    building1 = await building(id=1)
    building_ = await BuildingsRepository(session).get(1)
    assert building_ == building1


@pytest.mark.asyncio
async def test_buildings_get_non_existing(session):
    with pytest.raises(BuildingNotFoundError):
        await BuildingsRepository(session).get(1)


@pytest.mark.asyncio
async def test_buildings_add(session):
    building1 = BuildingFactory()
    _id = await BuildingsRepository(session).add(building1)
    buildings = await BuildingsRepository(session).list()
    assert _id == 1
    assert buildings == [building1]


@pytest.mark.asyncio
async def test_building_delete(session, building):
    await building(id=1)
    await BuildingsRepository(session).delete(1)
    buildings = await BuildingsRepository(session).list()
    assert buildings == []


@pytest.mark.asyncio
async def test_building_delete_non_existing(session, building):
    with pytest.raises(BuildingNotFoundError):
        await BuildingsRepository(session).delete(1)


@pytest.mark.asyncio
async def test_buildings_update(session, building):
    _building = await building(id=1)
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
    with pytest.raises(BuildingNotFoundError):
        await BuildingsRepository(session).update(
            1, country="Anglia", address="Graniczna 11"
        )
