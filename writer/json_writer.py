import json


class JSONWriter:

    def write(self, footprint, filename):

        data = self.convert_footprint(footprint)

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    def convert_footprint(self, footprint):

        return {
            "footprint": {
                "name": footprint.name,

                "pad_masters": [
                    self.convert_master(master)
                    for master in footprint.pad_masters
                ],

                "pads": [
                    self.convert_pad(pad)
                    for pad in footprint.pads
                ],

                "tracks": [
                    self.convert_track(track)
                    for track in footprint.tracks
                ],

                "arcs": [
                    self.convert_arc(arc)
                    for arc in footprint.arcs
                ]
            }
        }

    def convert_master(self, master):

        return {
            "id": master.id,

            "shape": master.shape,

            "main": {
                "size": master.size,
                "layer": master.layer
            },

            "options": master.options
        }

    def convert_pad(self, pad):

        return {
            "designator": pad.designator,

            "master": self.get_master_reference(
                pad.master
            ),

            "position": pad.position,

            "rotation": pad.rotation,

            "override": pad.override
        }

    def get_master_reference(self, master):

        if master is None:
            return None

        return master.id

    def convert_track(self, track):

        return {
            "layer": track.layer,
            "start": track.start,
            "end": track.end
        }

    def convert_arc(self, arc):

        return {
            "layer": arc.layer,
            "geometry": arc.geometry
        }
