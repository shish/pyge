import struct
from pygelib import Image

#
# MalieGF (.mgf) image -- really just a PNG with first few bytes swapped
#
class MalieGFImage(Image):
    name = "MalieGF"
    sig = "MalieGF"

    def read(self):
        self.file.seek(0)
        sig, = struct.unpack("<7sx", self.file.read(8))
        self.count = 1
        if sig != self.sig:
            print "sig needs to be '%s'\n" % (self.sig)
            return
        self.contentname = self.filename.replace(".mgf", ".png")

    def create(self, filelist):
        self.file.seek(0)
        self.append(filelist[0])

    def mgf2png(self, data):
        return data.replace("MalieGF\x00", "\x89PNG\x0D\x0A\x1A\x0A")

    def png2mgf(self, data):
        return data.replace("\x89PNG\x0D\x0A\x1A\x0A", "MalieGF\x00")

    decrypt = mgf2png
    encrypt = png2mgf

