import argparse
from pathlib import Path

from src.altiumpcblibtools.extractor import (
    extract_footprint,
    save_json,
)


def main():

    parser = argparse.ArgumentParser(
        description="Extract an Altium PcbLib footprint to JSON."
    )

    parser.add_argument(
        "pcb_library",
        help="Path to the .PcbLib file"
    )

    parser.add_argument(
        "footprint",
        help="Footprint name"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output JSON file"
    )

    args = parser.parse_args()

    data = extract_footprint(
        args.pcb_library,
        args.footprint
    )

    if args.output:
        output = Path(args.output)
    else:
        output = Path(
            f"{args.footprint}.json"
        )

    save_json(
        data,
        output
    )

    print()
    print("EXTRACTION SUCCESSFUL")
    print()
    print("Library:")
    print(data["source"]["library"])
    print()
    print("Footprint:")
    print(data["source"]["footprint"])
    print()
    print("Summary:")
    print(
        data["summary"]
    )
    print()
    print("JSON:")
    print(output.resolve())


if __name__ == "__main__":
    main()
