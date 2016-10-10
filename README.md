# Sw33p

## About

Scan WIFI networks and generate a list with that will contain the ESSID,
BSSID, CHANNEL, SIGNAL, ENCRYPTION-TYPE and the geographic coordinate.

This project must be written in python3.5! No third party modules are allowed.

## TODO
  - [ ] Check for dependencies;
  - [x] Create a SOCKET and save the data;
  - [ ] Decode the binary output from the socket using the 802.11 rfc;
    - [ ] Check frame for type; (we need beacon frame 80/128)
    - [ ] Check frame for lenght;
    - [ ] Check frame for encryption;
  - [ ] Create an install script;
  - [ ] Determinate geographic position of the host-device;
  - [ ] Parse all data on a map;


