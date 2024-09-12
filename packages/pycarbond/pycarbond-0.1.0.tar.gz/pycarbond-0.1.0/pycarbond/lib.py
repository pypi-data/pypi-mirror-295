import os
from pathlib import Path
import pycarbond.constants
from .fs import _load_cycle_intensity, _load_joule, _load_intensity, _load_mass, _load_efficiency


def load_system_intensity() -> float:
    """Loads the system intensity in ```g/kWh``` from carbond."""
    return _load_intensity(pycarbond.constants.SYSTEM_INTENSITY_PATH)


def load_grid_intensity() -> float:
    """Loads the grid intensity in ```g/kWh``` from carbond."""
    return _load_intensity(pycarbond.constants.GRID_INTENSITY_PATH)


def load_psu_efficiency() -> float:
    """Loads the psu efficiency from carbond."""
    return _load_efficiency(pycarbond.constants.PSU_EFFICIENCY_PATH)


def load_psu_intensity() -> float:
    """Loads the psu intensity in ```g/kWh``` from carbond."""
    return _load_intensity(pycarbond.constants.PSU_INTENSITY_PATH)


def load_cpu_embodied_intensity() -> float:
    """Loads the CPU embodied intensity in ```pg/cycle``` from carbond."""
    return _load_cycle_intensity(pycarbond.constants.CPU_EMBODIED_PATH)


def load_battery_intensity() -> float:
    """Loads the battery intensity in ```g/kWh``` from carbond."""
    total_energy = 0
    total_carbon = 0
    batteries = os.listdir(pycarbond.constants.BATTERY_TRACKER_PATH)
    if len(batteries) == 0:
        raise FileNotFoundError("No battery found")
    for bat in batteries:
        bat_path = Path(pycarbond.constants.BATTERY_TRACKER_PATH).joinpath(bat)
        total_energy += _load_joule(bat_path.joinpath("energy"))
        total_carbon += _load_mass(bat_path.joinpath("carbon"))
    total_energy = total_energy / 3_600_000
    if total_energy == 0:
        return 0.0
    return total_carbon / total_energy
