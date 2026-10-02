from model.pad import Pad
from model.track import Track
from model.arc import Arc
from model.footprint import Footprint

from builder.master_builder import PadMasterBuilder
from writer.json_writer import JSONWriter


# --------------------------------------------------
# Create synthetic footprint
# --------------------------------------------------

footprint = Footprint("CAP_TEST_2")


# --------------------------------------------------
# Pad 1
# Circle master
# --------------------------------------------------

pad1 = Pad()

pad1.designator = "1"

pad1.shape = "circle"

pad1.size = {
    "diameter": 2.4
}

pad1.position = {
    "x": 0,
    "y": 0
}

pad1.layer = "TopLayer"

footprint.pads.append(pad1)


# --------------------------------------------------
# Pad 2
# Same geometry as Pad 1
# Should inherit the same master
# --------------------------------------------------

pad2 = Pad()

pad2.designator = "2"

pad2.shape = "circle"

pad2.size = {
    "diameter": 2.4
}

pad2.position = {
    "x": 5,
    "y": 0
}

pad2.layer = "TopLayer"

footprint.pads.append(pad2)


# --------------------------------------------------
# Pad 3
# Same circle master
# But with an override
# --------------------------------------------------

pad3 = Pad()

pad3.designator = "3"

pad3.shape = "circle"

pad3.size = {
    "diameter": 2.4
}

pad3.position = {
    "x": 10,
    "y": 0
}

pad3.layer = "TopLayer"

pad3.rotation = 45

pad3.override = {
    "diameter": 3.0
}

footprint.pads.append(pad3)


# --------------------------------------------------
# Pad 4
# Different geometry
# Should create a second master
# --------------------------------------------------

pad4 = Pad()

pad4.designator = "4"

pad4.shape = "rectangle"

pad4.size = {
    "width": 3.0,
    "height": 2.0
}

pad4.position = {
    "x": 15,
    "y": 0
}

pad4.layer = "TopLayer"

footprint.pads.append(pad4)


# --------------------------------------------------
# Pad 5
# Same rectangle geometry as Pad 4
# Should inherit the rectangle master
# --------------------------------------------------

pad5 = Pad()

pad5.designator = "5"

pad5.shape = "rectangle"

pad5.size = {
    "width": 3.0,
    "height": 2.0
}

pad5.position = {
    "x": 20,
    "y": 0
}

pad5.layer = "TopLayer"

pad5.rotation = 90

footprint.pads.append(pad5)


# --------------------------------------------------
# Track 1
# --------------------------------------------------

track1 = Track()

track1.layer = "TopLayer"

track1.start = [0, 0]
track1.end = [20, 0]

track1.width = 0.3

footprint.tracks.append(track1)


# --------------------------------------------------
# Track 2
# --------------------------------------------------

track2 = Track()

track2.layer = "BottomLayer"

track2.start = [0, 5]
track2.end = [20, 5]

track2.width = 0.5

footprint.tracks.append(track2)


# --------------------------------------------------
# Arc 1
# --------------------------------------------------

arc1 = Arc()

arc1.layer = "TopLayer"

arc1.geometry = {
    "center": [5, 5],
    "radius": 2
}

footprint.arcs.append(arc1)


# --------------------------------------------------
# Arc 2
# --------------------------------------------------

arc2 = Arc()

arc2.layer = "BottomLayer"

arc2.geometry = {
    "center": [15, 5],
    "radius": 3
}

footprint.arcs.append(arc2)


# --------------------------------------------------
# Build Pad Masters
# --------------------------------------------------

builder = PadMasterBuilder()

masters = builder.build(
    footprint.pads
)

footprint.pad_masters = masters


# --------------------------------------------------
# Write JSON
# --------------------------------------------------

writer = JSONWriter()

writer.write(
    footprint,
    "cap_test_override.json"
)
