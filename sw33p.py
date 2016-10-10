#!/usr/bin/python3.5

import os
import sys
import socket
import codecs
import subprocess

# Check for root
if os.geteuid() != 0:
    sys.exit('This program needs root privileges!')

# Check if interface has been given
try:
    interface = sys.argv[1]
    interfaces = os.listdir('/sys/class/net')
    if not interface in interfaces:
        sys.exit()
except:
    print('No valid interface was given.')
    sys.exit()

# Socket setup
sweeper = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
sweeper.bind((interface, 0x003)) # Bind socket to interface

def decode_length( p, s, e ):
    item = str(p[s:e].hex()).rstrip('0')
    byte = 8 * len(item)
    item = int(item, byte)
    return item

def decode_lengthx1( p, s ):
    a = str(p[s])
    item = codecs.decode(str(a), 'hex')
    item = str(item.hex())
    print(item)
    # byte = 8 * len(item)
    # item = int(item, byte)
    return item

# sw33p
i = 0
while True:
    # Change channels and scan
    for channel in range(1, 14):
        subprocess.run(['iwconfig', interface, 'channel', str(channel)])
        print('Scanning channel {} ...'.format(channel))
        packet = sweeper.recvfrom(2048)[0]
    # Check if packet is an beacon_frame
        if packet[decode_length(packet, 2, 4)] == 128:
            i = i + 1
            print('{}: Found beacon_frame with header_length of {}'.format(i, decode_length(packet, 2, 4)))
            print(decode_lengthx1(packet, 74))
            #a = packet[74]
            #print(codecs.decode(str(a), 'hex'))

