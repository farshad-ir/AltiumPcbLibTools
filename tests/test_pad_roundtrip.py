import json

from writer.pad_roundtrip import PadRoundTripWriter


INPUT = "smd4.json"
OUTPUT = "PSMD4.PcbLib"


def main():

    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    writer = PadRoundTripWriter()

    writer.write(
        data,
        OUTPUT,
    )

    print("Created:", OUTPUT)


if __name__ == "__main__":
    main()
