from pathlib import Path

from .altium_monkey_loader import load_pcblib_api


class PcbReader:

    def __init__(self, filename):
        self.filename = Path(filename)

    def read(self):
        AltiumPcbLib = load_pcblib_api()

        return AltiumPcbLib.from_file(self.filename)
