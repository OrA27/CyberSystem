from scapy.all import *

# path to the output file
out_path = "../Output.txt"
# targeted IPs
IP_list = []
# source IP of the adversary
source_ip = ""
# source port of adversary
source_port = RandShort()
# port of the targeted IP
target_port = RandShort()
