from scapy.all import sniff


# analyze packets
def analyze_packet(packet):
    # Process and analyze the packet here
    print(packet.summary())


# Sniff packets on a specific interface, applying a filter to capture packets related to a specific site
# For example, sniff packets going to or coming from "localhost"
sniff(filter="host localhost", prn=analyze_packet)
