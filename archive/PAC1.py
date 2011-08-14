from archive import PygeArchive, GenericEntry

#
# Pac1 (.pac) as found in Himegoto
#
class PAC1(PygeArchive):
    name = "Pac1"
    desc = "Himegoto (broken)"
    sig = "PAC1"
    ext = "pac"
    header_fmt = "<4si"
    # name, something, type?, regular_size?, compressed_size?
    # regular_size? = compressed_size? for all known files
    entry_fmt = "<16si4x4xi"
