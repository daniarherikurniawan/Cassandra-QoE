# Run this on client side (request USING rabbit-mq)
#!/usr/bin/env python
import pika
import random
import string
import sys
import time
import asyncio


# Step #3
def on_open(connection):
    connection.channel(on_open_callback=on_channel_open)

# Step #4
def on_channel_open(channel):

    global message_num
    global string_load
    global dis_lambda
    global threshold
    global g_channel

    g_channel = channel

    random.seed(time.time())

    max_priority_num = 250
    c_properties = dict()
    c_properties['x-max-priority'] = max_priority_num
    g_channel.queue_declare(callback = on_queue_declareok, queue='TestQueue', durable=True, exclusive=False, auto_delete=True, arguments=c_properties)



def on_queue_declareok(method_frame):

    g_channel.confirm_delivery()
    print('Queue is OK')
    for x in range(0, message_num):
        random_num = random.random()
        if random_num <= threshold:
            g_channel.basic_publish(exchange='', routing_key='TestQueue', body=str(0) + ' ' + string_load,
                                  properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2,
                                                                  priority=0))
        else:
            g_channel.basic_publish(exchange='', routing_key='TestQueue', body=str(1) + ' ' + string_load,
                                  properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2,
                                                                  priority=1))
        print('[*] Send Successfully! Msg Num:', str(x))
        sleep_time = random.expovariate(dis_lambda)
        time.sleep(sleep_time)



# Step #1: Connect to RabbitMQ

payload = PACKETLENGTH  #Unit: Byte
message_num = MSGNUM
dis_lambda = THROUGHPUT
threshold = PROBABILITY

g_channel = None

print('Pre-setting starts')
string_load = ''.join([random.choice(string.ascii_letters + string.digits) for nn in range(payload)])
print('Payload is Ready')

connection = pika.SelectConnection(parameters = pika.ConnectionParameters('localhost'), on_open_callback=on_open)


try:
    # Step #2 - Block on the IOLoop
    connection.ioloop.start()
# Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Start the IOLoop again so Pika can communicate, it will stop on its own when the connection is closed
    connection.ioloop.start()
