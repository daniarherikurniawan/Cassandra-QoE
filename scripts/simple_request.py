from cassandra.cluster import Cluster
from  cassandra.policies import HostFilterPolicy
from  cassandra.policies import RoundRobinPolicy
import time
import numpy as np
import random

#cluster = Cluster(['hsgucare@cass-1.Cassandra-5nodes.ucare.emulab.net'])
primary_host = ['127.0.0.1']
def is_address_accepted(host):
	return host.address in primary_host

filter_policy = HostFilterPolicy(
    child_policy=RoundRobinPolicy(),
    predicate=is_address_accepted
)

cluster = Cluster(
    primary_host,
    load_balancing_policy=filter_policy,
)

session = cluster.connect()
session.set_keyspace('cassdb')
session.execute('use cassdb')

ids = [
	'0a8a0072-fc0d-11e8-9b56-4a0006dd1f80',
	'a519e37e-fc0c-11e8-9b56-4a0006dd1f80',
	'39a0b586-fc0d-11e8-9b56-4a0006dd1f80',
	'534b0608-fc0d-11e8-9b56-4a0006dd1f80',
	'3d2a72e6-fc0d-11e8-9b56-4a0006dd1f80',
	'b30c872a-fc0c-11e8-9b56-4a0006dd1f80',
	'c9255c30-fc0c-11e8-9b56-4a0006dd1f80',
	'bf108d96-fc0c-11e8-9b56-4a0006dd1f80',
	'22cdd668-fc0d-11e8-9b56-4a0006dd1f80',
	'1f736974-fc0d-11e8-9b56-4a0006dd1f80',
	'5699b2c8-fc0d-11e8-9b56-4a0006dd1f80',
	'52bd975a-fc0d-11e8-9b56-4a0006dd1f80',
	'cdc66388-fc0c-11e8-9b56-4a0006dd1f80',
	'c44a7bbe-fc0c-11e8-9b56-4a0006dd1f80',
	'29a03e36-fc0d-11e8-9b56-4a0006dd1f80',
	'38008a26-fc0d-11e8-9b56-4a0006dd1f80',
	'1f523394-fc0d-11e8-9b56-4a0006dd1f80',
	'0c5c6dcc-fc0d-11e8-9b56-4a0006dd1f80',
	'36cf478c-fc0d-11e8-9b56-4a0006dd1f80',
	'db51eacc-fc0c-11e8-9b56-4a0006dd1f80',
	'a9bff800-fc0c-11e8-9b56-4a0006dd1f80',
	'563f9180-fc0d-11e8-9b56-4a0006dd1f80',
	'15dc3166-fc0d-11e8-9b56-4a0006dd1f80',
	'38e39ec4-fc0d-11e8-9b56-4a0006dd1f80',
	'07d239ee-fc0d-11e8-9b56-4a0006dd1f80',
	'ecef5e9a-fc0c-11e8-9b56-4a0006dd1f80',
	'c27d4f28-fc0c-11e8-9b56-4a0006dd1f80',
	'af102e74-fc0c-11e8-9b56-4a0006dd1f80',
	'526f74b2-fc0d-11e8-9b56-4a0006dd1f80'
]

def execute(command):
    return session.execute_async(command)

def sendReadRequest(user_id):
	command = 'select * from users where id=' + user_id
	return execute(command)

def getLatency(query_result):
	start_time = time.time()
	request_finish = False
	time_elapsed = 0
	while not request_finish: 
		if query_result.has_more_pages:
			query_result.start_fetching_next_page()
		else:
			request_finish = True
			time_elapsed = time.time() - start_time
	return time_elapsed

def sendMultipleRequest(num_request, sleep_time):
	num_requested = 0
	latency = []
	while num_requested < num_request:
		id = random.sample(ids, 3)[1]
		query_result = sendReadRequest(id)
		time_elapsed = getLatency(query_result)
		latency.append(time_elapsed)
		time.sleep(sleep_time)
		num_requested = num_requested + 1
	#np.savetxt('latency.txt', time_elapsed)

### Main function
sendMultipleRequest(1000, 0.01)
