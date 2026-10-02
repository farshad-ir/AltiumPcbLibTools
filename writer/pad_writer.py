class PadWriter:

    def __init__(self, footprint):
        self.footprint = footprint

    def write(self, altium_footprint):

        masters = {}

        for master in self.footprint["pad_masters"]:
            masters[master["id"]] = master

        for pad in self.footprint["pads"]:

            master = masters[pad["master"]]

            options = master["options"]

            altium_footprint.add_pad(
                designator=pad["designator"],

                position_mils=(
                    self.to_mils(pad["position"]["x"]),
                    self.to_mils(pad["position"]["y"])
                ),

                width_mils=self.to_mils(
                    master["main"]["size"]["width"]
                ),

                height_mils=self.to_mils(
                    master["main"]["size"]["height"]
                ),

                layer=master["main"]["layer"],
                shape=master["shape"],

                rotation_degrees=pad["rotation"],

                hole_size_mils=self.to_mils(
                    options.get("hole_size", 0)
                ),

                plated=options.get("is_plated"),

                pad_mode=options.get("pad_mode"),

                top_shape=options.get("top_shape"),
                top_width_mils=self.to_mils(
                    options.get("top_width", 0)
                ),
                top_height_mils=self.to_mils(
                    options.get("top_height", 0)
                ),

                mid_shape=options.get("mid_shape"),
                mid_width_mils=self.to_mils(
                    options.get("mid_width", 0)
                ),
                mid_height_mils=self.to_mils(
                    options.get("mid_height", 0)
                ),

                bottom_shape=options.get("bot_shape"),
                bottom_width_mils=self.to_mils(
                    options.get("bot_width", 0)
                ),
                bottom_height_mils=self.to_mils(
                    options.get("bot_height", 0)
                )
            )

    def to_mils(self, value):
        return value / 10000.0
