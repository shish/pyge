from archive import PygeArchive, GenericEntry


#
# Gamedat Pac2 (.dat) as found in TG (?)
#
class PAC2(PygeArchive):
    name = "Pac2"
    desc = "TG?"
    sig = "GAMEDAT PAC2"
    ext = "dat"
    header_fmt = "<12si"
    # FIXME: actually 32s, offsets and lengths aren't specified (!?)
    entry_fmt = "<24sii"
