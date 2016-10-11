# Sw33p Notes

Socket:
sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
sniffer.bind((interface, 0x0003))
pkt = sniffer.recvfrom(2048)[0] 

# Positions needed information
'''
length_header: [2:4]
length_ESSID: [74]

>>> lenght_hex = test[2:4].hex()
>>> lenght_str = str(l).rstrip('0')
>>> a = 8 * len(lenght_str)
>>> lenght = int(lenght_str, a)
>>> print(lenght)
36