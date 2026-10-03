import sys
from pathlib import Path

from extractor.reader import PcbReader
from extractor.extractor import Extractor
from writer.json_writer import JSONWriter


def usage():
    print(
        "\nUsage:\n"
        "  json_export_cli.py <input.PcbLib> "
        "<footprint_name> <output.json>\n\n"
        "Example:\n"
        "  json_export_cli.py Test_Copy.PcbLib "
        "CAP_BOSHKE_SMD cap.json\n"
    )


def main():

    if len(sys.argv) != 4:
        usage()
        return 1

    input_file = Path(sys.argv[1])
    footprint_name = sys.argv[2]
    output_file = Path(sys.argv[3])

    if not input_file.exists():
        print("\nERROR:")
        print("Input PcbLib file was not found:")
        print(f"  {input_file}")
        print("\nPlease check the file path.\n")
        return 1

    if input_file.suffix.lower() != ".pcblib":
        print("\nERROR:")
        print("Input file must be an Altium PcbLib file:")
        print(f"  {input_file}")
        return 1

    try:
        print("Reading:", input_file)

        pcb = PcbReader(str(input_file)).read()

        footprint = Extractor().extract(
            pcb,
            footprint_name,
        )



        if footprint is None:
            print("\nERROR:")
            print("Footprint was not found in this PcbLib:")
            print(f"  {footprint_name}")
            print("\nPlease check the footprint name.\n")

            print("Available footprints:")
            for item in pcb.footprints:
                print(f"  {item.name}")

            return 1


        print("Extracted:", footprint.name)

        JSONWriter().write(
            footprint,
            str(output_file),
        )

        print("JSON created:", output_file)

    except ValueError as error:
        print("\nERROR:")
        print(error)
        print(
            "\nCheck the footprint name and try again.\n"
        )
        return 1

    except Exception as error:
        print("\nERROR:")
        print(error)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
