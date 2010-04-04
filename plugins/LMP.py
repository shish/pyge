import struct
from pygelib import PygePlugin

#
# LMP (.lmp) archives, as found in The Bard's Tale
#
# No signature
# No writer code (yet)
# Writer untestable -- comes from read only media (PS2 game)
#
class LMP(PygePlugin):
    name = "LMP"
    desc = "The Bard's Tale"
    sig = ""
    header_fmt = "<i"
    entry_fmt = "<56sii"
    entry_order = "nol"

    def detect(self):
        return self.filename.endswith(".LMP")

    def readheader(self):
        (self.count, ) = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))
