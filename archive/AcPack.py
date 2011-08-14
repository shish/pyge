import struct
from archive import PygeArchive, GenericEntry

#
# AcPack (.pak) as found in Discipline
#
class AcPack(PygeArchive):
    name = "AcPack"
    desc = "Discipline"
    sig = "ACPACK32"
    ext = "pak"
    header_fmt = "<8s4xi"
    entry_fmt = "<28si"

    def _readindex(self):
        for n in xrange(self.count):
            namez, start = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            name = namez.strip("\x00")
            if n > 0:
                self.list[n-1]._length = start - self.list[n-1]._offset
            if len(name) > 0:
                self.list.append(GenericEntry(self, name, start, 0))
