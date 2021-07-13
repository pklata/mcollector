import pytest
from sqlalchemy.future import select

from mcollector.domain import models


@pytest.mark.asyncio
async def test_building_mapping(session):
    await session.execute(
        "INSERT INTO buildings (id, country, address, zip_code, city, county, locals) "
        "VALUES "
        '(1, "Polska", "Towarowa 365", "02-200", "Warszawa", "mazowieckie", "[]");'
    )

    expected = [
        models.Building(
            id=1,
            country="Polska",
            address="Towarowa 365",
            zip_code="02-200",
            city="Warszawa",
            county="mazowieckie",
        ),
    ]
    result = await session.execute(select(models.Building))
    result = list(result.scalars())
    assert result == expected
