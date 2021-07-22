from mcollector.generic_repository import GenericRepository
from mcollector.locations.models import Building


class BuildingsRepository(GenericRepository):
    model = Building
