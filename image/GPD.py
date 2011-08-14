from pygelib import PygePlugin

#
# GPD (.gpd) image -- Used in Navel games
#
class GPD(PygePlugin):
    name = "GPD"
    desc = "Various Navel games"
    type = "image"
    sig = " DPG"
    header_fmt = "<4s4x4xiii"

