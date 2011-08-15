import struct


class PygeEntry(object):
    name = None
    archive = None

    def __init__(self, archive):
        self.archive = archive

    def get_data(self):
        return None

    def __str__(self):
        return "<PygeEntry %s>" % (self.name, )


class GenericEntry(PygeEntry):
    _offset = None
    _length = None

    def __init__(self, archive, name, offset, length):
        self.archive = archive
        self.name = name
        self._offset = offset
        self._length = length

    def get_data(self):
        self.archive.file.seek(self._offset)
        return self.archive.file.read(self._length)

    def __str__(self):
        return "<GenericEntry %s (%d:+%d)>" % (self.name, self._offset, self._length)


class PygeArchive(object):
    name = "Generic"
    desc = "An extremely standard archive format"
    sig = None
    ext = None
    header_fmt = "4si"
    entry_fmt = "32sii"
    entry_order = "nol"
    encrypt = None
    decrypt = None

    def __init__(self, file):
        self.file = file

    def detect(self):
        """
        returns a number representing how likely it is that this plugin can handle the file

        possibly like this:
        - 0 definite no
        - 1 I'm feeling lucky
        - 2 file.name looks likely
        - 3 header bytes look likely
        - 4 definite yes
        """
        if self.sig:
            self.file.seek(0)
            head = self.file.read(len(self.sig))
            if head == self.sig:
                return 3
        if self.ext:
            if self.file.name.split(".")[-1] == self.ext:
                return 2
        return 0

    def get_file_list(self):
        self._read()
        return self.list

    def _read(self):
        self.list = []
        self.file.seek(0)
        self._readheader()
        self._readindex()

    def _readheader(self):
        if self.sig:
            sig, self.count = struct.unpack(self.header_fmt,
                    self.file.read(struct.calcsize(self.header_fmt)))
            if sig != self.sig:
                print "sig needs to be '%s'\n" % (self.sig)
                return False

    def _readindex(self):
        for n in xrange(self.count):
            if self.entry_order == "nol":
                namez, offset, length = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            elif self.entry_order == "nlo":
                namez, length, offset = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            elif self.order == "oln":
                offset, length, namez = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            name = namez.strip("\x00")
            self.list.append(GenericEntry(self, name, offset, length))
