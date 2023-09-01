import socket
import netifaces as ni
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP, TCP
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading

def send_data():
    url = 'http://seatassist.byethost32.com/pages/index.php'

    driver = webdriver.Chrome()
    driver.get(url)

    time.sleep(1)  # wait for the page to load

    # Find and fill the fields with desired values
    input_elements = driver.find_elements(By.TAG_NAME, "input")
    input_elements = [element for element in input_elements if element.is_displayed()]

    input_names = []
    for i in range(2):
        name = input_elements[i].get_attribute("name")
        # print("name: " + name)
        script = f"document.getElementsByName('{name}')[0].type = 'text';"
        driver.execute_script(script)

    input_elements[0].send_keys("user name")  # Enter the username
    input_elements[1].send_keys("password")  # Enter password

    # Find and click the submit button
    button_elements = driver.find_elements(By.TAG_NAME, "button")
    button_elements = [element for element in button_elements if element.is_displayed() and
                       (element.get_attribute("type") == "submit" or
                        element.get_attribute("disabled type") == "submit")]
    if len(button_elements) == 0:
        button_elements = input_elements
        button_elements = [element for element in button_elements if element.is_displayed() and
                           (element.get_attribute("type") == "submit" or
                            element.get_attribute("disabled type") == "submit")]
    button_elements[-1].click()

    time.sleep(1)  # wait for the page to load

    driver.quit()

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
        # packet[TCP].dport == 80 and  # Assuming HTTP is on port 80
        Raw in packet and
        b'POST' in packet["Raw"].load  # Check if "POST" is in the packet content
    )


# Replace 'example.com' with the domain you want to resolve
domain = "seatassist.byethost32.com"
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
    print(f"IPv4 Address of {domain}: {server_ip}")
else:
    server_ip = "0.0.0.0"
    print(f"DNS resolution failed for {domain}")

my_ip = get_internal_ipv4()
send_data_thread = threading.Thread(target=send_data)
send_data_thread.start()
post_packet = sniff(filter=f"tcp", lfilter=lambda pkt: packet_filter(pkt, my_ip, server_ip), count=1)

# print(packet["Raw"].load)
packet_content = post_packet[0]["Raw"].load.decode()
packet_parts = packet_content.split("\r\n")
packet_variables_part = packet_parts[-1]
# packet_variables = dict()
text_variables = packet_variables_part.split("&")
for text_variable in text_variables:
    variable_vals = text_variable.split("=")
    if len(variable_vals) > 1:
        print("value: " + variable_vals[1])
        if variable_vals[1] in ["user+name", "password"]:
            values_found += 1
    else:
        break
if values_found == 2:
    print("attack succeeded")
else:
    print("attack failed")
    """
    variable_name = variable_vals[0]
    variable_val = variable_vals[1]
    packet_variables[variable_name] = variable_val
for variable in packet_variables.items():
    print(variable)
    """
"""
import socket

# Replace 'example.com' with the domain you want to resolve
domain = 'seatassist.byethost32.com'

try:
    # Get the IPv4 address associated with the domain
    ipv4_address = socket.gethostbyname(domain)
    print(f"IPv4 Address of {domain}: {ipv4_address}")
except socket.gaierror as e:
    print(f"Error resolving {domain}: {e}")
"""