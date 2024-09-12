from pathlib import Path
from typing import Tuple


def _load_joule(path: Path) -> float:
    s = _read_file(path)
    (value, unit) = _parse_data(s)
    assert unit == "J"
    return value


def _load_mass(path: Path) -> float:
    s = _read_file(path)
    (value, unit) = _parse_data(s)
    assert unit == "gCO2eq"
    return value


def _load_cycle_intensity(path: Path) -> float:
    s = _read_file(path)
    (value, unit) = _parse_data(s)
    assert unit == "pg/cycle"
    return value


def _load_intensity(path: Path) -> float:
    s = _read_file(path)
    (value, unit) = _parse_data(s)
    assert unit == "gCO2eq/kWh"
    return value


def _load_efficiency(path: Path) -> float:
    s = _read_file(path)
    value = float(s[:-1]) / 100.0
    unit = s[-1]
    assert unit == "%"
    return value


def _read_file(path: Path) -> str:
    with open(path, "r", encoding="UTF-8") as f:
        s = f.read()
    return s


def _parse_data(data: str) -> Tuple[float, str]:
    [value, unit] = data.split()
    value = float(value)
    return (value, unit)
