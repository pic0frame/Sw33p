# Sw33p Notes

Socket:
sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
sniffer.bind((interface, 0x0003))
pkt = sniffer.recvfrom(2048)[0] 

# Positions needed information
'''


>>> lenght_hex = test[2:4].hex()
>>> lenght_str = str(l).rstrip('0')
>>> a = 8 * len(lenght_str)
>>> lenght = int(lenght_str, a)
>>> print(lenght)
36

theurls = ["http://google.com", "http://yahoo.com"]

q = Queue.Queue()

for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    t.daemon = True
    t.start()

s = q.get()
print s


theurls = ["http://google.com", "http://yahoo.com"]

q = Queue.Queue()

for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    t.daemon = True
    t.start()

s = q.get()
print s
#----------------------------#
# length_header: [2:4]
# length_ESSID: [76 + 75:76]
# SSID = [a(2:4) + 76 + ]

radiotop_lenght(rl) = [2:4]
802.11_beacon(802_b) = rl + int(24)
802.11_wireless:
  - fixed_param = 802_b + int(12)
  - tagged_parm:
    - ESSID=(fixed_param + int(2)) + (decode(fixed_param +2))
    - supported_rates(sr) = ESSID + decode(ESSID + int(2))
    - channel = sr + decode(1)

 10 + 6


'''
'''
radiotab_header = decode_length(pkg, 2, 4)

 >>> def data(pkt):
...   radiotab_header = decode_length(pkt, 2, 4)
...   if radiotab_header == 38 and pkt[38:39] == b'\x80':
...     return 'beacon'

# SSID
ssid_start = 76
ssid_len = ord(pkg[75:76])
ssid_end = 76 + ord(pkg[75:76])
ssid = pkg[ssid_start:ssid_end].decode()

# MAC
mac = pkg[48:55].hex()
mac = ':'.join(re.findall('.{1,2}', mac))
sup_rate_len = decode_length(pkg, ssid_end+1, ssid_end+2) + 2


