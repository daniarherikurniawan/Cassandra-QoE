#!/usr/bin/env python
import pandas as pd
import numpy as np
import time
import random
import string
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

row_size = 5000  # unit: Byte
field_size = int(row_size / 10)

total_req_num = 5000

read_prob = 0.9 # write_prob = 1 - read_prob

sleep_period = 0.001

def get_id_list():

    global id_list
    df = pd.read_csv('y_id.csv')
    id_list = list(df['y_id'])
    id_list.sort()
    print('y_id process finished!')
    return 0


def sys_main():

    random.seed(time.time())
    get_id_list()
    payloads = []
    for i in range(0, 10):
        # payload = ''.join([random.choice(string.ascii_letters + string.digits) for nn in range(field_size)])
        payload = ''.join([random.choice(string.ascii_letters) for nn in range(field_size)])
        payloads.append(payload)

    req_sender = ClientSender(hosts)
    read_count = 0
    for times in range(0, total_req_num):
        user_id = random.sample(id_list, 1)[0]
        roller = random.random()
        if roller < read_prob:
            req_sender.get_read_latency_non_block(host=hosts[0], user_id=user_id)
            read_count += 1
        else:
            random.shuffle(payloads)
            req_sender.get_update_latency_non_block(host=hosts[0], user_id=user_id, fields=payloads)
        time.sleep(0.0001)

    while (len(req_sender.read_latencies) < read_count):
        print(read_count, len(req_sender.read_latencies))
        time.sleep(1)

    results = req_sender.read_latencies
    results = np.array(results)
    results = results * 1000
    np.savetxt('cassandra_latency.txt', results, delimiter=',')
    return 0


if __name__ == '__main__':
    print('Cassandra Client Start')
    st_time = time.time()
    sys_main()
    end_time = time.time()
    print('throughput', total_req_num/(end_time - st_time))
