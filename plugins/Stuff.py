import struct
from pygelib import PygePlugin

#
# Stuff (.stuff) as found in EVE online
#
class Stuff(PygePlugin):
    name = "Stuff"
    desc = "EVE Online"
    header_fmt = "<i"
    entry_fmt = "<ii"

    def detect(self):
        return (self.filename[-5:] == "stuff")

    def readheader(self):
        self.count = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))[0]

    def readindex(self):
        offset = 0
        for n in xrange(self.count):
            length, maybe_flags = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            name = ""
            while True:
                char = self.file.read(1)
                if char == "\x00":
                    break
                name = name + char
            self.list[name] = {"name":name, "start":offset, "length":length}
            offset = offset + length

        offset = self.file.tell()
        for n in self.list:
            self.list[n]["start"] = self.list[n]["start"] + offset
