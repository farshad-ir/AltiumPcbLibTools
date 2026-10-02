class PadMaster:
    def __init__(self):
        self.id = None
        self.shape = None
        self.size = {}
        self.layer = None
        self.options = {}


class Pad:
    def __init__(self):
        self.designator = None

        self.position = {
            "x": 0,
            "y": 0
        }

        self.shape = None
        self.size = {}
        self.layer = None
        self.rotation = 0

        self.options = {}
        self.override = {}

        self.master = None
