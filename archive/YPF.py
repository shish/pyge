from archive import PygeArchive, GenericEntry
import struct
import re


#
# YPF Archive, found in Eroge
#
class YPF(PygeArchive):
    name = "YPF (YU-RIS)"
    desc = "YU-RIS Script Engine"
    sig = "YPF\x00"
    ext = "ypf"
    header_fmt = "<4s4xi24x"
    entry_fmt = "xxx3sxxiiiii"  # 45 bytes
    
    def _readindex(self):
        #print "Entry count:", self.count
        last_valid_name = None
        for n in xrange(self.count):
            try:
                # <entry_type:1><filename:Ns><metadata:45x>
                # there doesn't seem to be a direct mapping between entry_type
                # and len(name); but trial and error suggests that there is an
                # *indirect* mapping, so here is what I've found mapped by hand...
                entry_type = self.file.read(1)
                entry_len = {
                    "\x8C": 27,
                    
                    "\xF5": 32,             "\xEF": 34,
                    "\xEC": 35, "\xF1": 36, "\xF0": 37, "\xF3": 38, "\xE6": 39,

                    "\xED": 40, "\xF2": 41, "\xEB": 42, "\xE4": 43, "\xE9": 44,
                    "\xE8": 45, "\xE7": 46, "\xEE": 47, "\xE5": 48, "\xEA": 49,
                    
                    "\xE1": 50, "\xE2": 51, "\xE3": 52, "\xE0": 53, "\xDC": 54,
                    "\xDE": 55, "\xDD": 56, "\xDF": 57, "\xDB": 58, "\xDA": 59,
                    
                    "\xD6": 60, "\xD8": 61, "\xD7": 62, "\xD9": 63, "\xD5": 64,
                    "\xD4": 65, "\xD0": 66,
                }[entry_type]
                #print "0x%02X -> %d" % (ord(entry_type), entry_len),
            except KeyError:
                # files often have the same start, eg cgsys/0001.png, cgsys/0002.png, ...
                # so if we don't know how long an entry is supposed to be, scan the data
                # looking for the next similar filename
                errpos = self.file.tell() - 1
                data_len = self.file.read(1000).find(last_valid_name[0:4], 20)
                print("Unknown entry_type 0x%02X at %d (Guess \"\\x%02X\": %d,)" % (
                    ord(entry_type), errpos,
                    ord(entry_type), data_len
                ))
                self.file.seek(-1000, 1)
                if data_len == -1:
                    break
                
            entry_data_len = struct.calcsize(self.entry_fmt)
            entry_name_len = entry_len - entry_data_len
            
            entry_name_dat = self.file.read(entry_name_len)
            entry_data_dat = self.file.read(entry_data_len)
            
            name = entry_name_dat
            ext, length, _length2, offset, _x1, _x2 = struct.unpack(self.entry_fmt, entry_data_dat)
            
            name = self.xorit(name).replace("|", "/")
            name = re.sub("[^a-zA-Z0-9\.\_\-/]", lambda x: "_0x%02X" % ord(x.group(0)), name)
            name = name.replace("_0x7F", "-")
            ext = self.xorit(ext)

            #print repr(name), repr(ext), length, offset # x1 and x2 have no obvious meaning v.v
            self.list.append(GenericEntry(self, name + "." + ext, offset, length))
            
            if not last_valid_name:
                last_valid_name = entry_name_dat
                
            #if n == 500:
            #    break

    def xorit(self, data):
        data = [ord(x) for x in data]
        for i in xrange(len(data)):
            data[i] ^= 159
        data = "".join([chr(x) for x in data])
        return data
