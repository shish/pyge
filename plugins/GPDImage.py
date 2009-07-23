from pygelib import Image

#
# GPD (.gpd) image -- Used in Navel games
#
class GPDImage(Image):
    sig = " DPG"
    header_fmt = "<4s4x4xiii"

