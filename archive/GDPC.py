import struct
from archive import PygeArchive, GenericEntry


#
# (.gdpc) Girls On Tanks
#
class GDPC(PygeArchive):
    name = "GDPC"
    desc = "Girls on Tanks"
    sig = "GDPC"
    ext = "pck"
    header_fmt = "<4s80xi"
    entry_fmt = "ii"
    entry_order = "oln"

    def _readindex(self):
        offset = 0
        for n in xrange(self.count):
            strlen, = struct.unpack("i", self.file.read(4))
            name = self.file.read(strlen)
            name = name.replace("res://", "res___/")
            offset, zero1, length, zero2, blah1, blah2, blah3, blah4 = struct.unpack("iiiiiiii", self.file.read(32))
            self.list.append(GenericEntry(self, name, offset, length))
            offset += length
