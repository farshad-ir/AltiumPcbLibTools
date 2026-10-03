import json
import sys
from pathlib import Path

from extractor.reader import PcbReader
from extractor.extractor import Extractor

from writer.json_writer import JSONWriter
from writer.pad_roundtrip import PadRoundTripWriter
from writer.full_roundtrip import FullRoundTripWriter


def usage():
    print()
    print("Usage:")
    print()
    print(
        "  draw_json "
        "<input.PcbLib> <footprint> <output.json>"
    )
    print(
        "  transform_pads "
        "<input.json> <output.PcbLib>"
    )
    print(
        "  transform_full "
        "<input.json> <output.PcbLib>"
    )
    print()


def draw_json(args):

    if len(args) != 3:
        usage()
        return 1

    input_file = args[0]
    footprint_name = args[1]
    output_file = args[2]

    pcb = PcbReader(input_file).read()

    footprint = Extractor().extract(
        pcb,
        footprint_name,
    )

    if footprint is None:
        print("Footprint not found")
        return 1

    JSONWriter().write(
        footprint,
        output_file,
    )

    print("Created:", output_file)
    return 0


def transform_pads(args):

    if len(args) != 2:
        usage()
        return 1

    with open(args[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    PadRoundTripWriter().write(
        data,
        args[1],
    )

    print("Created:", args[1])
    return 0


def transform_full(args):

    if len(args) != 2:
        usage()
        return 1

    with open(args[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    FullRoundTripWriter().write(
        data,
        args[1],
    )

    print("Created:", args[1])
    return 0


def main():

    if len(sys.argv) < 2:
        usage()
        return 1

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "draw_json":
        return draw_json(args)

    if command == "transform_pads":
        return transform_pads(args)

    if command == "transform_full":
        return transform_full(args)

    usage()
    return 1


if __name__ == "__main__":
    sys.exit(main())
