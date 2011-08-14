import struct
from pygelib import PygePlugin

#
# DAF1 (.dat) _reader, as found in Ayakashi
#
# overrides "readindex" and "writeindex" to account for non-constant
# lengths -- each entry is prefixed with an int specifying it's length
# (length int included)
#
class DAF1(PygePlugin):
    name = "DAF1"
    desc = "Ayakashi"
    sig = "DAF1"
    # first 4x = index offset? was 0x0100 when
    # the first index entry was at 0x0100...
    header_fmt = "<4s4xi4x240x" # 240x = padding to 0x0100
    entry_fmt = "<iii4x4x4x"

    def _readindex(self):
        for n in xrange(self.count):
            entrylen, start, length = struct.unpack(self.entry_fmt, self.file.read(24))
            namelen = entrylen - 24
            namez = self.file.read(namelen)
            name = namez.strip("\x00")
            self.list[name] = {"name":name, "start":start, "length":length}

    def create(self, filelist):
        print "DAF1 creation not supported yet"

