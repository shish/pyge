import struct
from archive import PygeArchive, GenericEntry

#
# CAPF (.pac) as seen in Navel games (Shuffle, Tick Tack, Soul Link, etc)
#
# unpack & repack seem to work and give the same filesize, data mod not tested
# since all formats inside the archive are proprietary...
#
class CAPF(PygeArchive):
    name = "CAPF"
    desc = "Various Navel games (Shuffle, Tick Tack)"
    sig = "CAPF"
    ext = "pac"
    header_fmt = "<4s8xi16x"
    entry_fmt = "<ii32s"
    entry_order = "oln"
