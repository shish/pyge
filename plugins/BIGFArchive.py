import struct
from pygelib import Archive

#
# bigf (.big) as found in SSX3
#
# broken (count, start and length don't work...)
#
class BIGFArchive(Archive):
    name = "BigF"
    desc = "SSX3"
    sig = "BIGF"
    header_fmt = "<4s4x4xi"
    entry_fmt = "<ii14s"

    def readindex(self):
        print "count"
        self.count = 10
        for n in xrange(self.count):
            length, start, namez = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            name = namez.strip("\x00")
            self.list[name] = {"name":name, "start":start, "length":length}

