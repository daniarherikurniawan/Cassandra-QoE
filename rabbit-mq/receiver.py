# Run this on client side (request USING rabbit-mq)
#!/usr/bin/env python

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.2'))
channel = connection.channel()

channel.queue_declare(queue='TestQueue', durable=False)

counter = 0
start_time = 0.0

def callback(ch, method, properties, body):

    global counter
    global start_time
    if counter == 0:
        start_time = time.time()
    counter += 1
    now_time = time.time()
    if now_time - start_time > 1.00:
        print('Throughput: ', counter)
        counter = 0
    print('[*] Received Message', counter)


channel.basic_consume(callback,
                      queue='TestQueue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
