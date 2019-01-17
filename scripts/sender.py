from cassandra.cluster import Cluster
from  cassandra.policies import HostFilterPolicy
from  cassandra.policies import RoundRobinPolicy
import random_id
import time

class Sender:

    def __init__(self, host_address):
        self.host_address = host_address
        self.session = self.generateSession()
        self.session.set_keyspace('cassdb')
        self.session.execute('use cassdb')
        self.read_prepare_stmt = self.session.prepare('select * from users where id=?')


    def isAddressAccepted(self, host):
        return host.address == self.host_address


    def generateSession(self):
        filter_policy = HostFilterPolicy(
            child_policy=RoundRobinPolicy(),
            predicate=self.isAddressAccepted
        )

        cluster = Cluster(
            [self.host_address],
            load_balancing_policy = filter_policy,
        )
        return cluster.connect()


    def getSession(self):
        return self.session


    def sendReadRequest(self):
        user_id = random_id.getRandomId()
        return self.session.execute_async('select * from users where id=' + user_id)


    def getReadLatency(self):
        future = self.sendReadRequest()
        start_time = time.time()
        row = future.result()[0];
        return time.time() - start_time

