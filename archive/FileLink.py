import struct
from archive import PygeArchive, GenericEntry


#
# CLS_FILELINK (.dat) as found in Splush Wave's "Space Fleet"
#
class FileLink(PygeArchive):
    name = "FileLink"
    desc = "From Splush Wave's 'Space Fleet'"
    sig = "CLS_FILELINK"
    ext = "dat"
    header_fmt = "<12s4xi12x32x"
    entry_fmt = "<32s12xii12x"
