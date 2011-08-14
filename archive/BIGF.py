import struct
from archive import PygeArchive, GenericEntry

#
# bigf (.big) as found in SSX3
#
# broken (count, start and length don't work...)
#
class BIGF(PygeArchive):
    name = "BigF"
    desc = "SSX3"
    sig = "BIGF"
    ext = "big"
    header_fmt = "<4s4x4xi"
    entry_fmt = "<ii14s"

    def _readindex(self):
        self.count = 10
        for n in xrange(self.count):
            length, start, namez = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            name = namez.strip("\x00")
            self.list.append(GenericEntry(self, name, start, length))
