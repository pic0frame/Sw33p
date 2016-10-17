#!/usr/bin/python3.5

import os
import sys
import re
import time
import socket
import codecs
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
    print('No valid interface was given.')
    sys.exit()

# Change channels
def channel_swap():
   # time.sleep(2)
    while True:
        for channel in range(1, 14):
            time.sleep(0.3)
            subprocess.run(['iwconfig', interface, 'channel', str(channel)])

# Socket setup
sweeper = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
sweeper.bind((interface, 0x0003)) # Bind socket to interface

def sw33p():
    i = 0
    while True:
        packet = sweeper.recvfrom(2048)[0]
        th = s_decode.type_header(packet)
        fdh = s_decode.f_data_header(packet)
        tdh = s_decode.t_data_header(packet)
        if th.getType() == 'Frame':
            source = th.getSource()
            destination = th.getDestination()
            essid = tdh.getESSID().decode('utf8')
            ch = tdh.getChannel()
            i = i + 1
            print('Count: {} \t Channel: {} \t S: {} \t D: {} \t ESSID: {}'.format(i, ch, source, destination, essid))

# Thread setup
import threading
t1 = threading.Thread(target=channel_swap)
t2 = threading.Thread(target=sw33p)

# sw33p                         
t1.start()
t2.start()