import struct
from pygelib import PygePlugin

#
# AcPack (.pak) as found in Discipline
#
class AcPack(PygePlugin):
    name = "AcPack"
    desc = "Discipline"
    sig = "ACPACK32"
    header_fmt = "<8s4xi"
    entry_fmt = "<28si"

    def _readindex(self):
        prev = None
        for n in xrange(self.count):
            namez, start = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            name = namez.strip("\x00")
            if prev:
                self.list[prev]["length"] = start - self.list[prev]["start"]
            if len(name) > 0:
                self.list[name] = {"name":name, "start":start, "length":0}
                prev = name

