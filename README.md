# Sw33p

## About

Scan WIFI networks and generate a list with that will contain the ESSID,
BSSID, CHANNEL, SIGNAL, ENCRYPTION-TYPE and the geographic coordinate.

This project must be written in python3.5! No third party modules are allowed.

## TODO
  - [x] Check for dependencies;
  - [x] Create a SOCKET and save the data;
  - [x] Decode the binary output from the socket using the 802.11 rfc;
    - [x] Check frame for type; (we need beacon frame 80/128)
    - [x] Check frame for lenght;
    - [ ] Check frame for encryption;
  - [ ] Determinate geographic position of the host-device;
  - [ ] Parse all data on a map;

## Output example ATM

```
→ sudo python3.5 sw33p.py wlp58s0mon  
Count: 1 	 Channel: 11 	 S: 80:2A:00:00:ED:87 	 D: FF:FF:FF:FF:FF:FF 	 ESSID: blabla-voip
Count: 2 	 Channel: 6 	 S: 82:2A:00:00:ED:87 	 D: FF:FF:FF:FF:FF:FF 	 ESSID: blabla
Count: 3 	 Channel: 1 	 S: 82:2A:00:00:ED:1A 	 D: FF:FF:FF:FF:FF:FF 	 ESSID: blabla
Count: 4 	 Channel: 11 	 S: 82:2A:00:00:ED:87 	 D: FF:FF:FF:FF:FF:FF 	 ESSID: blabla
Count: 5 	 Channel: 1 	 S: 92:2A:00:00:ED:1A 	 D: FF:FF:FF:FF:FF:FF 	 ESSID: It hurts when IP
```

