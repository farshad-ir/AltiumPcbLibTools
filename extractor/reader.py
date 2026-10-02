class PcbReader:

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, "r", encoding="utf-8",
                  errors="ignore") as f:
            return f.read()
