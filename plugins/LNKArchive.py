import struct
from pygelib import Archive

#
# LNK (.dat) as found in Ever17
#
class LNKArchive(Archive):
    name = "LNK (Ever17)"
    sig = "LNK\x00"
    header_fmt = "<4si8x"
    entry_fmt = "<ii24s"

    def readindex(self):
        offs = struct.calcsize(self.header_fmt) + struct.calcsize(self.entry_fmt) * self.count
        for n in xrange(self.count):
            start, length, namez = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            name = namez.strip("\x00")
            self.list[name] = name, start + offs, length

    def writeindex(self, filelist):
        start = 0
        for n in filelist:
            name = n
            length = os.stat(n).st_size
            self.file.write(struct.pack(self.entry_fmt, start, length, name))
            start = start + length


