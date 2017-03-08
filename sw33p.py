#!/usr/bin/python3.5

import os
import sys
import time
import socket
import threading
import subprocess
import s_decode

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
    sys.exit('No valid interface was given.')


# Change channels
def channel_swap():
    # time.sleep(2)
    while True:
        for channel in range(1, 14):
            time.sleep(0.3)
            subprocess.run(['iwconfig', interface, 'channel', str(channel)])

# Socket setup
sweeper = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
# Bind socket to interface
sweeper.bind((interface, 0x0003))


# This is the main function. It will grab a packet and decode it's headers
def sw33p():
    i = 0
    while True:
        packet = sweeper.recvfrom(2048)[0]
        th = s_decode.TypeHeader(packet)
        fdh = s_decode.FixedDataHeader(packet)
        tdh = s_decode.TaggeDataHeader(packet)
        if th.get_type() == 'Frame':
            source = th.get_source()
            destination = th.get_destination()
            essid = tdh.get_essid().decode('utf8')
            ch = tdh.get_channel()
            i = i + 1
            print('Count: {} \t Channel: {} \t S: {} \t D: {} \t ESSID: {}'.format(i, ch, source, destination, essid))

# Thread setup
t1 = threading.Thread(target=channel_swap)
t2 = threading.Thread(target=sw33p)

# sw33p                         
t1.start()
t2.start()