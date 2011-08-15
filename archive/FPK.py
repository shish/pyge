import struct
from archive import PygeArchive, GenericEntry


#
# FPK (.dat) as found in IOR and MNR
#
class FPK(PygeArchive):
    name = "FPK"
    desc = "(IOR, MNR) (broken)"
    sig = "FPK\x000100"
    ext = "dat"
    header_fmt = "<8s4xi12x"  # 12x = dirname?
    entry_fmt = "<4xii12s"    # 4x = compression?
    entry_order = "oln"
