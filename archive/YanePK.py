from archive import PygeArchive, GenericEntry

#
# yanepk (.dat) as found in Nuba (?)
#
class YanePK(PygeArchive):
    name = "YanePK"
    desc = "Nuba, Seiken Block 2"
    sig = "yanepkEx"
    ext = "dat"
    header_fmt = "<8si"
    entry_fmt = "<28s4xi4xi"
