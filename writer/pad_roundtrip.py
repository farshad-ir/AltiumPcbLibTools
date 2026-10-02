from extractor.altium_monkey_loader import load_pcblib_api

class PadRoundTripWriter:

    def __init__(self):
        pass

    def to_mils(self, value):
        if value is None:
            return 0
        return value / 10000.0

    def write(self, json_data, output_file):


        AltiumPcbLib = load_pcblib_api()
        pcb = AltiumPcbLib()

        fp_data = json_data["footprint"]

        fp = pcb.add_footprint(
            fp_data["name"],
            height=fp_data["parameters"].get("HEIGHT", "0mil"),
            description=fp_data["parameters"].get(
                "DESCRIPTION", ""
            ),
            item_guid=fp_data["parameters"].get(
                "ITEMGUID", ""
            ),
            revision_guid=fp_data["parameters"].get(
                "REVISIONGUID", ""
            ),
        )

        masters = {}

        for master in fp_data["pad_masters"]:
            masters[master["id"]] = master


        for pad in fp_data["pads"]:

            master = masters[pad["master"]]
            options = master["options"]

            size = master["main"]["size"]

            fp.add_pad(
                designator=pad["designator"],

                position_mils=(
                    self.to_mils(
                        pad["position"]["x"]
                    ),
                    self.to_mils(
                        pad["position"]["y"]
                    ),
                ),

                width_mils=self.to_mils(
                    size["width"]
                ),

                height_mils=self.to_mils(
                    size["height"]
                ),

                layer=master["main"]["layer"],

                shape=master["shape"],

                rotation_degrees=pad["rotation"],

                hole_size_mils=self.to_mils(
                    options.get("hole_size", 0)
                ),

                plated=options.get(
                    "is_plated"
                ),

                pad_mode = 1
		,





                top_shape=options.get(
                    "top_shape"
                ),

                top_width_mils=self.to_mils(
                    options.get("top_width", 0)
                ),

                top_height_mils=self.to_mils(
                    options.get("top_height", 0)
                ),
            )


        pcb.save(output_file)
