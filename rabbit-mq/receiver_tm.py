# Run this on client side (request USING rabbit-mq)
#!/usr/bin/env python

import pika
import time
import sys

pika_credentials = pika.PlainCredentials('test1', 'test1')

max_priority_num = 250
c_properties  = dict()
c_properties['x-max-priority'] = max_priority_num
c_properties['x-message-ttl'] = 10000000

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.2', credentials=pika_credentials))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='direct')

result = channel.queue_declare(queue='TestQueue', durable=True, exclusive=False, auto_delete=True, arguments = c_properties)
queue_name = result.method.queue
channel.queue_bind(exchange='logs',
                   queue=queue_name)

msg_counter = 0
msg_thres = 5000

def callback(ch, method, properties, body):

    global msg_counter
    global msg_thres
    msg_counter += 1
    msgarray = str(body).split()
    msgarray[0] = msgarray[0].strip('b\'')
    old_time = int(msgarray[0])
    new_time = int(round(time.time()*1000))
    msg_pri = int(msgarray[1])
    print(msg_pri, new_time - old_time)
    #print('[*] Received Message.', 'Time consumption:',  new_time - old_time, 'ms.', 'Msg priority:', msg_pri)
    if msg_counter >= msg_thres:
        exit()
    #ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count = 1)
channel.basic_consume(callback,
                      queue='TestQueue',
                      no_ack=True)

# print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
