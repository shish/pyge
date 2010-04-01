from pygelib import Archive

#
# Gamedat Pac2 (.dat) as found in TG (?)
#
class PAC2Archive(Archive):
    name = "Pac2"
    desc = "TG?"
    sig = "GAMEDAT PAC2"
    header_fmt = "<12si"
    entry_fmt = "<24sii" # FIXME: actually 32s, offsets and lengths aren't specified (!?)

