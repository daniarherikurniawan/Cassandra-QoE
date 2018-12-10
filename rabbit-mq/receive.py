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

def sendRequest(latency):
	replicaAddress = proxy.getReplicaServer(latency)
	print("send data to server : "+str(replicaAddress))
	future = sessions[replicaAddress].execute_async("SELECT * FROM users WHERE name='Lucas Allen' ALLOW FILTERING")
	handler = PagedResultHandler(future, replicaAddress, latency)
	print('finish sending async request')


class PagedResultHandler(object):
    def __init__(self, future, replicaAddress, latency):
        self.error = None
        self.replicaAddress = replicaAddress
        self.latency = latency
        # self.finished_event = show()
        self.future = future
        self.future.add_callbacks(
            callback=self.handle_page,
            errback=self.handle_error)
    def handle_page(self, rows):
        if self.future.has_more_pages:
            self.future.start_fetching_next_page()
        else:
        	print('Result from node '+str(self.replicaAddress)+
        		' (non-backend latency: '+str(self.latency)+' ms)')
        	proxy.reduceQueue(self.replicaAddress)
        	# for user_row in rows:
        	# 	print user_row.name, user_row.address, user_row.phone
            # self.finished_event.set()
    def handle_error(self, exc):
        self.error = exc
        self.finished_event.set()


def print_row_count(rows, label):
    for i, row in enumerate(rows):
        do_something = row
    print "{}: processed {} rows".format(label, i+1)

def print_err(reason):
    print "Error: {}".format(reason)


# ====================================================
# receiver rabbitmq code

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.queue_declare(queue='CassandraQueue')

def callback(ch, method, properties, body):
    print(" [x] Received request with latency %r" % body)
    sendRequest(int(body))
    print(" [x] Request sent to replica selector")


channel.basic_consume(callback,
                      queue='CassandraQueue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
