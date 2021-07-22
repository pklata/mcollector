# from datetime import date

#
# from mcollector.locations.models import (
#     Building,
#     BuildingESPIR,
#     Circuit,
#     CircuitMeasurement,
#     IRTechnicalConditions,
#     Local,
#     LocalESPIR,
#     MeasurementMethod,
#     ResidualCurrentDevice,
#     ResidualCurrentDeviceMeasurement,
#     SPTechnicalConditions,
# )
# @dataclass(frozen=True)
# class SPTechnicalConditions:
#     """Technical conditions of electric grid for electric shock protection
#
#     Attributes:
#         U0 (float): Nominalne napięcie przewodu liniowego względem ziemi
#         circuit_layout (str): Układ sieci
#         Zs (float): Dopuszczalna Impedancja
#         Ut (float): napięcie dotykowe
#         Ia (float): Maks. dopuszczalny prąd wyłączenia
#     """
#
#     u_0: float
#     circuit_layout: str
#     z_s: float
#     u_t: float
#     i_a: float
#
#
# @dataclass(frozen=True)
# class IRTechnicalConditions:
#     """
#     Technical conditions of isolation resistance measurements
#     Attributes:
#         np_lt_50 (float): Un < 50V
#         np_gt_50_lt_500 (float): 500V > Un >50V
#         np_gt_500 (float): Un > 500V
#     """
#
#     np_lt_50: float
#     np_gt_50_lt_500: float
#     np_gt_500: float
#
# @dataclass(frozen=True)
# class MeasurementMethod:
#     method: str
#     name: str
#
# @dataclass(frozen=True)
# class Circuit:
#     lp: int
#     name: str
#
#
# @dataclass(frozen=True)
# class CircuitMeasurementData:
#     device: str
#     i_n: float
#     u_n: float
#     i_off: float
#     z_m: float
#     z_s: float
#
#
# class CircuitMeasurement:
#     def __init__(self, circuit: Circuit, data: CircuitMeasurementData):
#         self.circuit = circuit
#         self.data = data
#         self.result: Optional[str] = None
#
#
# @dataclass(frozen=True)
# class ResidualCurrentDevice:
#     lp: int
#     name: str
#     i_zn: float
#     i_d: float
#     u_i: float
#     t_x: float
#
#
# class ResidualCurrentDeviceMeasurement:
#     def __init__(self, device: ResidualCurrentDevice):
#         self.device = device
#         self.i_zn: float = 0
#         self.u_i: float = 0
#         self.t_x: float = 0
#         self.valid: Optional[bool] = None
#         self.result: Optional[str] = None
#
#
# class LocalESPIR:
#     """Electric shock protection
#     and insulation resistance inspection taking place in local."""
#
#     def __init__(self, local: Local):
#         self.local = local
#         self.next_date: Optional[date] = None
#         self.note: str = ""
#         self.sp_technical_cond: Optional[SPTechnicalConditions] = None
#         self._circuits: Set[Circuit] = set()
#         self._circuit_meas: Set[CircuitMeasurement] = set()
#         self._rc_devices: Set[ResidualCurrentDevice] = set()
#         self._rc_device_meas: Set[ResidualCurrentDeviceMeasurement] = set()
#
#     def set_next_date(self, fixed_date: date, years: int = 0) -> None:
#         self.next_date = fixed_date.replace(year=fixed_date.year + years)
#
#     @singledispatchmethod
#     def add(self, item: Any) -> None:
#         raise NotImplementedError(f"Item {item} cannot be added to {self}")
#
#     @add.register
#     def _(self, circuit: Circuit) -> None:
#         self._circuits.add(circuit)
#
#     @add.register  # type: ignore[no-redef]
#     def _(self, circuit_measurement: CircuitMeasurement) -> None:
#         self._circuit_meas.add(circuit_measurement)
#
#     @add.register  # type: ignore[no-redef]
#     def _(self, rc_device: ResidualCurrentDevice) -> None:
#         self._rc_devices.add(rc_device)
#
#     @add.register  # type: ignore[no-redef]
#     def _(self, rcd_measurement: ResidualCurrentDeviceMeasurement) -> None:
#         self._rc_device_meas.add(rcd_measurement)
#
#     @property
#     def circuits(self) -> List[Circuit]:
#         return sorted(self._circuits, key=lambda c: c.lp)
#
#     @property
#     def circuit_measurements(self) -> List[CircuitMeasurement]:
#         return sorted(self._circuit_meas, key=lambda c: c.circuit.lp)
#
#     @property
#     def rc_devices(self) -> List[ResidualCurrentDevice]:
#         return sorted(self._rc_devices, key=lambda r: r.lp)
#
#     @property
#     def rcd_measurements(self) -> List[ResidualCurrentDeviceMeasurement]:
#         return sorted(self._rc_device_meas, key=lambda r: r.device.lp)
#
#
# class BuildingESPIR:
#     """Electric shock protection
#     and insulation resistance inspection taking place in building."""
#
#     def __init__(self, building: Building):
#         self.building = building
#         self._local_inspections: Set[LocalESPIR] = set()
#
#     def add(self, inspection: LocalESPIR) -> None:
#         self._local_inspections.add(inspection)
#
#     @property
#     def local_inspections(self) -> List[LocalESPIR]:
#         return sorted(self._local_inspections, key=lambda i: i.local.number)


