# import nmap3
# import nmap
from scapy.all import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import socket as s
from datetime import datetime
from deprecated import deprecated
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys

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

"""
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
"""

"""
def port_discovery(address="127.0.0.1"):
    start = time.time()
    nmScan = nmap.PortScanner()
    nmScan.scan(address, "1-65535")
    for host in nmScan.all_hosts():
        print('Host : %s (%s)' % (host, nmScan[host].hostname()))
        print('State : %s' % nmScan[host].state())
        for proto in nmScan[host].all_protocols():
            print('----------')
            print('Protocol : %s' % proto)

            allports = nmScan[host][proto].keys()
            sorted(allports)
            for port in allports:
                print('port : %s\tstate : %s' % (port, nmScan[host][proto][port]['state']))
            end = time.time()
            print((end - start) / 60)
            return allports

"""


# Easier to change the browser here in case of an error
def create_driver(page_url):
    driver = webdriver.Edge()
    driver.get(page_url)
    time.sleep(1)  # wait for the page to load
    return driver


def enter_login_input(login_page_url, user_name, password):
    driver = create_driver(login_page_url)

    # Find and fill the fields with desired values
    input_elements = driver.find_elements(By.TAG_NAME, "input")
    input_elements = [element for element in input_elements if element.is_displayed()]

    for i in range(2):
        name = input_elements[i].get_attribute("name")
        # print("name: " + name)
        script = f"document.getElementsByName('{name}')[0].type = 'text';"
        driver.execute_script(script)

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
    input_elements[0].send_keys(user_name)
    input_elements[1].send_keys(password)

    # perform login
    button_elements[-1].click()

    time.sleep(1)  # wait for the page to load

    try:
        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE)  # Escape popups
        actions.perform()
    except UnexpectedAlertPresentException:
        alert = driver.switch_to.active_element  # closing the popup

    # lookup failed -> abort
    try:
        new_url = driver.current_url
        passed = login_page_url != new_url
        return passed
    except:
        pass
    finally:
        # Close the browser window
        driver.quit()

    # return driver, input_elements[0], input_elements[1], button_elements[-1]
