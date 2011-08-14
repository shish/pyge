import struct
from pygelib import PygePlugin

#
# GGD (.ggd) image -- I don't get it /o/
#
class GGD(PygePlugin):
    name = "GGD"
    desc = "GGD Image (broken)"
    type = "image"
    sig = "\xB9\xAA\xB3\xB3"
    header_fmt = "<4shh"

    def _readheader(self):
        sig, self.width, self.height = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))
        self.depth = 32

