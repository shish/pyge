import struct
from archive import PygeArchive, GenericEntry

#
# LMP (.lmp) archives, as found in The Bard's Tale
#
# No signature
# No _writer code (yet)
# Writer untestable -- comes from _read only media (PS2 game)
#
class LMP(PygeArchive):
    name = "LMP"
    desc = "The Bard's Tale"
    ext = "lmp"
    header_fmt = "<i"
    entry_fmt = "<56sii"
    entry_order = "nol"

    def _readheader(self):
        (self.count, ) = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))
