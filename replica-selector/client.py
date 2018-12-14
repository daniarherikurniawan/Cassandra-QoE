# Run this on client side (request WITHOUT using rabbit-mq)
# for python 3
import xmlrpc.client
# for python 2.7
# import xmlrpclib
from cassandra.cluster import Cluster
import uuid
import subprocess
from faker import Faker
from random import randint

import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import timedelta
from datetime import datetime
import time
import math

fake = Faker()

IP=['cass-1.cassandra-qoe.cs331-uc.emulab.net',
    'cass-2.cassandra-qoe.cs331-uc.emulab.net',
    'cass-3.cassandra-qoe.cs331-uc.emulab.net']
IPSelector='selector.cassandra-qoe.cs331-uc.emulab.net'


clusters = [Cluster([str(IP[0])]), Cluster([str(IP[1])]), Cluster([str(IP[2])])]
sessions = [clusters[0].connect(), clusters[1].connect(), clusters[2].connect()]
proxy   =   xmlrpc.client.ServerProxy("http://"+str(IPSelector)+":8000/")

backend_latency_list = []

for session in sessions:
    session.execute('USE CassDB')

df = pd.DataFrame()
for x in range(1,2):
    print('reading: data-users-'+str(x)+'.csv')
    temp = pd.read_csv('data-users-'+str(x)+'.csv',sep='|')
    temp = temp[['id']]
    df = pd.concat([df,temp]).reset_index(drop=True)

def sendBatchRequestPerSeconds(req_number, usingSelector):
    # if(req_number<10):
    #     req_number = 10
    # samples = df.sample((req_number-math.ceil(req_number/10)), replace=True)
    samples = df.sample(req_number, replace=True)
    start = time.time()
    x=0
    for index, row in samples.iterrows():
        latency=200
        # latency=randint(400, 100000)
        sendReadRequest(latency, usingSelector, row['id'])
        # 10% of the request is writing
        # if (x%9==0):
        # there are 100 writting requests
        if ((req_number>=100) & (x%math.ceil(req_number*0.1)==0)):
            sendWriteRequest(latency, usingSelector)
        x=x+1
    print(x)
    return start, x


# Notes: Sending a single request to pc3000 took 0.25 ms 
def sendRequestPerSeconds(req_number, usingSelector, loop_number, sleep_time):
    latency_per_req = 0.25
    max_request = 1000/latency_per_req #4000
    total_sleep_time = (max_request - req_number)*latency_per_req
    # avg_sleep_time = total_sleep_time/1000/req_number
    samples = df.sample(req_number, replace=True)
    start = time.time()
    x=0
    latency=200
    mod=math.ceil(req_number*0.1)
    for index, row in samples.iterrows():
        sendReadRequest(latency, usingSelector, row['id'])
        # 10% of the request is writing
        # if (x%9==0):
        # there are 100 writting requests
        if ((x%mod==0)):
            sendWriteRequest(latency, usingSelector)
        x=x+1
        time.sleep(sleep_time)
        y=0
        while (y < loop_number):
            t=math.ceil(99999.2/43434)/00.4353
            t=math.ceil(85932.42/4242.5)/32321.4353
            t=math.ceil(9999.9/43.434)/34.4353
            y=y*1+1
        # if(x%10 == 0):
        #     time.sleep(avg_sleep_time)
    print(x)
    return start, x

def sendRequest(latency):
    start_time=time.time()
    # replicaAddress = proxy.getReplicaServer(latency)
    replicaAddress=0
    # print("send data to server - "+str(replicaAddress))
    future = sessions[replicaAddress].execute_async("SELECT * FROM users LIMIT 1000")
    handler = PagedResultHandler(future, replicaAddress, latency, start_time)

