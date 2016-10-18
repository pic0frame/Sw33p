#!/usr/bin/python3.5

import re

# This function will decode the header length.
def decode_length(pkt, start, end):
    item = pkt[start:end].hex()
    if not item == '10':
        item = item.rstrip('0')
    item = int(item, 8 * len(item))
    return item

'''I have create classes for every section/header
of the binary packet. This give's me alot more
flexibility for the upgrates in the future'''
class RadioTypeHeader(object):
    def __init__(self, frame):
        self.len = decode_length(frame, 2, 4)
        self.start = 0
        self.end = self.len
        self.frame = frame

    def get_len(self):
        return self.len

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end


# This section contains the source, destination and antena info
class TypeHeader(object):
    def __init__(self, frame):
        self.frame = frame
        self.start = RadioTypeHeader(self.frame).get_end()
        self.len = 24
        self.end = self.start + self.len

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_type(self): #Check for type of frame
        if self.frame[self.start:self.start+1] == b'\x80':
            return 'Frame'
        #This can be expanded later

    def get_source(self): #decode source
        source = self.frame[self.start+10:self.start+16].hex()
        source = str(':'.join(re.findall('.{1,2}', source))).upper()
        return source

    def get_destination(self): # decode destination
        dest = self.frame[self.start+4:self.start+10].hex()
        dest = str(':'.join(re.findall('.{1,2}', dest))).upper()
        return dest

    def get_bssid(self): #decode bssid
        bssid = self.frame[self.start+16:self.start+22].hex()
        bssid = str(':'.join(re.findall('.{1,2}', bssid))).upper()
        return bssid


# This header contains the rest of the data e.g. essid, channel,
# radiotypes, and security. There are two subheaders: tagged and fixed

# Fixed data header
class FixedDataHeader(object):
    def __init__(self, frame):
        self.frame = frame
        self.len = 12
        self.start = TypeHeader(self.frame).get_end()
        self.end = self.start + self.len

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

# Tagged data header
class TaggeDataHeader(object):
    def __init__(self, frame):
        self.frame = frame
        self.start = FixedDataHeader(self.frame).get_end()

    def get_essid(self): # decode ESSID
        essid_start = self.start+2
        essid_len = ord(self.frame[self.start+1:self.start+2])
        essid_end = essid_start + essid_len
        essid = self.frame[essid_start:essid_end]
        self.essid_hlen = 2 + essid_len
        self.essid_hend = self.start + self.essid_hlen
        return essid

    def get_channel(self): # Decode channel
        self.sr_start = self.essid_hend
        self.sr_len = decode_length(self.frame, self.sr_start+1, self.sr_start+2)
        self.sr_end = self.essid_hend + self.sr_len + 2
        channel = decode_length(self.frame, self.sr_end+2, self.sr_end+3)
        return channel
