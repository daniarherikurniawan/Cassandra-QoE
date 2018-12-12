# Run this on client side (request USING rabbit-mq)

#!/usr/bin/env python
# ====================================================
# client code
import xmlrpclib
from cassandra.cluster import Cluster
import uuid
import subprocess
from faker import Faker
from random import randint

fake = Faker()

IP=['cass-1.cassandra-qoe.cs331-uc.emulab.net',
	'cass-2.cassandra-qoe.cs331-uc.emulab.net',
	'cass-3.cassandra-qoe.cs331-uc.emulab.net']
IPSelector='selector.cassandra-qoe.cs331-uc.emulab.net'


clusters = [Cluster([str(IP[0])]), Cluster([str(IP[1])]), Cluster([str(IP[2])])]
sessions = [clusters[0].connect(), clusters[1].connect(), clusters[2].connect()]
proxy 	= 	xmlrpclib.ServerProxy("http://"+str(IPSelector)+":8000/")

for session in sessions:
	session.execute('USE CassDB')

def show():
	rows = sessions[0].execute('SELECT name, address, phone FROM users')
	for user_row in rows:
	    print user_row.name, user_row.address, user_row.phone

def sendTestRequest(latency):
	replicaAddress = proxy.getReplicaServer(latency)
	print("send data to server - "+str(replicaAddress))
	sessions[replicaAddress].execute(
	    """
	    INSERT INTO users (id, name, address, salary, phone)
	    VALUES (%s, %s, %s, %s, %s)
	    """,
	    (uuid.uuid1(), fake.name(), fake.address().replace('\n',', '), randint(4000, 100000), str(randint(1000000, 9000000)))
	)
# read and write
def sendRequest(latency):
	replicaAddress = proxy.getReplicaServer(latency)
	future = sessions[replicaAddress].execute_async(
	    """
	    INSERT INTO users (id, name, address, salary, phone)
	    VALUES (%s, %s, %s, %s, %s)
	    """,
	    (uuid.uuid1(), fake.name(), fake.address().replace('\n',', '), randint(4000, 100000), str(randint(1000000, 9000000)))
	)
	# future = sessions[replicaAddress].execute_async("SELECT * FROM users")
	future.add_callbacks(log_results, log_error)

def log_results(results):
	print('Got the result')
    # for row in results:
    #     log.info("Results: %s", row)

def log_error(exc):
    log.error("Operation failed: %s", exc)

# ====================================================
# receiver rabbitmq code

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='CassandraQueue')

def callback(ch, method, properties, body):
    sendRequest(int(body))
    print("[*] Request with latency "+ body+" ms is sent to replica selector")


channel.basic_consume(callback,
                      queue='CassandraQueue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
