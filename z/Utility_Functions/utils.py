import nmap3
import socket as s
from datetime import datetime
from deprecated import deprecated

ports = [
    21, 22, 25, 80, 110, 143, 389,
    443, 636, 1433, 1883, 3306, 5432,
    8080, 8081, 8088, 8443, 8888, 9090,
    9443, 27017]
ports2 = range(80, 65000, 7)


@deprecated(reason="use the nmap function")
def get_open_ports(ip: str):
    """
    checks for open ports.

    :param ip: IP address to check
    :return: list of open ports
    """
    server_ip = s.gethostbyname(ip)
    print(f"Scanning host: {server_ip}")
    open_ports = []
    for port in ports:
        print(f"testing port {port}")
        # create a socket and attempt to establish connection
        sk = s.socket(s.AF_INET, s.SOCK_STREAM)
        sk.settimeout(0.05)
        try:
            check_port = sk.connect_ex((server_ip, port))
            if check_port == 0:
                # if connection is successful, port is open and added to list
                print("Port {}: Open".format(port))
                open_ports.append(port)
                sk.close()
        except Exception as e:
            print(f"error occurred: {e}")
        finally:
            if len(open_ports) >= 2:
                break

    return open_ports


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
