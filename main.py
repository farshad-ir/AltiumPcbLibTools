from extractor.reader import PcbReader
from extractor.extractor import Extractor


file = "CAP_BOSHKE_SMD.PcbLib"

reader = PcbReader(file)

data = reader.read()

extractor = Extractor()

footprint = extractor.extract(data)

print(footprint.name)
print("Pads:", len(footprint.pads))
