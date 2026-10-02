import sys
import types
from pathlib import Path


def load_pcblib_api():
    package_dir = (
        Path(__file__).resolve().parents[1]
        / "altium_monkey"
        / "src"
        / "py"
        / "altium_monkey"
    )

    package = types.ModuleType("altium_monkey")
    package.__path__ = [str(package_dir)]
    package.__package__ = "altium_monkey"

    sys.modules["altium_monkey"] = package

    from altium_monkey.altium_pcblib import AltiumPcbLib

    return AltiumPcbLib
