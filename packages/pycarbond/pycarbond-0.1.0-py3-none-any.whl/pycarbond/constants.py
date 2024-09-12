from pathlib import Path


CARBOND_DATA_PATH = Path("/var/carbond")
OPERATIONAL_PATH = CARBOND_DATA_PATH.joinpath("operational")
EMBODIED_PATH = CARBOND_DATA_PATH.joinpath("embodied")
BATTERY_TRACKER_PATH = CARBOND_DATA_PATH.joinpath("battery")

SYSTEM_INTENSITY_PATH = OPERATIONAL_PATH.joinpath("system-intensity")
GRID_INTENSITY_PATH = OPERATIONAL_PATH.joinpath("grid/intensity")
PSU_EFFICIENCY_PATH = OPERATIONAL_PATH.joinpath("PSU/efficiency")
PSU_INTENSITY_PATH = OPERATIONAL_PATH.joinpath("PSU/intensity")

BATTERY_EMBODIED_PATH = EMBODIED_PATH.joinpath("battery")
CPU_EMBODIED_PATH = EMBODIED_PATH.joinpath("cpu")
