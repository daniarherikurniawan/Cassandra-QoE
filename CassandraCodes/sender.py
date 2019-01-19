from cassandra.cluster import Cluster
from cassandra.policies import HostFilterPolicy
from cassandra.policies import RoundRobinPolicy
import time
import sys
import os

class Sender:

    def __init__(self, host_address):
        self.host_address = host_address
        self.session = self.generateSession()
        self.session.set_keyspace('ycsb')
        self.session.execute('use ycsb')
        self.read_prepare_stmt = self.session.prepare('select * from usertable where y_id=?')
        self.scan_prepare_stmt = self.session.prepare('select * from usertable where y_id>? limit 100')
        self.update_prepare_stmt = self.session.prepare('update usertable set filed0=?, filed1=?, filed2=?, filed3=?, filed4=?, filed5=?, filed6=?, filed7=?, filed8=?, filed9=? where y_id=? if exists')

    def isAddressAccepted(self, host):
        return host.address == self.host_address

    def generateSession(self):
        filter_policy = HostFilterPolicy(
            child_policy=RoundRobinPolicy(),
            predicate=self.isAddressAccepted
        )

        cluster = Cluster(
            [self.host_address],
            load_balancing_policy=filter_policy,
        )
        return cluster.connect()

    def getSession(self):
        return self.session

    def sendReadRequest(self, user_id):
        return self.session.execute_async('select * from users where id=' + user_id)

    def getReadLatencyNonBlock(self, callback):
        future = self.session.execute_async('select * from users where id=' + user_id)
        ResultHandler(future, callback, time.time())

    def getReadLatency(self):
        start_time = time.time()
        future = self.sendReadRequest()
        row = future.result()[0]
        return time.time() - start_time


class ResultHandler:

    def __init__(self, future, callback, start_time):
        self.callback = callback
        self.future = future
        self.start_time = start_time
        self.future.add_callbacks(callback=self.handle_success, errback=self.handle_error)

    def read_from_rows(self, rows):
        for row in rows:
            counter = 0
            for i in range(0, 100):
                counter += 1
        return 0

    def handle_success(self, rows):

        self.read_from_rows(rows=rows)
        if self.future.has_more_pages:
            self.future.start_fetching_next_page()
        else:
            self.callback(time.time() - self.start_time)

    def handle_error(self, exception):
        pass