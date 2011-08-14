import struct
from pygelib import PygePlugin

#
# MalieGF (.mgf) image -- really just a PNG with first few bytes swapped
#
class MalieGF(PygePlugin):
    name = "MalieGF"
    type = "image"
    sig = "MalieGF"

    def mgf2png(self, data):
        return data.replace("MalieGF\x00", "\x89PNG\x0D\x0A\x1A\x0A")

    def png2mgf(self, data):
        return data.replace("\x89PNG\x0D\x0A\x1A\x0A", "MalieGF\x00")

    decrypt = mgf2png
    encrypt = png2mgf

