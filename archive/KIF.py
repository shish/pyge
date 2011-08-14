from archive import PygeArchive, GenericEntry

#
# KIF (.int) as found in Donburi
#
# unpack and repack work, no crash (2006/07/10)
# mod not tried
#
class KIF(PygeArchive):
    name = "KIF"
    desc = "Donburi"
    sig = "KIF\x00"
    ext = "int"
    header_fmt = "<4si"
    entry_fmt = "<32sii"
