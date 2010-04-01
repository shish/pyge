#!/usr/bin/python

import struct
import sys, os

class Archive(object):
    name = "Unnamed (BUG)"
    desc = ""
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


    def detect(self):
        if self.sig == None:
            return False
        self.file.seek(0)
        head = self.file.read(len(self.sig))
        return head == self.sig


    def read(self):
        self.list = {}
        self.file.seek(0)
        self.readheader()
        self.readindex()

    def readheader(self):
        sig, self.count = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))
        if sig != self.sig:
            print "sig needs to be '%s'\n" % (self.sig)
            return False

    def readindex(self):
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
            self.list[name] = {"name":name, "start":offset, "length":length}

    def extract(self, name, ofile=None):
        if not ofile:
            unix_name = name.replace("\\", "/")
            (dirname, filename) = os.path.split(unix_name)
            if len(dirname) > 0:
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
            ofile = open(unix_name, "w")
        print "extracting %s" % (name)
        self.file.seek(self.list[name]["start"])
        data = self.file.read(self.list[name]["length"])
        if(self.decrypt):
            data = self.decrypt(data)
        # for some reason, the first couple of oggs in a
        # pac3 archive are offset by an extra 12 bytes...
        if data[0:32].find("OggS") > 0:
            data = data[data[0:32].find("OggS"):]
        ofile.write(data)
        return len(data)


    def create(self, filelist):
        self.file.seek(0)
        self.writeheader(filelist)
        self.writeindex(filelist)

        for n in filelist:
            fp = open(n, 'rb')
            self.append(n, fp)
            fp.close()

    def writeheader(self, filelist):
        self.file.write(struct.pack(self.header_fmt, self.sig, len(filelist)))

    def writeindex(self, filelist):
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
            offset = offset + length

    def append(self, name, ifile):
        print "appending %s" % (name)
        data = ifile.read()
        if(self.encrypt):
            data = self.encrypt(data)
        self.file.write(data)

class Image(object):
    name = "Unnamed (BUG)"
    desc = ""
    width = 0
    height = 0
    depth = 0
    filename = None
    file = None
    sig = None
    header_fmt = "4shhh"
    encrypt = None
    decrypt = None

    def __init__(self, filename, file):
        self.filename = filename
        self.file = file


    def detect(self):
        if self.sig == None:
            return False
        self.file.seek(0)
        head = self.file.read(len(self.sig))
        return head == self.sig

    def read(self):
        self.file.seek(0)
        self.readheader()

    def readheader(self):
        sig, self.width, self.height, self.depth = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))
        if sig != self.sig:
            print "sig needs to be '%s'\n" % (self.sig)
            return False

    def getBmp(self):
        print "reading %s to buffer" % (self.filename)
        self.file.seek(0)
        data = self.file.read()
        if(self.decrypt):
            data = self.decrypt(data)
        return data

class Sound(object):
    name = "Unnamed (BUG)"
    desc = ""
    samples = 0
    rate = 0
    depth = 0
    filename = None
    file = None
    sig = None
    header_fmt = "4s"
    encrypt = None
    decrypt = None

    def __init__(self, filename, file):
        self.filename = filename
        self.contentname = self.filename + ".wav"
        self.file = file


    def detect(self):
        if self.sig == None:
            return False
        self.file.seek(0)
        head = self.file.read(len(self.sig))
        return head == self.sig


    def read(self):
        self.file.seek(0)
        self.readheader()

    def readheader(self):
        sig, = struct.unpack(self.header_fmt,
                self.file.read(struct.calcsize(self.header_fmt)))
        if sig != self.sig:
            print "sig needs to be '%s'\n" % (self.sig)
            return False

    def getWav(self):
        print "reading %s to buffer" % (self.filename)
        self.file.seek(0)
        data = self.file.read()
        if(self.decrypt):
            data = self.decrypt(data)
        return data


def load_plugins(path):
    sys.path.append(path)
    for fname in os.listdir(path):
        if fname[-3:] == ".py":
            __import__(fname[0:-3])
    arcs = list(Archive.__subclasses__())
    imgs = list(Image.__subclasses__())
    snds = list(Sound.__subclasses__())
    plugins = {}
    for plugin in arcs + imgs + snds:
        if plugin.name in plugins:
            print "ERROR: duplicate plugin name: "+plugin.name
        plugins[plugin.name] = plugin
    return plugins

