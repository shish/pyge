from pygelib import Archive

#
# yanepk (.dat) as found in Nuba (?)
#
class YanePKArchive(Archive):
    name = "YanePK Archive (Nuba, Seiken Block 2)"
    sig = "yanepkEx"
    header_fmt = "<8si"
    entry_fmt = "<28s4xi4xi"

