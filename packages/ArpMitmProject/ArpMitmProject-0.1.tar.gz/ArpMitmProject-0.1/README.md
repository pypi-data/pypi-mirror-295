# ArpMitmProject
created by Matan Nafgi

`ArpMitmProject` is a Python library for performing ARP spoofing and man-in-the-middle (MITM) attacks.

## Installation

You can download ArpspoofMITM by cloning the Git Repo and simply installing its requirements
```
~ ❯❯❯ sudo apt-get update && sudo apt-get install scapy

~ ❯❯❯ gh repo clone https://github.com/Nathanafgi/ArpMitmProject.git
```
## bash
```
~ ❯❯❯ pip install Arp-Mitm
```

## Usage
```
make sure that IP forwarding is enabled on your attacker machine so that packets from the victim can reach the intended destination (the target).


sudo python3 arpmitm.py <victim_ip> <target_ip> <iface>
```
#default interface will be chosen if not specified

# Disclaimer

ArpMitmProject is provided as is under the MIT Licence (as stated below). 
It is built for educational purposes *only*. If you choose to use it otherwise, the developers will not be held responsible. Please, do not use it with evil intent.
