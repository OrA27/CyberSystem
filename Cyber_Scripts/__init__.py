import nmap3
from scapy.all import *
import socket as s
from datetime import datetime
from deprecated import deprecated

# variables
# path to the output file
out_path = "../Output.txt"
# targeted IPs
IP_list = ['192.168.68.59']
# source IP of the adversary
source_ip = ""
# source port of adversary
source_port = 80
# port of the targeted IP
target_port = 80


# functions
def get_open_ports_nmap(ip: str, amount: int = 50):
    open_ports = []
    nm = nmap3.Nmap()
    nm.scan_top_ports(ip, default=amount)
    my_dict = dict(nm.top_ports)  # turn to dictionary
    port_list = next(iter(my_dict.items()))[1]['ports']  # get the ports list
    for port in port_list:
        if port['state'] == 'open':
            open_ports.append(int(port['portid']))
    return open_ports
