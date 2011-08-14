import struct
from archive import PygeArchive, GenericEntry

#
# Inx (.Inx / .Snn) as found in Oppai Life
#
class Inx(PygeArchive):
    name = "Inx / Snn"
    desc = "Oppai Life"
    ext = "inx"
    header_fmt = "<i"
    entry_fmt = "<64sii"

    def _readheader(self):
        self.count = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))[0]


    def extract(self, fname, ofile=None):
        self.file = open(self.filename[0:-3] + "Snn", "rb")
        PygeArchive.extract(self, fname, ofile)
