from pygelib import Archive
import struct

#
# Another pac format (.pac) as found in STRIKES' Yashin
#
class PAC3Archive(Archive):
    name = "Unknown .pac (STRIKES' Yashin)"
    sig = "\x00\x00\x00\x00"
    header_fmt = "<i" + ("x" * (0x3FE - 4))
    entry_fmt = "<16sii"
    entry_order = "nlo"

    def detect(self):
        self.file.seek(    4) ; t1 = self.file.read(len(self.sig)) == self.sig
        self.file.seek(0x3FE) ; t2 = self.file.read(1).isalnum()
        self.file.seek(0x416) ; t3 = self.file.read(1).isalnum()
        self.file.seek(0x42E) ; t4 = self.file.read(1).isalnum()
        return (self.filename[-3:] == "pac") and t1 and t2 and t3 and t4

    def readheader(self):
        self.count = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))[0]


#
# Another pac format (.pac) as found in MEs, same as PAC3
# except that filenames are 32 chars
#
class PAC3bArchive(Archive):
    name = "Unknown .pac (MEs)"
    sig = "\x00\x00\x00\x00"
    header_fmt = "<i" + ("x" * (0x3FE - 4))
    entry_fmt = "<32sii"
    entry_order = "nlo"

    def detect(self):
        self.file.seek(    4) ; t1 = self.file.read(len(self.sig)) == self.sig
        self.file.seek(0x3FE) ; t2 = self.file.read(1).isalnum()
        self.file.seek(0x416) ; t3 = self.file.read(1) == "\x00"
        self.file.seek(0x42E) ; t4 = self.file.read(1).isalnum()
        return (self.filename[-3:] == "pac") and t1 and t2 and t3 and t4

    def readheader(self):
        self.count = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))[0]

