class Footprint:
    def __init__(self, name):
        self.name = name

        self.parameters = {}

        self.pad_masters = []
        self.pads = []
        self.tracks = []
        self.arcs = []
        self.component_body = None

        self.metadata = {}
