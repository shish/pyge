import struct
from pygelib import PygePlugin

#
# Inx (.Inx / .Snn) as found in Oppai Life
#
class Inx(PygePlugin):
    name = "Inx / Snn"
    desc = "Oppai Life"
    header_fmt = "<i"
    entry_fmt = "<64sii"

    def detect(self):
        return (self.filename[-3:] == "Inx")

    def _readheader(self):
        self.count = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))[0]


    def extract(self, fname, ofile=None):
        self.file = open(self.filename[0:-3] + "Snn", "rb")
        PygePlugin.extract(self, fname, ofile)
