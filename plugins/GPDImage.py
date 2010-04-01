from pygelib import Image

#
# GPD (.gpd) image -- Used in Navel games
#
class GPDImage(Image):
    name = "GPD"
    desc = "Various Navel games"
    sig = " DPG"
    header_fmt = "<4s4x4xiii"