def sendWriteRequest(latency,usingSelector):
    start_time=time.time()
    replicaAddress=0
    if(usingSelector):
        replicaAddress = proxy.getReplicaServer(latency)
    future = sessions[replicaAddress].execute_async(
        """
        INSERT INTO users (id, name, address, salary, phone)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (uuid.uuid1(), "Any Name", "Any Address", "4000", "3214566352")
    )
    handler = PagedResultHandler(future, replicaAddress, latency, start_time)

def sendReadRequest(latency,usingSelector, uuid):
    start_time=time.time()
    replicaAddress=0
    if(usingSelector):
        replicaAddress = proxy.getReplicaServer(latency)
    # print(str(replicaAddress))
    future = sessions[replicaAddress].execute_async("SELECT * FROM users WHERE id="+uuid)
    handler = PagedResultHandler(future, replicaAddress, latency, start_time)

class PagedResultHandler(object):
    def __init__(self, future, replicaAddress, latency, start_time):
        self.replicaAddress = replicaAddress
        self.latency = latency
        self.future = future
        self.start_time = start_time
        self.future.add_callbacks(
            callback=self.handle_page,
            errback=self.handle_error)
    def handle_page(self, rows):
        if self.future.has_more_pages:
            self.future.start_fetching_next_page()
        else:
            latency=time.time()-self.start_time
            backend_latency_list.append(latency)
    def handle_error(self, exc):
        self.error = exc
        self.finished_event.set()

def info(backend_latency_list, start, req_number):
    exec_time = (time.time()-start)
    print('=== '+str(math.ceil(req_number/exec_time))+' RPS')
    print('finish sending '+str(req_number)+' async request in '+ str(exec_time)+' s')
    while(True):
        if(len(backend_latency_list) < req_number):
            print('waiting '+str(math.ceil(len(backend_latency_list)/req_number*100))+'% ..')
            time.sleep(0.8)
        else:
            batch_time=(time.time()-start)*1000
            backend_latency_arr = np.array(backend_latency_list)
            median=np.percentile(backend_latency_arr, 50)*1000
            total = np.sum(backend_latency_list)*1000
            nine=np.percentile(backend_latency_arr, 99.99)*1000
            print("median "+str(median)+ " ms")
            print("1th "+str(np.percentile(backend_latency_arr, 1)*1000)+ " ms")
            print("99th "+str(np.percentile(backend_latency_arr, 99)*1000)+ " ms")
            print("99.99th "+str(nine)+ " ms")
            print("total "+str(total)+ " ms")
            print("batch exec "+str(batch_time)+ " ms")
            median_array.append(median)
            nine_array.append(nine)
            batch_array.append(batch_time)
            total_array.append(total)
            if (exec_time>1):
                return True
            else:
                return False

median_array = []
nine_array = []
total_array = []
batch_array = []
multiply = 1000
usingSelector = False
sleep_time = 0.0001 
loop_number = 0.0001 
# 1000-25000
# usingSelector = True
for x in range(1,2):
    time.sleep(1)
    backend_latency_list=[]
    req_number = multiply*x
    start, x = sendRequestPerSeconds(req_number, usingSelector, loop_number, sleep_time)
    stop = info(backend_latency_list, start, x)
    # if(stop):
        # break

tes = pd.DataFrame({'median':median_array})
tes['nine'] = nine_array
tes['total'] = total_array
tes['batch'] = batch_array
tes['rps'] = (tes.index+2)*multiply
tes.to_csv('selector_true_big')
tes.to_csv('selector_false_big')

scp daniar@pc444.emulab.net:/tmp/Cassandra-QoE/dataset/selector_true_big ~/Documents/Project/Cassandra-QoE/dataset/
scp daniar@pc444.emulab.net:/tmp/Cassandra-QoE/dataset/selector_false_big ~/Documents/Project/Cassandra-QoE/dataset/



import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import timedelta
from datetime import datetime
import time
import math

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


# tes_t = pd.read_csv('selector_true_big')
tes_f = pd.read_csv('selector_false_big')

ax = plt.subplot(111)

# ax.plot(tes_t['rps'], tes_t['nine'], "r-", label="99th-percentile", linestyle='dashed')
# ax.plot(tes_t['rps'], tes_t['median'], "g-", label="Median", linestyle='dashed')
# # ax.plot(tes_t['rps'], tes_t['total'], "b-", label="Total ", linestyle='dashed')
# ax.plot(tes_t['rps'], tes_t['batch'], "b-", label="Elapsed time per rps ", linestyle='dashed')

ax.plot(tes_f['rps'], tes_f['nine'], "r-", label="99th-percentile")
ax.plot(tes_f['rps'], tes_f['median'], "g-", label="Median")
# ax.plot(tes_f['rps'], tes_f['total'], "b-", label="Total ")
ax.plot(tes_f['rps'], tes_f['batch'], "b-", label="Elapsed time per rps ")

plt.title("Using Replica Selector (Dashed Line) and Without Replica Selector (Continous Line)")
# plt.title("Request Using Replica Selector ")
# plt.title("Request Without Replica Selector ")
# plt.xlabel('RPS')
plt.xlabel('# request')
plt.ylabel('Latency (ms)')
plt.legend()
plt.show()




