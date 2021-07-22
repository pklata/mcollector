from mcollector_tests.factories import BuildingFactory

from mcollector.locations.models import Local


class TestBuildings:
    def test_local_can_be_add_to_building(self, local):
        building = BuildingFactory()
        building.add(local)
        assert building.locals == [local]

    def test_locals_in_building_are_sorted(self):
        building = BuildingFactory()
        local7 = Local(number=7)
        local8 = Local(number=8)
        building.add(local7)
        building.add(local8)
        assert building.locals == [local7, local8]

    def test_filter_out_local_number_7(self):
        building = BuildingFactory()
        local7 = Local(number=7)
        local8 = Local(number=8)
        building.add(local7)
        building.add(local8)
        _locals = building.filter_locals("7")
        assert _locals == [local7]

    def test_filter_out_local_number_7_17_71(self):
        building = BuildingFactory()
        local7 = Local(number=7)
        local17 = Local(number=17)
        local71 = Local(number=71)
        local8 = Local(number=8)
        building.add(local7)
        building.add(local17)
        building.add(local71)
        building.add(local8)
        _locals = building.filter_locals("7")
        assert _locals == [local7, local17, local71]
