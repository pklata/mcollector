from datetime import date

from mcollector_tests.factories import BuildingFactory

from mcollector.domain.models import (
    BuildingESPIR,
    Circuit,
    CircuitMeasurement,
    Local,
    LocalESPIR,
    ResidualCurrentDevice,
    ResidualCurrentDeviceMeasurement,
)


class TestBuildings:
    def test_local_can_be_add_to_building(self, local):
        building = BuildingFactory()
        building.add(local)
        assert building.locals == [local]

    def test_locals_in_building_are_sorted(self):
        building = BuildingFactory()
        local7 = Local(7)
        local8 = Local(8)
        building.add(local7)
        building.add(local8)
        assert building.locals == [local7, local8]

    def test_filter_out_local_number_7(self):
        building = BuildingFactory()
        local7 = Local(7)
        local8 = Local(8)
        building.add(local7)
        building.add(local8)
        _locals = building.filter_locals("7")
        assert _locals == [local7]

    def test_filter_out_local_number_7_17_71(self):
        building = BuildingFactory()
        local7 = Local(7)
        local17 = Local(17)
        local71 = Local(71)
        local8 = Local(8)
        building.add(local7)
        building.add(local17)
        building.add(local71)
        building.add(local8)
        _locals = building.filter_locals("7")
        assert _locals == [local7, local17, local71]


class TestBuildingESPIR:
    def test_adding_local_inspection(self, local):
        building = BuildingFactory()
        b_insp = BuildingESPIR(building)
        l_insp = LocalESPIR(local)
        b_insp.add(l_insp)
        assert b_insp.local_inspections == [l_insp]

    def test_local_inspection_are_sorted(self, local):
        building = BuildingFactory()
        b_insp = BuildingESPIR(building)
        local7 = Local(7)
        local8 = Local(8)
        l_insp1 = LocalESPIR(local8)
        l_insp2 = LocalESPIR(local7)
        b_insp.add(l_insp1)
        b_insp.add(l_insp2)
        assert b_insp.local_inspections == [l_insp2, l_insp1]


class TestLocalESPIR:
    def test_set_next_date_3_years_from_fixed_date(self, local):
        l_insp = LocalESPIR(local)
        l_insp.set_next_date(date(year=2020, month=7, day=21), years=3)
        assert l_insp.next_date == date(year=2023, month=7, day=21)

    def test_set_next_fixed_date(self, local):
        l_insp = LocalESPIR(local)
        l_insp.set_next_date(date(year=2020, month=7, day=21))
        assert l_insp.next_date == date(year=2020, month=7, day=21)

    def test_add_circuit(self, local):
        l_insp = LocalESPIR(local)
        circ1 = Circuit(1, "kuchnia")
        l_insp.add(circ1)
        assert circ1 in l_insp.circuits

    def test_circuits_are_sorted(self, local):
        l_insp = LocalESPIR(local)
        circ1 = Circuit(1, "oświetlenie")
        circ2 = Circuit(2, "kuchnia")
        l_insp.add(circ2)
        l_insp.add(circ1)
        assert l_insp.circuits == [circ1, circ2]

    def test_add_circuit_measurement(self, local, c_meas_data):
        l_insp = LocalESPIR(local)
        circ1 = Circuit(1, "kuchnia")
        meas1 = CircuitMeasurement(circ1, c_meas_data)
        l_insp.add(meas1)
        assert meas1 in l_insp.circuit_measurements

    def test_circuit_measurements_are_sorted(self, local, c_meas_data):
        l_insp = LocalESPIR(local)
        circ1 = Circuit(1, "oświetlenie")
        circ2 = Circuit(2, "kuchnia")
        meas2 = CircuitMeasurement(
            circ1,
            c_meas_data,
        )
        meas1 = CircuitMeasurement(
            circ2,
            c_meas_data,
        )
        l_insp.add(meas1)
        l_insp.add(meas2)
        assert l_insp.circuit_measurements == [meas2, meas1]

    def test_add_residual_current_device(self, local):
        l_insp = LocalESPIR(local)
        rcd1 = ResidualCurrentDevice(
            lp=1, name="25/003", i_zn=25, i_d=30, u_i=50, t_x=200
        )
        l_insp.add(rcd1)
        assert rcd1 in l_insp.rc_devices

    def test_residual_current_devices_are_sorted(self, local):
        l_insp = LocalESPIR(local)
        rcd1 = ResidualCurrentDevice(
            lp=2, name="25/003", i_zn=25, i_d=30, u_i=50, t_x=200
        )
        l_insp.add(rcd1)
        rcd2 = ResidualCurrentDevice(
            lp=1, name="25/003", i_zn=25, i_d=30, u_i=50, t_x=200
        )
        l_insp.add(rcd2)
        assert l_insp.rc_devices == [rcd2, rcd1]

    def test_add_residual_current_device_measurement(self, local):
        l_insp = LocalESPIR(local)
        rcd1 = ResidualCurrentDevice(
            lp=1, name="25/003", i_zn=25, i_d=30, u_i=50, t_x=200
        )
        rcd1_meas = ResidualCurrentDeviceMeasurement(rcd1)
        l_insp.add(rcd1_meas)
        assert rcd1_meas in l_insp.rcd_measurements

    def test_residual_current_device_measurements_are_sorted(self, local):
        l_insp = LocalESPIR(local)
        rcd1 = ResidualCurrentDevice(
            lp=2, name="25/003", i_zn=25, i_d=30, u_i=50, t_x=200
        )
        rcd1_meas = ResidualCurrentDeviceMeasurement(rcd1)
        l_insp.add(rcd1_meas)
        rcd2 = ResidualCurrentDevice(
            lp=1, name="25/003", i_zn=25, i_d=30, u_i=50, t_x=200
        )
        rcd2_meas = ResidualCurrentDeviceMeasurement(rcd2)
        l_insp.add(rcd2_meas)
        assert l_insp.rcd_measurements == [rcd2_meas, rcd1_meas]
