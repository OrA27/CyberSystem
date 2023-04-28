import socket
from datetime import datetime
from Cyber_Scripts import out_path

s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8)
logs = {}
logs_txt = open(out_path, "a")
log_str = ""

# the full line to be written to the output screen
logs_txt.writelines(f"[{str(datetime.now())}]\t{log_str}")
