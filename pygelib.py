#!/usr/bin/python

"""
PyGE base library, various types of object that can be inherited from

To add support for a new format, create a class in plugins/ which
inherits from PygePlugin, then override the methods as relevant.


The following methods are exposed, to be used as the public API:

detect()
    check if this plugin can handle the file (checking against
    self.filename (string) or self.file (filehandle))

print_list()
    print a listing of contents to stdout

extract(filename)
    extract the named file; if filename is Null, extract all files

create(filenames)
    build an archive containing the named files

In many cases, these methods don't need to be overridden at all, the
programmer only needs to tweak their behaviour by setting some class
variables:

    name = "Unnamed (BUG)"  # the human-readable name of the format
    sig = None              # what the first few bytes of file look like
    header_fmt = "4si"      # header = 4 byte string (signature), 32-bit int (file count)
    entry_fmt = "32sii"     # entry = 32s (name), int (offset), int (length)
    entry_order = "nol"     # name, offset, length
    encrypt = None          # callback function to encrypt a file
    decrypt = None          # callback function to decrypt a file

For example, if you have an archive with header "ARCH\\x00\\x00\\x00\\x02"
and a list of files [(4-byte offset, 4-byte length, 24-byte name), ...] you
would create the class:

ArchArchive(PygePlugin):
    name = "Example Archive"
    sig = "ARCH"
    entry_order = "oln"
    entry_fmt = "ii24s"

Given these parameters detection, extraction, and re-packing can all be
handled using the flexible base methods.


If the flexible base methods aren't flexible enough (for example, if the
file records are variable-length, or the number of entries is stored at
the end of the archive), you can override each method, or even specific
sub-parts of each method:

[to be documented]
"""

import struct
import sys, os


class PygePlugin(object):
    name = "Unnamed (BUG)"
    desc = ""
    type = "archive"
    filename = None
    file = None
    list = {}
    count = 0
    sig = None
    header_fmt = "4si"
    entry_fmt = "32sii"
    entry_order = "nol"
    encrypt = None
    decrypt = None

    def __init__(self, filename, file):
        self.filename = filename
        self.file = file

    # detect
    def detect(self):
        """
        check if this plugin can handle the file

        default: return true if the first few bytes of the file == self.sig
        """
        if self.sig is None:
            return False
        self.file.seek(0)
        head = self.file.read(len(self.sig))
        return head == self.sig

    # get / print list
    def print_list(self):
        if self.type == "archive":
            self._read()
            print "%50s : %12s %12s" % ("Name", "Offset", "Length")
            tlen = 0
            for name in self.list:
                data = self.list[name]
                tlen = tlen + data["length"]
                print "%50s : %12i %12i" % (data["name"], data["start"], data["length"])
            #print "%50s : %12i %12i" % ("", 0, tlen)
        if self.type == "image":
            print "File is an image"
        if self.type == "sound":
            print "File is a sound"

    def _read(self):
        self.list = {}
        self.file.seek(0)
        self._readheader()
        self._readindex()

    def _readheader(self):
        sig, self.count = struct.unpack(self.header_fmt,
            self.file.read(struct.calcsize(self.header_fmt)))
        if sig != self.sig:
            print "sig needs to be '%s'\n" % self.sig
            return False

    def _readindex(self):
        for n in xrange(self.count):
            if self.entry_order == "nol":
                namez, offset, length = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            elif self.entry_order == "nlo":
                namez, length, offset = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            elif self.entry_order == "oln":
                offset, length, namez = struct.unpack(self.entry_fmt,
                    self.file.read(struct.calcsize(self.entry_fmt)))
            else:
                raise Exception("Unknown entry_order: %r" % self.entry_order)
            name = namez.strip("\x00")
            self.list[name] = {"name": name, "start": offset, "length": length}

    # extraction
    def extract(self, name=None, ofile=None):
        if self.type == "archive":
            self._extract_from_archive(name, ofile)
        if self.type == "image":
            self._extract_image(name, ofile)
        if self.type == "sound":
            self._extract_sound(name, ofile)

    def _extract_from_archive(self, name=None, ofile=None):
        if not self.list:
            self._read()
        if not name:
            for name in self.list:
                self._extract_from_archive(name)
            return
        if not ofile:
            unix_name = name.replace("\\", "/")
            (dirname, filename) = os.path.split(unix_name)
            if len(dirname) > 0:
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
            ofile = open(unix_name, "w")
        print "extracting %s" % name
        self.file.seek(self.list[name]["start"])
        data = self.file.read(self.list[name]["length"])
        if self.decrypt:
            data = self.decrypt(data)
        # for some reason, the first couple of oggs in a
        # pac3 archive are offset by an extra 12 bytes...
        if data[0:32].find("OggS") > 0:
            data = data[data[0:32].find("OggS"):]
        ofile.write(data)
        return len(data)

    def _extract_image(self, name=None, oname=None):
        if not name:
            name = self.filename
        if not oname:
            oname = name+".png"
        self.file.seek(0)
        data = self.file.read()
        if self.decrypt:
            data = self.decrypt(data)
        file(oname, "wb").write(data)

    def _extract_sound(self, name=None, oname=None):
        if not name:
            name = self.filename
        if not oname:
            oname = name+".wav"
        self.file.seek(0)
        data = self.file.read()
        if self.decrypt:
            data = self.decrypt(data)
        file(oname, "wb").write(data)

    # creations
    def create(self, filelist):
        if self.type == "archive":
            self.file.seek(0)
            self._writeheader(filelist)
            self._writeindex(filelist)

            for n in filelist:
                fp = open(n, 'rb')
                self._append(n, fp)
                fp.close()
        if self.type == "image":
            self._create_image(filelist)
        if self.type == "sound":
            self._create_sound(filelist)

    def _writeheader(self, filelist):
        self.file.write(struct.pack(self.header_fmt, self.sig, len(filelist)))

    def _writeindex(self, filelist):
        offset = struct.calcsize(self.header_fmt) + struct.calcsize(self.entry_fmt) * len(filelist)

        print "writing index"
        for n in filelist:
            name = n
            length = os.stat(n).st_size
            if self.entry_order == "nol":
                self.file.write(struct.pack(self.entry_fmt, name, offset, length))
            elif self.entry_order == "nlo":
                self.file.write(struct.pack(self.entry_fmt, name, length, offset))
            elif self.entry_order == "oln":
                self.file.write(struct.pack(self.entry_fmt, offset, length, name))
            offset += length

    def _append(self, name, ifile):
        print "appending %s" % (name)
        data = ifile.read()
        if self.encrypt:
            data = self.encrypt(data)
        self.file.write(data)

    def _create_image(self, filenames):
        for fn in filenames:
            data = file(fn).read()
            if self.encrypt:
                data = self.encrypt(data)
            file(self.filename, "wb").write(data)

    def _create_sound(self, filenames):
        for fn in filenames:
            data = file(fn).read()
            if self.encrypt:
                data = self.encrypt(data)
            file(self.filename, "wb").write(data)


def load_plugins(path):
    sys.path.append(path)
    for fname in os.listdir(path):
        if fname[-3:] == ".py":
            __import__(fname[0:-3])
    plugins = {}
    for plugin in list(PygePlugin.__subclasses__()):
        if plugin.name in plugins:
            print "ERROR: duplicate plugin name: " + plugin.name
        plugins[plugin.name] = plugin
    return plugins

