import socket
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP, TCP
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
from Cyber_Scripts import *
from PyQt6.QtWidgets import QTextEdit

"""
def get_internal_ipv4():
    try:
        # Create a socket and connect to a remote server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to Google's public DNS server

        # Get the local IP address
        internal_ip = s.getsockname()[0]

        s.close()
        return internal_ip
    except Exception as e:
        print("Error:", e)
        return None
"""


def get_internal_ip():
    try:
        internal_ip = socket.gethostbyname(socket.gethostname())
        return internal_ip
    except socket.error:
        return None


def get_ip_address(url):
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except socket.error:
        return None

def packet_filter(packet, your_ip, server_ip):
    return (
        IP in packet and
        packet[IP].src == your_ip and
        packet[IP].dst == server_ip and
        TCP in packet and
        Raw in packet and
        b'POST' in packet["Raw"].load  # Check if "POST" is in the packet content
    )


def execute(login_page_url):
    try:
        domain = login_page_url.split("/")[2]
        values_found = 0

        """
        response = None
        while not response:
            # Craft a DNS query
            dns_query = IP(dst='8.8.8.8') / UDP(sport=RandShort(), dport=53) / DNS(rd=1, qd=DNSQR(qname=domain))

            # Send the DNS query and receive the response
            response = sr1(dns_query, timeout=1, verbose=0)

        # Parse the response to obtain the IPv4 address
        if response and DNSRR in response:
            server_ip = response[DNSRR].rdata
        else:
            server_ip = "0.0.0.0"
        """

        # login_page_ip = get_ip_address(login_page_url)
        domain = login_page_url.split("/")[2:][0]
        login_page_ip = socket.gethostbyname(domain)
        my_ip = get_internal_ip()
        if not my_ip or not login_page_ip:
            raise Exception
        send_data_thread = threading.Thread(target=enter_login_input, args=[login_page_url, "user name", "password"])
        send_data_thread.start()
        post_packet = sniff(filter=f"tcp", lfilter=lambda pkt: packet_filter(pkt, my_ip, login_page_ip), count=1)

        packet_content = post_packet[0]["Raw"].load.decode()
        packet_parts = packet_content.split("\r\n")
        packet_variables_part = packet_parts[-1]
        text_variables = packet_variables_part.split("&")
        for text_variable in text_variables:
            variable_vals = text_variable.split("=")
            if len(variable_vals) > 1:
                if variable_vals[1] in ["user+name", "password"]:
                    values_found += 1
            else:
                break
        return values_found == 2
    except:
        return None


# execute(login_page_url='http://seatassist.byethost32.com/pages/index.php')