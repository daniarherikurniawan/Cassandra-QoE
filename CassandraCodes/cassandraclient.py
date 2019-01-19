import xmlrpc.client
# for python 2.7 import xmlrpclib
from cassandra.cluster import Cluster
import uuid
import subprocess
from faker import Faker

import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import timedelta
from datetime import datetime
import time
import math
import string
import random

fake = Faker()

IP = ['cass-1.CassandraTest.DeepEdgeVideo.emulab.net', 'cass-2.CassandraTest.DeepEdgeVideo.emulab.net', 'cass-3.CassandraTest.DeepEdgeVideo.emulab.net']
clusters = [Cluster([str(IP[0])]), Cluster([str(IP[1])]), Cluster([str(IP[2])])]
sessions = [clusters[0].connect(), clusters[1].connect(), clusters[2].connect()]

'''
For debug, just use only 1 replica
'''
clusters = [Cluster([str(IP[0])])]
sessions = [clusters[0].connect()]
'''
For debug, just use only 1 replica
'''

id_list = []

row_size = 5000 # unit: Byte
field_size = int(row_size / 10)
payloads = []


bk_delays = []

class PagedResultHandler(object):

    def __init__(self, future, replica_addr, start_time, op_type):
        self._replica_addr = replica_addr
        self._future = future
        self._start_time = start_time
        self._op_type = op_type
        self._future.add_callbacks(
            callback=self.handle_page,
            errback=self.handle_error)

    def handle_page(self, rows):

        if self._future.has_more_pages:
            self._future.start_fetching_next_page()
        else:
            latency = time.time()-self._start_time
            if self._op_type == 'SCAN':
                global bk_delays
                bk_delays.append(latency)

    def handle_error(self, exc):

        self.error = exc
        self.finished_event.set()


def sendUpdateRequest(key, replica_addr):
    orders = list(range(0, 10))
    random.shuffle(orders)
    start_time = time.time()
    future = sessions[replica_addr].execute_async(
        """
        INSERT INTO usertable (y_id, filed0, filed1, filed2, filed3, filed4, filed5, filed6, filed7, filed8, filed9)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (key, payloads[orders[0]], payloads[orders[1]], payloads[orders[2]], payloads[orders[3]], payloads[orders[4]], payloads[orders[5]], payloads[orders[6]], payloads[orders[7]], payloads[orders[8]], payloads[orders[9]])
    )
    handler = PagedResultHandler(future=future, replica_addr=replica_addr, start_time=start_time, op_type='UPDATE')



def get_id_list():

    global id_list
    df = pd.read_csv('y_id.csv')
    id_list = list(df['y_id'])
    return 0

def sys_main():

    random.seed(time.time())
    # Build connection to replicas
    for session in sessions:
        session.execute('USE ycsb')
    get_id_list()
    for i in range(0, 10):
        payload = ''.join([random.choice(string.ascii_letters + string.digits) for nn in range(field_size)])
        payloads.append(payload)

    return 0


if __name__ == '__main__':
    print('Cassandra Client Start')
    sys_main()
