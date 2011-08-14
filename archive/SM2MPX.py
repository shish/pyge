from archive import PygeArchive, GenericEntry

#
# sm2 (no ext) as found in Crescendo
#
class SM2MPX(PygeArchive):
    name = "SM2"
    desc = "Crescendo"
    sig = "SM2MPX10"
    ext = None
    header_fmt = "<8si20x"
    entry_fmt = "<12sii"
