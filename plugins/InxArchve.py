import struct
from pygelib import Archive

#
# Inx (.Inx / .Snn) as found in Oppai Life
#
class InxArchive(Archive):
    name = "Inx / Snn (Oppai Life)"
    header_fmt = "<i"
    entry_fmt = "<64sii"

    def detect(self):
        return (self.filename[-3:] == "Inx")

    def readheader(self):
        self.count = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))[0]


    def extract(self, fname, ofile=None):
        self.file = open(self.filename[0:-3] + "Snn", "rb")
        Archive.extract(self, fname, ofile)
