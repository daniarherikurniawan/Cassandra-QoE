# Run this on client side (request USING rabbit-mq)

#!/usr/bin/env python
import pika
import random
import string
import sys


payload = PACKETLENGTH  #1000 - 1K; 1000000 - 1M
message_num = MSGNUM

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='TestQueue', durable=False)

string_load =  ''.join([random.choice(string.ascii_letters + string.digits) for nn in range(payload)])

for x in range(0, message_num):
    channel.basic_publish(exchange='', routing_key='TestQueue', body=string_load)
    print('[*] Send Successfully! Message', str(x))

connection.close()

