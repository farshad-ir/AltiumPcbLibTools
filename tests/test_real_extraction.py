from extractor.reader import PcbReader
from extractor.extractor import Extractor
from writer.json_writer import JSONWriter


SOURCE = "/home/farshad/AltiumTools/Test_Copy.PcbLib"
FOOTPRINT = "CAP_BOSHKE_SMD"
OUTPUT = "cap_boshke_smd.json"


def main():
    reader = PcbReader(SOURCE)
    source = reader.read()

    footprint = Extractor().extract(
        source,
        FOOTPRINT,
    )

    print("Footprint:", footprint.name)
    print("Parameters:", footprint.parameters)
    print("Pad masters:", len(footprint.pad_masters))
    print("Pads:", len(footprint.pads))
    print("Tracks:", len(footprint.tracks))
    print("Arcs:", len(footprint.arcs))
    print("Component body:", footprint.component_body)

    JSONWriter().write(
        footprint,
        OUTPUT,
    )

    print("JSON:", OUTPUT)


if __name__ == "__main__":
    main()
