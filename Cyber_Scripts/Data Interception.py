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
def send_data(login_page_url):
    driver, user_name_element, password_element, submit_button = get_login_elements(login_page_url)
    user_name_element.send_keys("user name")  # Enter the username
    password_element.send_keys("password")  # Enter password
    submit_button.click()

    time.sleep(1)  # wait for the page to load

    driver.quit()
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


def packet_filter(packet, your_ip, server_ip):
    return (
        IP in packet and
        packet[IP].src == your_ip and
        packet[IP].dst == server_ip and
        TCP in packet and
        Raw in packet and
        b'POST' in packet["Raw"].load  # Check if "POST" is in the packet content
    )


def execute(domain, login_page_url, output: QTextEdit):
    output.append('Data Interception Check')
    output.append(f'Domain: {domain}')
    output.append(f'Login page url: {login_page_url}')
    values_found = 0
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

    my_ip = get_internal_ipv4()
    send_data_thread = threading.Thread(target=enter_login_input, args=[login_page_url, "user name", "password"])
    send_data_thread.start()
    post_packet = sniff(filter=f"tcp", lfilter=lambda pkt: packet_filter(pkt, my_ip, server_ip), count=1)

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
    if values_found == 2:
        print("attack succeeded")
        output.append("The Site is vulnerable to the attack\n\n")
        return True
    else:
        print("attack failed")
        output.append("The site is not vulnerable to the attack\n\n")
        return False

# execute(domain="seatassist.byethost32.com", login_page_url='http://seatassist.byethost32.com/pages/index.php')
