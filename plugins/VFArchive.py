import struct
from pygelib import Archive

#
# VF (.vfs) as found in CraziesT
#
# unpack & repack tested, binary compatible (2006/07/10)
# no data change tested since it's all proprietary formats
#
class VFArchive(Archive):
    name = "VFS (CraziesT)"
    sig = "VF\x01\x01"
    header_fmt = "<4sh10x"
    entry_fmt = "<13s2x4xii4xx"

    # FIXME: contains voodoo
    # FIXME: depends on filelist being real files
    def writeheader(self, filelist):
        idxsize = len(filelist) * struct.calcsize(self.entry_fmt)
        fsize = struct.calcsize(self.header_fmt) + idxsize
        for n in filelist:
            fsize = fsize + os.stat(n).st_size
        self.file.write(struct.pack("<4sh2sii", self.sig, len(filelist),
                                    "\x20\x00", idxsize, fsize))

    def writeindex(self, filelist):
        start = struct.calcsize(self.header_fmt) + struct.calcsize(self.entry_fmt) * len(filelist)

        for n in filelist:
            name = n
            length = os.stat(n).st_size
            # 0 = compression, length#2 = compressed size?
            self.file.write(struct.pack("<13s2siiiix", name, "\x20\x00", 0, start, length, length))
            start = start + length

