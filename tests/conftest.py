import pytest

from mcollector.domain.models import Building, Local


@pytest.fixture
def building():
    return Building()


@pytest.fixture
def local():
    return Local()
