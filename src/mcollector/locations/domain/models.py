from dataclasses import dataclass, field
from datetime import date
from functools import singledispatchmethod
from typing import Any, List, Optional, Set


@dataclass(frozen=True)
class SPTechnicalConditions:
    """Technical conditions of electric grid for electric shock protection

    Attributes:
        U0 (float): Nominalne napięcie przewodu liniowego względem ziemi
        circuit_layout (str): Układ sieci
        Zs (float): Dopuszczalna Impedancja
        Ut (float): napięcie dotykowe
        Ia (float): Maks. dopuszczalny prąd wyłączenia
    """

    u_0: float
    circuit_layout: str
    z_s: float
    u_t: float
    i_a: float


@dataclass(frozen=True)
class IRTechnicalConditions:
    """
    Technical conditions of isolation resistance measurements
    Attributes:
        np_lt_50 (float): Un < 50V
        np_gt_50_lt_500 (float): 500V > Un >50V
        np_gt_500 (float): Un > 500V
    """

    np_lt_50: float
    np_gt_50_lt_500: float
    np_gt_500: float


@dataclass
class Local:
    """Local where the part of inspection is taking place. Part of the building"""

    number: int


@dataclass(frozen=True)
class MeasurementMethod:
    method: str
    name: str


@dataclass
class Building:
    """Building where inspection is taking place"""

    id: Optional[int] = None
    country: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    locals: List[Local] = field(default_factory=list)

    def get_locals(self) -> List[Local]:
        return sorted(self.locals, key=lambda l: l.number)

    def add(self, local: Local) -> None:
        self.locals.append(local)

    def filter_locals(self, match: str) -> List[Local]:
        _locals = [local for local in self.locals if match in str(local.number)]
        return sorted(_locals, key=lambda l: l.number)


@dataclass(frozen=True)
class Circuit:
    lp: int
    name: str


@dataclass(frozen=True)
class CircuitMeasurementData:
    device: str
    i_n: float
    u_n: float
    i_off: float
    z_m: float
    z_s: float


class CircuitMeasurement:
    def __init__(self, circuit: Circuit, data: CircuitMeasurementData):
        self.circuit = circuit
        self.data = data
        self.result: Optional[str] = None


@dataclass(frozen=True)
class ResidualCurrentDevice:
    lp: int
    name: str
    i_zn: float
    i_d: float
    u_i: float
    t_x: float


class ResidualCurrentDeviceMeasurement:
    def __init__(self, device: ResidualCurrentDevice):
        self.device = device
        self.i_zn: float = 0
        self.u_i: float = 0
        self.t_x: float = 0
        self.valid: Optional[bool] = None
        self.result: Optional[str] = None


class LocalESPIR:
    """Electric shock protection
    and insulation resistance inspection taking place in local."""

    def __init__(self, local: Local):
        self.local = local
        self.next_date: Optional[date] = None
        self.note: str = ""
        self.sp_technical_cond: Optional[SPTechnicalConditions] = None
        self._circuits: Set[Circuit] = set()
        self._circuit_meas: Set[CircuitMeasurement] = set()
        self._rc_devices: Set[ResidualCurrentDevice] = set()
        self._rc_device_meas: Set[ResidualCurrentDeviceMeasurement] = set()

    def set_next_date(self, fixed_date: date, years: int = 0) -> None:
        self.next_date = fixed_date.replace(year=fixed_date.year + years)

    @singledispatchmethod
    def add(self, item: Any) -> None:
        raise NotImplementedError(f"Item {item} cannot be added to {self}")

    @add.register
    def _(self, circuit: Circuit) -> None:
        self._circuits.add(circuit)

    @add.register  # type: ignore[no-redef]
    def _(self, circuit_measurement: CircuitMeasurement) -> None:
        self._circuit_meas.add(circuit_measurement)

    @add.register  # type: ignore[no-redef]
    def _(self, rc_device: ResidualCurrentDevice) -> None:
        self._rc_devices.add(rc_device)

    @add.register  # type: ignore[no-redef]
    def _(self, rcd_measurement: ResidualCurrentDeviceMeasurement) -> None:
        self._rc_device_meas.add(rcd_measurement)

    @property
    def circuits(self) -> List[Circuit]:
        return sorted(self._circuits, key=lambda c: c.lp)

    @property
    def circuit_measurements(self) -> List[CircuitMeasurement]:
        return sorted(self._circuit_meas, key=lambda c: c.circuit.lp)

    @property
    def rc_devices(self) -> List[ResidualCurrentDevice]:
        return sorted(self._rc_devices, key=lambda r: r.lp)

    @property
    def rcd_measurements(self) -> List[ResidualCurrentDeviceMeasurement]:
        return sorted(self._rc_device_meas, key=lambda r: r.device.lp)


class BuildingESPIR:
    """Electric shock protection
    and insulation resistance inspection taking place in building."""

    def __init__(self, building: Building):
        self.building = building
        self._local_inspections: Set[LocalESPIR] = set()

    def add(self, inspection: LocalESPIR) -> None:
        self._local_inspections.add(inspection)

    @property
    def local_inspections(self) -> List[LocalESPIR]:
        return sorted(self._local_inspections, key=lambda i: i.local.number)
