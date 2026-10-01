#!/usr/bin/env python3

import argparse

from src.altiumpcblibtools.writer import apply_json


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Apply semantic footprint JSON "
            "to an Altium PcbLib footprint."
        )
    )

    parser.add_argument(
        "pcb_library",
        help="Source .PcbLib path",
    )

    parser.add_argument(
        "footprint",
        help="Footprint name",
    )

    parser.add_argument(
        "json_file",
        help="Semantic JSON file",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output .PcbLib path",
    )

    args = parser.parse_args()

    output = (
        args.output
        or f"{args.footprint}_modified.PcbLib"
    )

    apply_json(
        args.pcb_library,
        args.footprint,
        args.json_file,
        output,
    )


if __name__ == "__main__":
    main()
