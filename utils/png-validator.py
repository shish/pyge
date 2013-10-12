#!/usr/bin/env python

import sys
import struct
import zlib

def read_header(fp):
    data = fp.read(8)
    if data != "\x89PNG\x0D\x0A\x1A\x0A":
        print "Bad header"
        return False
    print "Good header"
    return True

def read_chunk(fp):
    length, chunk_type = struct.unpack(">i4s", fp.read(8))
    print "%s %4d" % (chunk_type, length),
    data = fp.read(length)
    csum = struct.unpack(">i", fp.read(4))[0]
    dsum = zlib.crc32(chunk_type + data)
    if csum != dsum:
        print "Invalid checksum"
        return False
    if chunk_type == "IHDR":
        width, height, depth, color_type, comp_meth, filter_meth, interlace_meth = struct.unpack(">iibbbbb", data)
        print "%dx%d @%d" % (width, height, depth)
    elif chunk_type == "tEXt":
        print data
    else:
        print "No meta"
    if chunk_type == "IEND":
        return False
    return True

fp = file(sys.argv[1], "rb")

if read_header(fp):
    while read_chunk(fp):
        pass