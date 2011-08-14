from pygelib import PygePlugin

#
# Gamedat Pac2 (.dat) as found in TG (?)
#
class PAC2(PygePlugin):
    name = "Pac2"
    desc = "TG?"
    sig = "GAMEDAT PAC2"
    header_fmt = "<12si"
    entry_fmt = "<24sii" # FIXME: actually 32s, offsets and lengths aren't specified (!?)

