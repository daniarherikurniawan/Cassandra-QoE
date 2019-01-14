#!/usr/bin/env python
import pika
import random
import string
import sys
import time
import math
import numpy as np


class RabbitMQTest(object):
    EXCHANGE = 'logs'
    EXCHANGE_TYPE = 'direct'
    PUBLISH_INTERVAL = 1
    QUEUE = 'TestQueue'
    ROUTING_KEY = 'TestQueue'
    ORI_THROUGHPUT = 87.965737345304
    FILENAME = 'time_invervals.txt'

    def __init__(self, payload, is_fifo, dis_lambda):
        """Setup our publisher object, passing in the URL we will use
        to connect to RabbitMQ.

        :param int payload: message size (in bytes)
        :param int message_num: # messages we need to send out
        :param int dis_lambda: throughput (reqs per second)
        :param int threshold: message size (Byte)
        """
        self._connection = None
        self._channel = None

        self._deliveries = []
        self._acked = None
        self._nacked = None
        self._message_number = None

        self._stopping = False

        self._string_load = ''.join([random.choice(string.ascii_letters + string.digits) for nn in range(payload)])
        self._dislamba = dis_lambda
        self._max_priority = 20

        self._lasttime = 0
        self._currenttime = 0
        self._timeinterval = np.loadtxt('time_invervals.txt')
        self._message_totalnum = 5000
        self._timeinterval = self._timeinterval[0:5000]
        self._timeinterval = self._timeinterval * (87.965737345304/self._dislamba)

        self._is_fifo = is_fifo


    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.
        :rtype: pika.SelectConnection
        """
        return pika.SelectConnection(parameters=pika.ConnectionParameters('localhost'),
                                     on_open_callback=self.on_connection_open,
                                     on_close_callback=self.on_connection_closed,
                                     stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.
        :type unused_connection: pika.SelectConnection
        """
        print('Connection is established!!')
        self.open_channel()

    def on_connection_closed(self, connection, reason, reply_txt):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param Exception reason: exception representing reason for loss of
            connection.

        """
        self._channel = None
        if self._stopping:
            self._connection.ioloop.stop()
        else:
            self._connection.ioloop.add_timeout(5, self._connection.ioloop.stop)

    def open_channel(self):
        """This method will open a new channel with RabbitMQ by issuing the
        Channel.Open RPC command. When RabbitMQ confirms the channel is open
        by sending the Channel.OpenOK RPC reply, the on_channel_open method
        will be invoked.

        """
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the exchange to use.

        :param pika.channel.Channel channel: The channel object

        """
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange(self.EXCHANGE)

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.
        """
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reply_code, reply_txt):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel channel: The closed channel
        :param Exception reason: why the channel was closed

        """
        self._channel = None
        if not self._stopping:
            self._connection.close()

    def setup_exchange(self, exchange_name):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declareok method will
        be invoked by pika.

        :param str|unicode exchange_name: The name of the exchange to declare

        """
        self._channel.exchange_declare(self.on_exchange_declareok, exchange_name, self.EXCHANGE_TYPE)

    def on_exchange_declareok(self, unused_frame):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame

        """
        print('Exchange is established!')
        self.setup_queue(self.QUEUE)

    def setup_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        :param str|unicode queue_name: The name of the queue to declare.

        """
        max_priority_num = 250
        c_properties = dict()
        c_properties['x-max-priority'] = max_priority_num
        c_properties['x-message-ttl'] = 10000000
        c_properties['x-max-length'] = 10000000
        self._channel.queue_declare(queue=queue_name, callback=self.on_queue_declareok, durable=True, exclusive=False,
                                    auto_delete=True, arguments=c_properties)

    def on_queue_declareok(self, method_frame):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method method_frame: The Queue.DeclareOk frame

        """
        print('Queue is established!')
        self._channel.queue_bind(self.on_bindok, self.QUEUE, self.EXCHANGE, self.ROUTING_KEY)

    def on_bindok(self, unused_frame):
        """This method is invoked by pika when it receives the Queue.BindOk
        response from RabbitMQ. Since we know we're now setup and bound, it's
        time to start publishing."""
        self.start_publishing()

    def start_publishing(self):
        """This method will enable delivery confirmations and schedule the
        first message to be sent to RabbitMQ
        """
        print('Start publishing messages!')
        #self.enable_delivery_confirmations()
        self.schedule_next_message()

    def enable_delivery_confirmations(self):
        """Send the Confirm.Select RPC method to RabbitMQ to enable delivery
        confirmations on the channel. The only way to turn this off is to close
        the channel and create a new one.

        When the message is confirmed from RabbitMQ, the
        on_delivery_confirmation method will be invoked passing in a Basic.Ack
        or Basic.Nack method from RabbitMQ that will indicate which messages it
        is confirming or rejecting.

        """
        self._channel.confirm_delivery(self.on_delivery_confirmation)

    def on_delivery_confirmation(self, method_frame):
        """Invoked by pika when RabbitMQ responds to a Basic.Publish RPC
        command, passing in either a Basic.Ack or Basic.Nack frame with
        the delivery tag of the message that was published. The delivery tag
        is an integer counter indicating the message number that was sent
        on the channel via Basic.Publish. Here we're just doing house keeping
        to keep track of stats and remove message numbers that we expect
        a delivery confirmation of from the list used to keep track of messages
        that are pending confirmation.

        :param pika.frame.Method method_frame: Basic.Ack or Basic.Nack frame

        """
        confirmation_type = method_frame.method.NAME.split('.')[1].lower()

        if confirmation_type == 'ack':
            self._acked += 1
        elif confirmation_type == 'nack':
            self._nacked += 1
        #self._deliveries.remove(method_frame.method.delivery_tag)

    def schedule_next_message(self):
        """If we are not closing our connection to RabbitMQ, schedule another
        message to be delivered in PUBLISH_INTERVAL seconds.

        """
        self.publish_message()
        #self._connection.ioloop.add_timeout(self.PUBLISH_INTERVAL, self.publish_message)

    def publish_message(self):
        """If the class is not stopping, publish a message to RabbitMQ,
        appending a list of deliveries with the message number that was sent.
        This list will be used to check for delivery confirmations in the
        on_delivery_confirmations method.

        Once the message has been sent, schedule another message to be sent.
        The main reason I put scheduling in was just so you can get a good idea
        of how the process is flowing by slowing down and speeding up the
        delivery intervals by changing the PUBLISH_INTERVAL constant in the
        class.

        """
        if self._channel is None or not self._channel.is_open:
            return

        # self._currenttime = time.time()
        # print('Real time interval', int(round((self._currenttime - self._lasttime)*1000000)), 'us')
        # self._lasttime = self._currenttime
        r_num = random.random()
        r_priority = int(math.floor(r_num*self._max_priority))

        '''
        For FIFO debug - all 
        '''
        if self._is_fifo == 1:
            r_priority = 0
        '''
        For FIFO debug
        '''
        # message format: current_time + ' ' + priority + ' ' + a long string
        #t_time = time.time()
        message = str(int(round(time.time() * 1000))) + ' ' + str(r_priority) + ' '
        #print('time consumption', (time.time() - t_time)*1000)


        properties = pika.BasicProperties(content_type='text/plain', delivery_mode=1, priority=r_priority)

        self._channel.basic_publish(self.EXCHANGE, self.ROUTING_KEY, message, properties)
        self._message_number += 1
        #self._deliveries.append(self._message_number)

        # print('[*] Messaage', self._message_number, 'sent!')

        if self._message_number < self._message_totalnum:
            #self.PUBLISH_INTERVAL = random.expovariate(self._dislamba)
            self.PUBLISH_INTERVAL = self._timeinterval[self._message_number]/1000.0
            # print('Published Interval Setting:', round(self.PUBLISH_INTERVAL * 1000000), 'us')
            self.PUBLISH_INTERVAL = max(0.0, self.PUBLISH_INTERVAL - 0.0014) # original 0.001
            ####### for debug
            #self.PUBLISH_INTERVAL = 0.0
            ####### for debug
            self.schedule_next_message()
        else:
            print('Mission Complete! Program Exit.')
            self.stop()
            if (self._connection is not None and
                    not self._connection.is_closed):
                # Finish closing
                self._connection.ioloop.start()


    def run(self):

        random.seed(time.time())

        while not self._stopping:
            self._connection = None
            self._acked = 0
            self._nacked = 0
            self._message_number = 0

            try:
                self._connection = self.connect()
                self._connection.ioloop.start()
            except KeyboardInterrupt:
                self.stop()
                if (self._connection is not None and
                        not self._connection.is_closed):
                    # Finish closing
                    self._connection.ioloop.start()

    def stop(self):
        """Stop the example by closing the channel and connection. We
        set a flag here so that we stop scheduling new messages to be
        published. The IOLoop is started because this method is
        invoked by the Try/Catch below when KeyboardInterrupt is caught.
        Starting the IOLoop again will allow the publisher to cleanly
        disconnect from RabbitMQ.
        """

        self._stopping = True
        self.close_channel()
        self.close_connection()

    def close_channel(self):
        """Invoke this command to close the channel with RabbitMQ by sending
        the Channel.Close RPC command.
        """
        if self._channel is not None:
            self._channel.close()

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        if self._connection is not None:
            self._connection.close()


def main(PACKETLENGTH, IS_FIFO, THROUGHPUT):
    '''
    Total priority level = 10
    :param PACKETLENGTH: message size in bytes
    :param MSGNUM: total number of messages needs to send
    :param THROUGHPUT: requests per second, poisson arrival
    :param PRIORITY: priority of tested quests (1 - 10, 10 is the highest)
    :return:
    '''
    payload = PACKETLENGTH
    fifo_or_not = IS_FIFO
    dis_lambda = THROUGHPUT

    our_tester = RabbitMQTest(payload, fifo_or_not, dis_lambda)
    print('Pre-setting is OK')
    our_tester.run()


if __name__ == '__main__':
    sys.setrecursionlimit(1000000)
    payload = int(sys.argv[1])
    is_fifo = int(sys.argv[2])
    dis_lambda = int(sys.argv[3])
    main(PACKETLENGTH=payload, IS_FIFO=is_fifo, THROUGHPUT=dis_lambda)