# def test_make_measurements_of_espir(c_meas_data):
#     """Make measurements of effectiveness of
#     protection against electric shock and insulation resistance"""
#     # Użytkownik wybiera budynek którego dotyczy pomiar
#     building = Building(
#         country="Polska",
#         address="Towarowa 365",
#         zip_code="02-200",
#         city="Warszawa",
#         county="mazowieckie",
#     )
#     local7 = Local(number=7)
#     building.add(local7)
#     local5 = Local(number=5)
#     building.add(local5)
#     # Użytkownik wybiera typ badania, które będzie wykonywał
#     building_inspection = BuildingESPIR(building)
#     # Użytkownik odfiltrowuje z listy lokali po numerze lokalu odpowiedni lokal
#     local = building.filter_locals("7")[0]
#     assert local == local7
#
#     local_inspection = LocalESPIR(local)
#     building_inspection.add(local_inspection)
#     # Użytkownik zatwierdza domyślny miernik, datę
#     # wykonania pomiaru i termin następnego badania oraz notatkę.
#     local_inspection.method = MeasurementMethod(
#         method="miernik", name="EuroTest Combo MI 3125 Seryjny 19351565"
#     )
#     local_inspection.date = date.today()
#     local_inspection.set_next_date(date.today(), years=5)
#     local_inspection.note = (
#         "Pomiary zostąły zrealizowane zgodnie z normą: PN-HD 60364-4-41 dla"
#         "ochrony przeciwpożarowej oraz PN-HD 60364-6:2008 dla rezystancji izolacji."
#     )
#     # Użytkownik wybiera warunki techniczne (układ sieci) z listy
#     local_inspection.sp_technical_cond = SPTechnicalConditions(
#         u_0=230.0, circuit_layout="TN-S", z_s=4.6, u_t=50.0, i_a=30.0
#     )
#     # Użytkownik dodaje obwody lokalu z bezpiecznikami ich dotyczącymi
#     local_inspection.add(Circuit(1, "kuchnia"))
#     local_inspection.add(Circuit(2, "oświetlenie"))
#     local_inspection.add(Circuit(3, "łazienka"))
#     # Po koleji z listy można wybrać obwód i dodać pomiar Impendancji pętli zwarcia
#     # (sugerowana jest wartość losowa z przedziału 0,4-0,8)
#     # oraz zmierzoną rezystancję izolacji [MOhm] (sugerowana wartość >1),
#     # jeżeli wynik jest prawidłowy można po prostu kliknąć dalej
#     circuit0 = local_inspection.circuits[0]
#     meas0 = CircuitMeasurement(
#         circuit0,
#         c_meas_data,
#     )
#     meas0.result = "PASSED"
#     local_inspection.add(meas0)
#     circuit1 = local_inspection.circuits[1]
#     meas1 = CircuitMeasurement(
#         circuit1,
#         c_meas_data,
#     )
#     meas1.result = "PASSED"
#     local_inspection.add(meas1)
#     circuit2 = local_inspection.circuits[2]
#     meas2 = CircuitMeasurement(
#         circuit2,
#         c_meas_data,
#     )
#     meas2.result = "PASSED"
#     local_inspection.add(meas2)
#     # Badanie wyłączników różnicowoprądowych, dodajemy do listy i wykonujemy badanie.
#     local_inspection.ir_technical_cond = IRTechnicalConditions(
#         np_lt_50=250,
#         np_gt_50_lt_500=500,
#         np_gt_500=1000,
#     )
#     res_current_device1 = ResidualCurrentDevice(
#         lp=1, name="25/003", i_zn=25, i_d=30, u_i=50, t_x=200
#     )
#     local_inspection.add(res_current_device1)
#     res_current_device2 = ResidualCurrentDevice(
#         lp=2, name="25/003", i_zn=25, i_d=30, u_i=50, t_x=200
#     )
#     local_inspection.add(res_current_device2)
#     meas_res_current_device1 = ResidualCurrentDeviceMeasurement(res_current_device1)
#     local_inspection.add(meas_res_current_device1)
#     meas_res_current_device2 = ResidualCurrentDeviceMeasurement(res_current_device2)
#     local_inspection.add(meas_res_current_device2)
#     # Można wpisać wnioski i uwagi
#     local_inspection.remarks = []
#     local_inspection.conclusion = "TODO"
#     assert len(local_inspection.circuits) == 3
#     assert len(local_inspection.rc_devices) == 2
#     assert len(local_inspection.rcd_measurements) == 2
#     assert len(local_inspection.circuit_measurements) == 3
