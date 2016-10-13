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

# Decode length byte into decimals
def decode_length( pkt, start, end):
    item = pkt[start:end].hex()
    if not item == '10':
        item = item.rstrip('0')
    item = int(item, 8 * len(item))
    return item

# def decode_info(pkt):
#     radiotap = decode_length(pkt, 2, 4)
#     beacon = radiotap + 24
#     fixed_parm = beacon + 12
#     essid_l = decode_length(pkt, int(fixed_parm+2), int(fixed_parm+3))
#     ESSID = fixed_parm+2 + essid_l
#     essid = packetx2[fixed_parm+2:fixed_parm+2 + essid_l].decode()
#     supported_rates = (ESSID + 1) + decode_length(pkt, ESSID+1, ESSID+2)
#     CH = decode_length(pkt, supported_rates+2, supported_rates+3)
#     MAC = str(':'.join(re.findall('.{1,2}', pkt[radiotap+10:radiotap+17].hex()))).upper

# Change channels
def channel_swap():
    while True:
        for channel in range(1, 14):
            subprocess.run(['iwconfig', interface, 'channel', str(channel)])
            #time.sleep(float(0.5))
            #channel = channel
            #return 1

def rest():
    i = 0
    #time.sleep()
    while True:
        # sw33p packet
        packet = sweeper.recvfrom(2048)[0]
        # Check if packet is an beacon_frame
        if packet[decode_length(packet, 2, 4)] == 128:
            # Try to decode ESSID (some packets look like beacons but they are not)
            try:
               # decode_info(packet)
                radiotap = decode_length(packet, 2, 4)
                beacon = radiotap + 24
                fixed_parm = beacon + 12
                essid_l = decode_length(packet, int(fixed_parm+2), int(fixed_parm+3))
                ESSID = fixed_parm+2 + essid_l
                essid = packet[fixed_parm+2:fixed_parm+2 + essid_l].decode()
                print(essid)
                supported_rates = (ESSID + 1) + decode_length(packet, ESSID+1, ESSID+2)
                CH = decode_length(packet, supported_rates+2, supported_rates+3)
                print(CH)
                MAC = ':'.join(re.findall('.{1,2}', packet[radiotap+10:radiotap+17].hex()))
                print(MAC)

            except:
                pass
                print('decode_info failed!!')

            #print(radiotap)
            #print(beacon)
            #print(fixed_parm)
            #print(essid_l)
            #print(ESSID)
            #print(essid)
            #print(MAC)
            #print(supported_rates)
            #print('{}\n'.format(CH))


# Thread setup
import threading
t1 = threading.Thread(target=channel_swap)
t2 = threading.Thread(target=rest)

# sw33p                         
t1.start()
t2.start()

# table print
