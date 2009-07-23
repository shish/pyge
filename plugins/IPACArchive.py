from pygelib import Archive

#
# IPAC (.pak) as found in <Something japanese...>
#
class IPACArchive(Archive):
    name = "IPAC (?)"
    sig = "IPAC"
    header_fmt = "<4si"
    entry_fmt = "<36sii"

