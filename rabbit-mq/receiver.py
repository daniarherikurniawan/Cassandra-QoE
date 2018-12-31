# Run this on client side (request USING rabbit-mq)
#!/usr/bin/env python

import pika
import time
import sys

pika_credentials = pika.PlainCredentials('test1', 'test1')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.2', credentials=pika_credentials))
channel = connection.channel()

channel.queue_declare(queue='TestQueue', durable=True, exclusive=False, auto_delete=True)

counter = 0
start_time = 0.0
last_time = 0.0
now_time = 0.0

def callback(ch, method, properties, body):

    global counter
    global start_time
    global last_time
    global now_time
    if counter == 0:
        start_time = time.time()
    counter += 1
    last_time = now_time
    now_time = time.time()
    if now_time - start_time > 1.00:
        print('Throughput:', counter, 'Total Time Consumption:', now_time - start_time)
        counter = 0
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print('[*] Received Message', counter, 'Time Consumption:', now_time-last_time, 'Message Length:', sys.getsizeof(body))

channel.basic_qos(prefetch_count = 1)
channel.basic_consume(callback,
                      queue='TestQueue',
                      no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
