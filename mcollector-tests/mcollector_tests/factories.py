from typing import Callable, Type

import factory

from mcollector.locations.models import Building


async def async_factory(factory_: Type[factory.Factory], session) -> Callable:
    async def inner(**kwargs):
        obj = factory_(**kwargs)
        session.add(obj)
        return obj

    return inner


class BuildingFactory(factory.Factory):
    class Meta:
        model = Building

    country = "Polska"
    address = "Towarowa 365"
    zip_code = "02-200"
    city = "Warszawa"
    county = "mazowieckie"
