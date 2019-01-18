import random
import time
from sender import Sender


class ClientSender:

    def __init__(self, hosts):
        self.senders = {}
        self.latencies = []
        self.hosts = hosts
        for host in hosts:
            self.senders[host] = Sender(host)


    def sendReadRequest(self, host):
        if host in self.hosts:
            return self.senders[host].sendReadRequest()


    def getReadLatency(self, host):
        if host in self.hosts:
            return self.senders[host].getReadLatency()


    def getReadLatencyNonBlock(self, host):
        if host in self.hosts:
            return self.senders[host].getReadLatencyNonBlock(self.nonBlockCallback)

    def nonBlockCallback(self, time):
        self.latencies.append(time)

    def getHosts(self):
        return self.hosts


    def getSenders(self):
        return self.senders


    def getLatencies(self):
        return self.latencies


    def sendMultipleReadRequest(self, num_request, interval, next_host_policy = None):
        next_host =  next_host_policy if next_host_policy != None else self.defaultNextPolicy
        self.clearLatencyTable()
        num_requested = 0
        consumed_time = 0
        while num_requested < num_request:
            start_time = time.time()
            host = next_host()
            latency = self.getReadLatency(host)
            self.latencies.append(latency)
            num_requested = num_requested + 1
            consumed_time = consumed_time + time.time() - start_time
            time.sleep(interval)
        return self.latencies, consumed_time


    def sendMultipleReadRequestNonBlock(self, num_request, interval, next_host_policy = None):
        next_host =  next_host_policy if next_host_policy != None else self.defaultNextPolicy
        self.clearLatencyTable()
        num_requested = 0
        consumed_time = 0
        while num_requested < num_request:
            start_time = time.time()
            host = next_host()
            latency = self.getReadLatencyNonBlock(host)
            num_requested = num_requested + 1
            consumed_time = consumed_time + time.time() - start_time
            time.sleep(interval)

        start_time = time.time()
        while len(self.latencies) < num_request:
            time.sleep(0.00001)
        consumed_time = consumed_time + time.time() - start_time
        return self.latencies, consumed_time


    def defaultNextPolicy(self):
        return random.sample(self.hosts, 1)[0]


    def clearLatencyTable(self):
        self.latencies = []

    def shutdown(self):
        for host in self.hosts:
            self.senders[host].shutdown()
