from pygelib import PygePlugin

#
# VVV (.vvv) as found in VVVVVV
#
class VVV(PygePlugin):
    name = "VVV"
    desc = "VVV (VVVVVV)"
    sig = ""
    header_fmt = "<0s"
    # name, something, type?, regular_size?, compressed_size?
    # regular_size? = compressed_size? for all known files
    entry_fmt = "<48siii" # 60

    def detect(self):
        return (self.filename[-3:] == "vvv")

    def _readheader(self):
        self.count = 15
#        self.count = struct.unpack(self.header_fmt,
#                self.file.read(struct.calcsize(self.header_fmt)))[0]

    def _readindex(self):
        import struct
        offset = 0x1E00
        for n in xrange(self.count):
            namez, x1, length, x2 = struct.unpack(self.entry_fmt,
                self.file.read(struct.calcsize(self.entry_fmt)))
            name = namez.strip("\x00")
            #print name, x1, length, x2 # x1 and x2 have no obvious meaning v.v
            self.list[name] = {"name":name, "start":offset, "length":length}
            offset = offset + length
