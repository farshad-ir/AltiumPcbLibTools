class Footprint:
    """
    مدل داخلی یک Footprint
    """

    def __init__(self, name):

        self.name = name

        # Pad system
        self.pad_masters = []
        self.pads = []

        # Other primitives
        self.tracks = []
        self.arcs = []

        # Future expansion
        self.component_body = None
        self.metadata = {}
