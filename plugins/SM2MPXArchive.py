from pygelib import Archive

#
# sm2 (no ext) as found in Crescendo
#
class SM2MPXArchive(Archive):
    name = "SM2"
    desc = "Crescendo"
    sig = "SM2MPX10"
    header_fmt = "<8si20x"
    entry_fmt = "<12sii"

