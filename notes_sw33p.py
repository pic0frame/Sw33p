# Sw33p Notes

Socket:
sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
sniffer.bind((interface, 0x0003))
pkt = sniffer.recvfrom(2048)[0] 