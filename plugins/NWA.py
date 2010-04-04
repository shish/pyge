import struct
from pygelib import PygePlugin

class NWA(PygePlugin):
    name = "NWA"
    desc = ".nwa audio, from navel games"
    type = "sound"
    sig = None
    nwa_fmt = "<hhiiiiiii"
    wav_fmt = "<4si4s4sihhiihh4si"

    def detect(self):
        return self.filename[-4:] == ".nwa"

    def _read(self):
        self.file.seek(0)
        (self.channels, self.depth, self.rate, u1, u2, u3, data_size, u4, self.samples) = \
                struct.unpack(self.nwa_fmt, self.file.read(struct.calcsize(self.nwa_fmt)))
        print "NWA unknowns: %i, %i, %i, %i" % (u1, u2, u3, u4)
        print "(tested with -1, 0, 0, 0)"
        print "(compression?, ???, block count?, compressed size?)"

    def nwa2wav(self, data):
        (channels, depth, rate, u1, u2, u3, data_size, u4, samples) = \
                struct.unpack(self.nwa_fmt, data[0:struct.calcsize(self.nwa_fmt)])
        riff_size = 36 + samples*(depth/8)
        # 16 = size of "fmt" section
        # 1 = PCM format
        header = struct.pack(self.wav_fmt, "RIFF", riff_size, "WAVE",
                             "fmt ", 16, 1, channels, rate,
                             rate*(depth/8), rate*(depth/8)*channels, depth, "data", data_size)
        return header + data[struct.calcsize(self.nwa_fmt):]

    def wav2nwa(self, data):
        (j_riff, samples, j_wave, j_fmt, j_16, j_1, channels, rate, j_bps, depth, j_data, data_size) = \
                struct.unpack(self.wav_fmt, data[0:struct.calcsize(self.wav_fmt)])
        header = struct.pack(self.nwa_fmt, channels, depth, rate, -1, 0, 0, data_size, 0, samples)
        return header + data[struct.calcsize(self.wav_fmt):]

    decrypt = nwa2wav
    encrypt = wav2nwa

