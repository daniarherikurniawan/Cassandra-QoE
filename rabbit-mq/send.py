#!/usr/bin/env python
import pika
from random import randint

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='CassandraQueue')

for x in xrange(1,500):
	latency=randint(200, 10000)
	channel.basic_publish(exchange='', routing_key='CassandraQueue', body=str(latency))
	print("[*] Sent request with latency "+str(latency))

connection.close()

