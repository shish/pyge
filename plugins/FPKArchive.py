import struct
from pygelib import Archive

#
# FPK (.dat) as found in IOR and MNR
#
class FPKArchive(Archive):
    name = "FPK"
    desc = "(IOR, MNR) (broken)"
    sig = "FPK\x000100"
    header_fmt = "<8s4xi12x" # 12x = dirname?
    entry_fmt = "<4xii12s" # 4x = compression?
    entry_order = "oln"

