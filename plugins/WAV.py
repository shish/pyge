import struct
from pygelib import PygePlugin

#
# Plain .wav file, for testing
#
class WAV(PygePlugin):
    name = "WAV"
    desc = "plain .wav sound"
    type = "sound"
    sig = "RIFF"
    header_fmt = "<4si4s4sihhiihh4si"

    def read(self):
        self.file.seek(0)
        (j_riff, self.samples, j_wave, j_fmt, j_16, j_1, self.channels,
                self.rate, j_byps, j_block_size, self.depth, j_data, j_data_size) = \
                struct.unpack(self.header_fmt, self.file.read(struct.calcsize(self.header_fmt)))
        print "WAV unknowns: bs:%i, ds:%i" % (j_block_size, j_data_size)
        assert j_byps == self.rate * (self.depth/8)
        assert j_riff == "RIFF"
        assert j_wave == "WAVE"
        assert j_fmt == "fmt "
        assert j_16 == 16
        assert j_1 == 1
        assert j_data == "data"

