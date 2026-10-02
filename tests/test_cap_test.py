from model.pad import Pad, PadMaster
from model.track import Track
from model.arc import Arc
from model.footprint import Footprint

from builder.master_builder import PadMasterBuilder
from writer.json_writer import JSONWriter

footprint = Footprint("CAP_TEST")
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

footprint.pads.append(pad1)

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

footprint.pads.append(pad2)

pad3 = Pad()

pad3.designator = "3"

pad3.shape = "rectangle"

pad3.size = {
    "width": 3,
    "height": 2
}

pad3.position = {
    "x": 10,
    "y": 0
}

footprint.pads.append(pad3)

track = Track()

track.layer = "TopLayer"

track.start = [0, 0]
track.end = [10, 0]

footprint.tracks.append(track)

arc = Arc()

arc.layer = "TopLayer"

arc.geometry = {
    "center": [5, 5],
    "radius": 2
}

footprint.arcs.append(arc)


builder = PadMasterBuilder()

masters = builder.build(
    footprint.pads
)

footprint.pad_masters = masters

writer = JSONWriter()

writer.write(
    footprint,
    "cap_test.json"
)
