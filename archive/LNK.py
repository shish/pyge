import struct
from archive import PygeArchive, GenericEntry


#
# LNK (.dat) as found in Ever17
#
class LNK(PygeArchive):
    name = "LNK"
    desc = "Ever17"
    sig = "LNK\x00"
    ext = "dat"
    header_fmt = "<4si8x"
    entry_fmt = "<ii24s"

    def _readindex(self):
        offs = self._data_offset()
        for n in xrange(self.count):
            start, length, namez = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            name = namez.strip("\x00")
            self.list.append(GenericEntry(self, name, start + offs, length))

    def _writeindex(self, filelist):
        start = 0
        for n in filelist:
            name = n
            length = os.stat(n).st_size
            self.file.write(struct.pack(self.entry_fmt, start, length, name))
            start = start + length
