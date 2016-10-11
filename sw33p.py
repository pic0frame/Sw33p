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

def decode_length( p, s, e):
    a = p[s:e]
    if type(a) == bytes:
        a = a.hex()
        if not a == '10':
            a = a.rstrip('0')
        byte = 8 * len(a)
        a = int(a, byte)
    else:
        a = codecs.decode(a, 'hex')
        byte = 8 * len(a)
        a = int(a, byte)
    return a

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
            print('{}: ===> {} :  Found beacon_frame with header_length of "{}" on channel: "{}"'.format(i, SSID, decode_length(packet, 2, 4), channel))