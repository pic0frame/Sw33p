#!/usr/bin/python3.5

import os
import sys
import socket
import subprocess

if os.geteuid() != 0:
	sys.exit('Run as root!')

try:
	interface = sys.argv[1]
	interfaces = os.listdir('/sys/class/net')
	if not interface in interfaces:
		sys.exit(0)
except:
	print('No valid interface.')
	sys.exit(0)

sweeper = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
sweeper.bind((interface, 0x0003))

def check_header_lenght(pkt):
	header = str(pkt[2:4].hex()).rstrip('0')
	l = 8 * len(header)
	lenght = int(header, l)
	return lenght 

while True:
	for channel in range(1, 13):
		subprocess.run(['iwconfig', interface, 'channel', str(channel)])
		print('Channel: {}'.format(channel))
		packet = sweeper.recvfrom(2048)[0]

		if packet[check_header_lenght(packet)] == 128:
			i = i + 1
			print('{} :This is an frame and has a header_leght of {}'.format(i, check_header_lenght(packet)))


check_header_lenght(packet)


