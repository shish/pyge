from archive import PygeArchive, GenericEntry


#
# IPAC (.pak) as found in <Something japanese...>
#
class IPAC(PygeArchive):
    name = "IPAC"
    desc = "Found in <Something japanese...>"
    sig = "IPAC"
    ext = "pak"
    header_fmt = "<4si"
    entry_fmt = "<36sii"
