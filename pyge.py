#!/usr/bin/python

import os, os.path, sys
import getopt, struct, re
from array import array
import pygelib

def print_help():
    print "Usage: pyge [options]"
    print " -f <arcname>    operate on this archive"
    print " -F <format>     explicitly set the format"
    print " -x <filename>   extract a file"
    print " -X              extract all files"
    print " -l              list files"
    print " -c              create archive"

def main():
    plugins = pygelib.load_plugins("/home/shish/src/pyge/plugins")

    filename = None
    fp = None
    archive = None
    do_extract = False
    do_list = False
    do_create = False
    format = None
    extractName = None

    if(len(sys.argv) == 2):
        do_extract = True
        filename = sys.argv[1]

    try:
        optlist, args = getopt.getopt(sys.argv[1:], "Xx:f:p:lcF:")
    except getopt.GetoptError, goe:
        print "Unrecognised option"
        print_help()
        return 1

    for a, o in optlist:
        if a == "-x":
            do_extract = True
            extractName = o
        if a == "-X":
            do_extract = True
            extractName = None
        if a == "-l":
            do_list = True
        if a == "-f":
            filename = o
        if a == "-F":
            format = o
        if a == "-c":
            do_create = True

    if filename == None:
        print "Filename not specified"
        return
    else:
        fp = open(filename, 'rb+')
        if format:
            archive = formats[format](filename, fp)
        else:
            for plugin in plugins:
                if plugin(filename, fp).detect():
                    print "Detected format: %s" % (plugin.name)
                    archive = plugin(filename, fp)
                    break

    if archive == None:
        print "Unknown format"
        return

    if do_create:
        archive.create(args)

    if do_list:
        archive.read()
        print "%20s : %8s %8s" % ("Name", "Offset", "Length")
        for name in archive.list:
            data = archive.list[name]
            print "%20s : %8i %8i" % (data["name"], data["start"], data["length"])

    if do_extract:
        archive.read()
        if extractName == None:
            for name in archive.list:
                archive.extract(name)
        else:
            archive.extract(extractName)

if __name__ == "__main__":
    main()

