import pytest

from mcollector.domain.models import Address, Building, CircuitMeasurementData, Local


@pytest.fixture
def address():
    return Address(
        country="Polska",
        address="Towarowa 365",
        zip_code="02-200",
        city="Warszawa",
        county="mazowieckie",
    )


@pytest.fixture
def building(address):
    return Building(address)


@pytest.fixture
def local():
    return Local(7)


@pytest.fixture
def c_meas_data():
    return CircuitMeasurementData(
        device="B-16", i_n=16.0, u_n=230.0, i_off=80.0, z_m=0.44, z_s=2.88
    )
