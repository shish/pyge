from pygelib import PygePlugin
import struct

#
# LIB (.lib) as found in Imitation Lover
# 
# this format contains a directory structure; the _reader currently
# _reads file entries, but not diretory entries, and the file entry
# offset is hackily hardcoded for one specific file...
#
class Lib(PygePlugin):
    name = "Lib"
    desc = "Imitation Lover"
    sig = "LIB"
    header_fmt = "<3sx212xi4x"
    entry_fmt = "<36sii4x"
    entry_order = "nlo"

    def _readindex(self):
        for n in xrange(self.count):
            namez, length, offset = struct.unpack(self.entry_fmt, self.file.read(struct.calcsize(self.entry_fmt)))
            name = namez.strip("\00")
            self.list[name] = {"name":name, "start":offset+0xd0, "length":length}
