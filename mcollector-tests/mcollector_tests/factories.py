import factory

from mcollector.locations.models import Building


class BuildingFactory(factory.Factory):
    class Meta:
        model = Building

    country = "Polska"
    address = "Towarowa 365"
    zip_code = "02-200"
    city = "Warszawa"
    county = "mazowieckie"
