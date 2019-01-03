# Run this on client side (request USING rabbit-mq)
#!/usr/bin/env python
import pika
import random
import string
import sys
import time


# Step #3
def on_open(connection):
    connection.channel(on_open_callback=on_channel_open)

# Step #4
def on_channel_open(channel):

    global message_num
    global string_load
    random.seed(time.time())

    max_priority_num = 250
    c_properties = dict()
    c_properties['x-max-priority'] = max_priority_num
    c_properties['x-message-ttl'] = 10000000

    # channel.exchange_declare(exchange='logs',
    #                          exchange_type='direct')

    channel.queue_declare(callback = on_queue_declareok, queue='TestQueue', durable=True, exclusive=False, auto_delete=True,
                                   arguments=c_properties)
    # channel.queue_bind(exchange='logs',
    #                    queue='TestQueue')
    #channel.confirm_delivery()
    for x in range(0, message_num):
        r_num = random.random()
        if r_num < 0.5:
            channel.basic_publish(exchange='', routing_key='TestQueue', body=str(1) + ' ' + string_load,
                                  properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2,
                                                                  priority=1))
        else:
            channel.basic_publish(exchange='', routing_key='TestQueue', body=str(0) + ' ' + string_load,
                                  properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2,
                                                                  priority=0))
    print('Send Successfully!')


def on_queue_declareok(method_frame):
    """Method invoked by pika when the Queue.Declare RPC call made in
    setup_queue has completed. In this method we will bind the queue
    and exchange together with the routing key by issuing the Queue.Bind
    RPC command. When this command is complete, the on_bindok method will
    be invoked by pika.

    :param pika.frame.Method method_frame: The Queue.DeclareOk frame

    """
    print('Queue is OK')



# Step #1: Connect to RabbitMQ
payload = PACKETLENGTH  #1000 - 1K; 1000000 - 1M
message_num = MSGNUM


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
