#!/usr/bin/python3.5

import re

def decode_length(pkt, start, end):
    item = pkt[start:end].hex()
    if not item == '10':
        item = item.rstrip('0')
    item = int(item, 8 * len(item))
    return item

# FRAME_HEADERS
class radiotab_header(object):
    frame = object
    def __init__(self, frame):
        self.len = decode_length(frame, 2, 4)
        self.start = 0
        self.end = self.len

    def getLen(self):
        return self.len
    def getStart(self):
        return self.start
    def getEnd(self):
        return self.end

class type_header(object):
    def __init__(self, object):
        self.frame = object
        self.start = radiotab_header(self.frame).getEnd()
        self.len = 24
        self.end = self.start + self.len

    def getStart(self):
        return self.start
    def getEnd(self):
        return self.end
    def getType(self):
        if self.frame[self.start:self.start+1] == b'\x80':
            return 'Frame'
        #This can be expanded later
    def getSource(self):
        Source = self.frame[self.start+10:self.start+16].hex()
        Source = str(':'.join(re.findall('.{1,2}', Source))).upper()
        return Source
    def getDestination(self):
        dest = self.frame[self.start+4:self.start+10].hex()
        dest = str(':'.join(re.findall('.{1,2}', dest))).upper()
        return dest
    def getBSSID(self):
        bssid = self.frame[self.start+16:self.start+22].hex()
        bssid = str(':'.join(re.findall('.{1,2}', bssid))).upper()
        return bssid

class f_data_header(object):
    def __init__(self, object):
        self.frame = object
        self.len = 12
        self.start = type_header(self.frame).getEnd()
        self.end = self.start + self.len
    def getStart(self):
        return self.start
    def getEnd(self):
        return self.end

class t_data_header(object):
    def __init__(self, object):
        self.frame = object
        self.start = f_data_header(self.frame).getEnd()

    def getESSID(self):
        essid_start = self.start+2 
        essid_len = ord(self.frame[self.start+1:self.start+2])
        essid_end = essid_start + essid_len
        essid = self.frame[essid_start:essid_end]
        self.essid_hlen = 2 + essid_len
        self.essid_hend = self.start + self.essid_hlen
        return essid

    def getChannel(self):
        self.sr_start = self.essid_hend
        self.sr_len = decode_length(self.frame, self.sr_start+1, self.sr_start+2)
        self.sr_end = self.essid_hend + self.sr_len + 2
        channel = decode_length(self.frame, self.sr_end+2, self.sr_end+3)
        return channel