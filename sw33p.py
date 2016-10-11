#!/usr/bin/python3.5

import os
import sys
import re
import queue
import socket
import codecs
import threading
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

# Decode length byte
def decode_length( pkt, start, end):
    item = pkt[start:end].hex()
    if not item == '10':
        item = item.rstrip('0')
    item = int(item, 8 * len(item))
    return item

# sw33p
i = 0
while True:
    # Change channels and scan
    for channel in range(1, 14):
        subprocess.run(['iwconfig', interface, 'channel', str(channel)])
        packet = sweeper.recvfrom(2048)[0]
    # Check if packet is an beacon_frame
        if packet[decode_length(packet, 2, 4)] == 128:
            i = i + 1
            SSID = packet[76:(76 + decode_length(packet, 75, 76))].decode()
            MAC = ':'.join(re.findall('.{1,2}', packet[48:55].hex()))
            
            print('{}: \t {} \t\t\t {} \t\t\t {}'.format(i, SSID, MAC, channel))

# table print