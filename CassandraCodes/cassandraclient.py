#!/usr/bin/env python
import pandas as pd
import numpy as np
import time
import random
import string
import sys
from client_sender import ClientSender

hosts = ['cass-1.CassandraTest.DeepEdgeVideo.emulab.net', 'cass-2.CassandraTest.DeepEdgeVideo.emulab.net', 'cass-3.CassandraTest.DeepEdgeVideo.emulab.net']

'''
For debug, just use only 1 replica
'''
hosts = ['155.98.39.52']
'''
For debug, just use only 1 replica
'''

id_list = []

row_size = 1000  # unit: Byte
field_size = int(row_size / 10)

total_req_num = 5000
read_prob = 0.9 # write_prob = 1 - read_prob

file_time_interval = 'new_intervals_cassandra.txt'


def get_id_list():

    global id_list
    df = pd.read_csv('y_id.csv')
    id_list = list(df['y_id'])
    id_list.sort()
    print('y_id process finished!')
    return 0

def get_time_interval(target_throughput):

    time_interval = np.loadtxt(file_time_interval)
    total_interval = np.sum(time_interval)
    ori_throughput = total_interval/len(time_interval)*1000
    time_interval = time_interval * (ori_throughput/target_throughput)
    return time_interval

def sys_main(target_throughput):

    random.seed(time.time())
    get_id_list()
    time_intervals = get_time_interval(target_throughput)

    payloads = []
    for i in range(0, 10):
        # payload = ''.join([random.choice(string.ascii_letters + string.digits) for nn in range(field_size)])
        payload = ''.join([random.choice(string.ascii_letters) for nn in range(field_size)])
        payloads.append(payload)

    req_sender = ClientSender(hosts, total_req_num, time.time())
    read_count = 0
    for times in range(0, total_req_num):
        if (times % 100 ==0):
            print('have finished', times, 'requests')
        user_id = random.sample(id_list, 1)[0]
        roller = random.random()
        if roller < read_prob:
            req_sender.get_read_latency_non_block(host=hosts[0], user_id=user_id)
            read_count += 1
        else:
            random.shuffle(payloads)
            req_sender.get_update_latency_non_block(host=hosts[0], user_id=user_id, fields=payloads)
        time.sleep(time_intervals[times]/1000)

    time.sleep(100)

    return 0


if __name__ == '__main__':
    print('Cassandra Client Start')
    target_throughput = int(sys.argv[1])
    print('Target throughput is: ', target_throughput, 'rps')
    sys_main(target_throughput)

