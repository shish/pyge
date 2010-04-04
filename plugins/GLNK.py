from pygelib import PygePlugin
import struct

#
# GLNK (.gl) as found in Present for You
#
class GLNK(PygePlugin):
    name = "GLNK"
    desc = "Present for You"
    sig = "GLNK"
    header_fmt = "<4sxxi"
    entry_fmt = "<iiB"

    def readindex(self):
        for n in xrange(self.count):
            length, blah, namelen = struct.unpack(self.entry_fmt, self.file.read(9))
            name = self.file.read(namelen)
            start, = struct.unpack("i", self.file.read(4))
            self.list[name] = {"name":name, "start":start, "length":length}

    def create(self, filelist):
        print "GLNK creation not supported yet"

