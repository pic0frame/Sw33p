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
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
s.bind((interface, 0x003)) # Bind socket to interface

# Decode length byte
def decode_length( pkt, start, end):
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

def sweeper():
    while True:
    # Check if packet is an beacon_frame
        packet = s.recvfrom(2048)[0]
        if packet[decode_length(packet, 2, 4)] == 128 and packet[38:39] == b'\x80':

            

            SSID_POS = 76 + ord(packet[75:76])

            essid_l = ord(packet[75:76])

            SSID = packet[76:SSID_POS].decode()

            MAC = ':'.join(re.findall('.{1,2}', packet[48:55].hex()))

            suported_rates = (SSID_POS + ord(packet[SSID_POS+2:SSID_POS+3])) + 2

            CH = decode_length(packet, suported_rates, suported_rates+1)
            print(packet)

            


            


            print('MAC\t\t\t CH\t essid_l\t ESSID')
            print('{}\t {} \t {}\t {}'.format(MAC, CH, essid_l, SSID))



# Thread setup
import threading
t1 = threading.Thread(target=channel_swap)
t2 = threading.Thread(target=sweeper)

# sw33p                         
t1.start()
t2.start()