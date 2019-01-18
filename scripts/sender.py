from cassandra import ProtocolVersion
from cassandra.cluster import Cluster
from  cassandra.policies import (HostFilterPolicy, RoundRobinPolicy, HostDistance)
import random_id
import time


class Sender:

    def __init__(self, host_address):
        self.host_address = host_address
        self.cluster = self.generateCluster()
        self.session = self.cluster.connect()
        self.session.set_keyspace('cassdb')
        self.session.execute('use cassdb')


    def isAddressAccepted(self, host):
        return host.address == self.host_address


    def generateCluster(self):
        filter_policy = HostFilterPolicy(
            child_policy=RoundRobinPolicy(),
            predicate=self.isAddressAccepted
        )

        cluster = Cluster(
            [self.host_address],
            load_balancing_policy = filter_policy,
            protocol_version=ProtocolVersion.V3
        )
        # cluster.set_max_requests_per_connection(HostDistance.LOCAL, 10)
        # cluster.set_core_connections_per_host(HostDistance.LOCAL, 2)
        return cluster


    def getSession(self):
        return self.session


    def sendReadRequest(self):
        user_id = random_id.getRandomId()
        return self.session.execute('select * from users where id=' + user_id)


    def getReadLatencyNonBlock(self, callback):
        user_id = random_id.getRandomId()
        future = self.session.execute_async('select * from users where id=' + user_id)
        ResultHandler(future, callback, time.time())


    def getReadLatency(self):
        start_time = time.time()
        row = self.sendReadRequest()
        return time.time() - start_time


    def shutdown(self):
        self.cluster.shutdown()


class ResultHandler:

    def __init__(self, future, callback, start_time):
        self.callback = callback
        self.future = future
        self.start_time = start_time
        self.future.add_callbacks(callback=self.handle_success, errback=self.handle_error)


    def handle_success(self, rows):
        self.callback(time.time() - self.start_time)


    def handle_error(self, exception):
        log.error("Failed to fetch user info")
