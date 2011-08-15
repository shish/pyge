from archive import PygeArchive, GenericEntry
import struct


#
# no sig or extension as found in Time Stripper Mako-chan
#
class Mako(PygeArchive):
    name = "Mako"
    desc = "Time Stripper Mako-chan"
    sig = None
    header_fmt = "<h"
    entry_fmt = "<12si"

    def _readheader(self):
        self.header_len = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))[0]
        self.count = (self.header_len - 2) / struct.calcsize(self.entry_fmt)

    def _readindex(self):
        for n in xrange(self.count):
            name, offset = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            name = name.strip("\0")
            self.list.append(GenericEntry(self, name, offset, 0))
            if n > 0:
                self.list[n - 1]._length = offset - self.list[n - 1]._offset
        self.file.seek(0, 2)
        self.list[n - 1]._length = self.file.tell() - self.list[n - 1]._offset
