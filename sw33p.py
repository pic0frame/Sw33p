#!/usr/bin/python3.5

import os
import sys
import re
import time
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
    #print(packet)
    item = pkt[start:end].hex()
    if not item == '10':
        item = item.rstrip('0')
    item_l = len(item)
    item = int(item, 8 * len(item))
    return item

# Change channels and scan
def channel_swap():
    while True:
        for channel in range(1, 14):
            subprocess.run(['iwconfig', interface, 'channel', str(channel)])
           # time.sleep(float(0.4))
            #channel = channel
            #return 1

def rest():
    # Check if packet is an beacon_frame
    i = 0
    while True:
        packet = sweeper.recvfrom(2048)[0]
        if packet[decode_length(packet, 2, 4)] == 128 or packet[2:4] != b'&\x00':
            try:
                SSID = packet[76:(76 + decode_length(packet, 75, 76))].decode()
            except:
                print('Error: Deoding SSID')
        #   print(packet[76])
            MAC = ':'.join(re.findall('.{1,2}', packet[48:55].hex()))
            #list_apx1 = [str(i), SSID, MAC, channel]    
                #print(packet)
            i = i+1
            print('Count: {} | {}'.format(i, str(SSID)))
            print('\t MAC: {}'.format(str(MAC).upper()))
            #time.sleep(float(0.5))
            #print('\t CH : {}\n'.format(decode_length(packet, 112, 113)))

# Thread setup
import threading
t1 = threading.Thread(target=channel_swap)
t2 = threading.Thread(target=rest)

# sw33p                         
t1.start()
t2.start()

# table print
