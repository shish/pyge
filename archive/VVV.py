from archive import PygeArchive, GenericEntry

#
# VVV (.vvv) as found in VVVVVV
#
class VVV(PygeArchive):
    name = "VVV"
    desc = "VVV (VVVVVV)"
    sig = None
    ext = "vvv"
    entry_fmt = "<48siii" # 60

    def _readheader(self):
        self.count = 15

    def _readindex(self):
        import struct
        offset = 0x1E00
        for n in xrange(self.count):
            namez, x1, length, x2 = struct.unpack(self.entry_fmt,
                self.file.read(struct.calcsize(self.entry_fmt)))
            name = namez.strip("\x00")
            #print name, x1, length, x2 # x1 and x2 have no obvious meaning v.v
            self.list.append(GenericEntry(self, name, offset, length))
            offset = offset + length
