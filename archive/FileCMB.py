import struct
import re
from archive import PygeArchive, GenericEntry


#
# FileCMB (.dat) as found in Roommate
#
class FileCMB(PygeArchive):
    name = "FileCMB"
    desc = "Roommate"
    sig = "FILECMB-DATA-LIST-IN\x0A"
    ext = "dat"
    header_fmt = "<21s"
    entry_fmt = "<ii24s"

    def _readheader(self):
        sig, = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))
        if sig != self.sig:
            print "sig needs to be '%s'\n" % (self.sig)
            return False
        self.count = -1

    def _readindex(self):
        line = ""
        while True:
            line = self.file.readline()
            if line == None:
                break
            elif line == "LIST-END\n":
                break
            else:
                m = re.search("^([\w\.]+)\s+(\d+)\s+(\d+)", line)
                self.list.append(GenericEntry(
                    self,
                    m.group(1),
                    int(m.group(2)),
                    int(m.group(3)) - int(m.group(2))
                ))

    def create(self, filelist):
        print "Create not supported yet"
