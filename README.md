# Sw33p

## About

Scan WIFI networks and generate a list with that will contain the ESSID,
BSSID, CHANNEL, SIGNAL, ENCRYPTION-TYPE and the geographic coordinate.

This project must be written in python3.5! No third party modules are allowed.

## TODO

*MUST HAVE*
  - [ ] Check for dependencies;
    - [x] aircrack-ng
    - [x] iwconfig
    - [ ] interface is in monitoring mode
    - [x] SUDO
  - [x] Create a SOCKET;
  - [x] Decode the binary output from the socket using the 802.11 rfc;
    - [x] Check frame for type;
    - [x] Check every header for it's lenght;
    - [x] Decode ESSID
    - [x] Decode BSSID
    - [x] Decode channel
    - [ ] Decode encryption type
  - [ ] Add 5ghz support
  - [x] Add multithreading
  - [ ] Add 5ghz channel support
  - [ ] Add Logging to the whole program
 *SHOULD HAVE*
  - [ ] Change channel with the SOCKET and not with 'iwconfig'
  - [ ] Set interface in monitoring mode with the SOCKET and not with 'airmon-ng'
  - [ ] Determinate geographic position of the host-device;
  - [ ] Parse all data on a map;
  - [ ] Arguments
    - [ ] help, interface, run_time etc


## Output example
This software is still in making. A.T.M. is the output printed for debugging purposes.

```
→ sudo python3.5 sw33p.py wlp58s0mon  
Count: 1 	 Channel: 11 	 S: 80:2A:00:00:ED:87 	 D: FF:FF:FF:FF:FF:FF 	 ESSID: blabla-voip
Count: 2 	 Channel: 6 	 S: 82:2A:00:00:ED:87 	 D: FF:FF:FF:FF:FF:FF 	 ESSID: blabla
Count: 3 	 Channel: 1 	 S: 82:2A:00:00:ED:1A 	 D: FF:FF:FF:FF:FF:FF 	 ESSID: blabla
Count: 4 	 Channel: 11 	 S: 82:2A:00:00:ED:87 	 D: FF:FF:FF:FF:FF:FF 	 ESSID: blabla
Count: 5 	 Channel: 1 	 S: 92:2A:00:00:ED:1A 	 D: FF:FF:FF:FF:FF:FF 	 ESSID: It hurts when IP
```

