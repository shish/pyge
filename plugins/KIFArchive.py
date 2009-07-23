from pygelib import Archive

#
# KIF (.int) as found in Donburi
#
# unpack and repack work, no crash (2006/07/10)
# mod not tried
#
class KIFArchive(Archive):
    name = "KIF (Donburi)"
    sig = "KIF\x00"
    header_fmt = "<4si"
    entry_fmt = "<32sii"

