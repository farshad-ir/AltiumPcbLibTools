class PadMaster:
    def __init__(self):
        # Main
        self.shape = None
        self.size = None
        self.layer = None

        # Options
        self.options = {}


class Pad:
    def __init__(self):
        # Instance data
        self.designator = None
        self.position = None
        self.rotation = None

        # اتصال به Master
        self.master = None

        # موارد خاص این Pad
        self.override = {}

class Track:
    def __init__(self):
        self.layer = None
        self.start = None
        self.end = None
        self.width = None
        self.options = {}


class Arc:
    def __init__(self):
        self.layer = None
        self.geometry = {}
        self.options = {}


class Footprint:
    def __init__(self, name):
        self.name = name

        self.pad_masters = []
        self.pads = []

        self.tracks = []
        self.arcs = []


