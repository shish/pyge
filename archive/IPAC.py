from pygelib import PygePlugin

#
# IPAC (.pak) as found in <Something japanese...>
#
class IPAC(PygePlugin):
    name = "IPAC"
    desc = "Found in <Something japanese...>"
    sig = "IPAC"
    header_fmt = "<4si"
    entry_fmt = "<36sii"

