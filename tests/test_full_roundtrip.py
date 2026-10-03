import json

from writer.full_roundtrip import FullRoundTripWriter


INPUT = "F2904.json"
OUTPUT = "FULL_2904.PcbLib"


def main():

    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    writer = FullRoundTripWriter()

    writer.write(
        data,
        OUTPUT,
    )

    print("Created:", OUTPUT)


if __name__ == "__main__":
    main()
