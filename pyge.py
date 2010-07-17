#!/usr/bin/python

import os, os.path, sys
import struct, re
from array import array
from optparse import OptionParser
import pygelib

def main():
    plugins = pygelib.load_plugins(os.path.join(os.path.dirname(sys.argv[0]), "plugins"))

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
            help="file (archive) to operate on", metavar="FILE")
    parser.add_option("-x", "--extract",
            action="store_true", dest="do_extract", default=False,
            help="extract files")
    parser.add_option("-l", "--list",
            action="store_true", dest="do_list", default=False,
            help="list archive contents")
    parser.add_option("-c", "--create",
            action="store_true", dest="do_create", default=False,
            help="create new archive")
    parser.add_option("-F", "--format", dest="format",
            help="archive format", metavar="FMT")
    parser.add_option("-L", "--format-list",
            action="store_true", dest="do_format_list", default=False,
            help="list known formats")

    (options, args) = parser.parse_args()

    fp = None
    archive = None

    if options.do_format_list:
        for name in plugins:
            print "%15s: %s" % (plugins[name].name, plugins[name].desc)
        return

    if options.filename == None:
        print "Filename not specified"
        return
    else:
        fp = open(options.filename, 'rb+')
        if options.format:
            if options.format in plugins:
                archive = plugins[options.format](options.filename, fp)
            else:
                archive = None
        else:
            for name in plugins:
                if plugins[name](options.filename, fp).detect():
                    print "Detected format: %s" % (plugins[name].name)
                    archive = plugins[name](options.filename, fp)
                    break

    if archive == None:
        print "Unknown format"
        return

    if options.do_create:
        archive.create(args)

    if options.do_list:
        archive.print_list()

    if options.do_extract:
        if args:
            for name in args:
                archive.extract(name)
        else:
            archive.extract()

if __name__ == "__main__":
    main()

