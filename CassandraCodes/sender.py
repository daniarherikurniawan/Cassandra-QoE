from cassandra.cluster import Cluster
from cassandra.policies import HostFilterPolicy
from cassandra.policies import RoundRobinPolicy
import time
import sys
import os


class Sender:

    def __init__(self, host_address):
        self.host_address = host_address
        self.session = self.generate_session()
        self.session.set_keyspace('ycsb')
        self.session.execute('use ycsb')
        self.read_prepare_stmt = self.session.prepare('select * from usertable where y_id=?')
        self.scan_prepare_stmt = self.session.prepare('select * from usertable where y_id>? limit 100')
        self.update_prepare_stmt = self.session.prepare(
            'update usertable set filed0=?, filed1=?, filed2=?, filed3=?, filed4=?, filed5=?, filed6=?, filed7=?, filed8=?, filed9=? where y_id=? if exists')

    def is_address_accepted(self, host):
        return host.address == self.host_address

    def generate_session(self):
        filter_policy = HostFilterPolicy(
            child_policy=RoundRobinPolicy(),
            predicate=self.is_address_accepted()
        )

        cluster = Cluster(
            [self.host_address],
            load_balancing_policy=filter_policy,
        )
        return cluster.connect()

    def get_session(self):
        return self.session

    def get_read_latency_no_block(self, callback, user_id):
        read_stmt = self.read_prepare_stmt.bind((user_id))
        starting_time = time.time()
        future = self.session.execute_async(read_stmt)
        ResultHandler(future, callback, starting_time)

    def get_scan_latency_no_block(self, callback, user_id):
        scan_stmt = self.scan_prepare_stmt.bind((user_id))
        starting_time = time.time()
        future = self.session.execute_async(scan_stmt)
        ResultHandler(future, callback, starting_time)

    def get_update_latency_no_block(self, callback, user_id, fields):
        update_stmt = self.update_prepare_stmt.bind((fields[0], fields[1], fields[2], fields[3], fields[4], fields[5],
                                                     fields[6], fields[7], fields[8], fields[9], user_id))
        starting_time = time.time()
        future = self.session.execute_async(update_stmt)
        ResultHandler(future, callback, starting_time)


class ResultHandler:

    def __init__(self, future, callback, start_time):
        self.callback = callback
        self.future = future
        self.start_time = start_time
        self.future.add_callbacks(callback=self.handle_success, errback=self.handle_error)

    def handle_success(self, rows):

        results = []
        for row in rows:
            results.append(row)
            counter = 0
            for i in range(0, 100):
                counter += 1

        if self.future.has_more_pages:
            self.future.start_fetching_next_page()
        else:
            self.callback(time.time() - self.start_time)

    def handle_error(self, exception):
        pass