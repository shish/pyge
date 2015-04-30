import struct
from archive import PygeArchive, GenericEntry


#
# (.arc) Tokoya, I/O
#
# unpack & repack seem to work and give the same filesize, data mod not tested
# since all formats inside the archive are proprietary...
#
class Arc(PygeArchive):
    name = "Arc"
    desc = "Tokoya / I/O"
    sig = "\x01\x00\x00\x00"
    ext = "arc"
    header_fmt = "<4s4xi4x"
    entry_fmt = "<9sii" # 21
    entry_order = "nlo"
