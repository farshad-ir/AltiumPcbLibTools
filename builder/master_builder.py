from model.pad import PadMaster


class PadMasterBuilder:

    def __init__(self):
        self.masters = []

    def build(self, pads):

        for pad in pads:

            master = self.find_match(pad)

            if master:
                pad.master = master

            else:
                new_master = self.create_master(pad)

                new_master.id = (
                    f"PAD_MASTER_{len(self.masters) + 1:03d}"
                )

                self.masters.append(new_master)

                pad.master = new_master

        return self.masters

    def find_match(self, pad):

        for master in self.masters:

            if self.is_same_geometry(master, pad):
                return master

        return None

    def is_same_geometry(self, master, pad):

        return (
            master.shape == pad.shape
            and master.size == pad.size
            and master.layer == pad.layer
        )

    def create_master(self, pad):

        master = PadMaster()

        master.shape = pad.shape
        master.size = pad.size.copy()
        master.layer = pad.layer
        master.options = pad.options.copy()

        return master
