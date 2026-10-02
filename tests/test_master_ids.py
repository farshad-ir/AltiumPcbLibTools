from model.pad import Pad
from model.footprint import Footprint

from builder.master_builder import PadMasterBuilder
from writer.json_writer import JSONWriter


# --------------------------------------------------
# Create synthetic footprint
# --------------------------------------------------

footprint = Footprint("MASTER_ID_TEST")


# --------------------------------------------------
# Pad 1
# Circle 2.4
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
# Same master as Pad 1
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
# Different circle geometry
#
# IMPORTANT:
# Same shape, but different size.
# This must create another master.
# --------------------------------------------------

pad3 = Pad()

pad3.designator = "3"

pad3.shape = "circle"

pad3.size = {
    "diameter": 3.5
}

pad3.position = {
    "x": 10,
    "y": 0
}

pad3.layer = "TopLayer"

footprint.pads.append(pad3)


# --------------------------------------------------
# Pad 4
# Rectangle
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
# Build masters
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
    "master_id_test.json"
)
