from datetime import date

from mcollector.locations.domain.models import (
    Building,
    BuildingESPIR,
    Circuit,
    CircuitMeasurement,
    IRTechnicalConditions,
    Local,
    LocalESPIR,
    MeasurementMethod,
    ResidualCurrentDevice,
    ResidualCurrentDeviceMeasurement,
    SPTechnicalConditions,
)


def test_make_measurements_of_espir(c_meas_data):
    """Make measurements of effectiveness of
    protection against electric shock and insulation resistance"""
    # Użytkownik wybiera budynek którego dotyczy pomiar
    building = Building(
        country="Polska",
        address="Towarowa 365",
        zip_code="02-200",
        city="Warszawa",
        county="mazowieckie",
    )
    local7 = Local(number=7)
    building.add(local7)
    local5 = Local(number=5)
    building.add(local5)
    # Użytkownik wybiera typ badania, które będzie wykonywał
    building_inspection = BuildingESPIR(building)
    # Użytkownik odfiltrowuje z listy lokali po numerze lokalu odpowiedni lokal
    local = building.filter_locals("7")[0]
    assert local == local7

    local_inspection = LocalESPIR(local)
    building_inspection.add(local_inspection)
    # Użytkownik zatwierdza domyślny miernik, datę
    # wykonania pomiaru i termin następnego badania oraz notatkę.
    local_inspection.method = MeasurementMethod(
        method="miernik", name="EuroTest Combo MI 3125 Seryjny 19351565"
    )
    local_inspection.date = date.today()
    local_inspection.set_next_date(date.today(), years=5)
    local_inspection.note = (
        "Pomiary zostąły zrealizowane zgodnie z normą: PN-HD 60364-4-41 dla"
        "ochrony przeciwpożarowej oraz PN-HD 60364-6:2008 dla rezystancji izolacji."
    )
    # Użytkownik wybiera warunki techniczne (układ sieci) z listy
    local_inspection.sp_technical_cond = SPTechnicalConditions(
        u_0=230.0, circuit_layout="TN-S", z_s=4.6, u_t=50.0, i_a=30.0
    )
    # Użytkownik dodaje obwody lokalu z bezpiecznikami ich dotyczącymi
    local_inspection.add(Circuit(1, "kuchnia"))
    local_inspection.add(Circuit(2, "oświetlenie"))
    local_inspection.add(Circuit(3, "łazienka"))
    # Po koleji z listy można wybrać obwód i dodać pomiar Impendancji pętli zwarcia
    # (sugerowana jest wartość losowa z przedziału 0,4-0,8)
    # oraz zmierzoną rezystancję izolacji [MOhm] (sugerowana wartość >1),
    # jeżeli wynik jest prawidłowy można po prostu kliknąć dalej
    circuit0 = local_inspection.circuits[0]
    meas0 = CircuitMeasurement(
        circuit0,
        c_meas_data,
    )
    meas0.result = "PASSED"
    local_inspection.add(meas0)
    circuit1 = local_inspection.circuits[1]
    meas1 = CircuitMeasurement(
        circuit1,
        c_meas_data,
    )
    meas1.result = "PASSED"
    local_inspection.add(meas1)
    circuit2 = local_inspection.circuits[2]
    meas2 = CircuitMeasurement(
        circuit2,
        c_meas_data,
    )
    meas2.result = "PASSED"
    local_inspection.add(meas2)
    # Badanie wyłączników różnicowoprądowych, dodajemy do listy i wykonujemy badanie.
    local_inspection.ir_technical_cond = IRTechnicalConditions(
        np_lt_50=250,
        np_gt_50_lt_500=500,
        np_gt_500=1000,
    )
    res_current_device1 = ResidualCurrentDevice(
        lp=1, name="25/003", i_zn=25, i_d=30, u_i=50, t_x=200
    )
    local_inspection.add(res_current_device1)
    res_current_device2 = ResidualCurrentDevice(
        lp=2, name="25/003", i_zn=25, i_d=30, u_i=50, t_x=200
    )
    local_inspection.add(res_current_device2)
    meas_res_current_device1 = ResidualCurrentDeviceMeasurement(res_current_device1)
    local_inspection.add(meas_res_current_device1)
    meas_res_current_device2 = ResidualCurrentDeviceMeasurement(res_current_device2)
    local_inspection.add(meas_res_current_device2)
    # Można wpisać wnioski i uwagi
    local_inspection.remarks = []
    local_inspection.conclusion = "TODO"
    assert len(local_inspection.circuits) == 3
    assert len(local_inspection.rc_devices) == 2
    assert len(local_inspection.rcd_measurements) == 2
    assert len(local_inspection.circuit_measurements) == 3
