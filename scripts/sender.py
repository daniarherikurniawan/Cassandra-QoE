from cassandra.cluster import Cluster
from  cassandra.policies import HostFilterPolicy
from  cassandra.policies import RoundRobinPolicy
import random
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


class ClientSender:

    def __init__(self, hosts):
        self.senders = {}
        self.hosts = hosts
        for host in hosts:
            self.senders[host] = Sender(host)


    def sendReadRequest(self, host):
        self.senders[host].sendReadRequest()


    def getReadLatency(self, host):
        self.senders[host].getReadLatency()


    def sendMultipleReadRequest(self, num_request, interval, next_policy = None):
        next_host =  next_policy if next_policy != None else self.defaultNextPolicy
        latencies = []
        num_requested = 0
        while num_requested < num_request:
            host = next_host()
            latency = self.getReadLatency(host)
            time.sleep(interval)
            latencies.append(latency)
            num_requested = num_requested + 1
        return latencies


    def defaultNextPolicy(self):
        return random.sample(self.hosts, 1)[0]