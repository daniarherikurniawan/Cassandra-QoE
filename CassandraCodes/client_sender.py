import random
import time
import sender as sd

class ClientSender:

    def __init__(self, hosts):
        self.senders = {}
        self.update_latencies = []
        self.scan_latencies = []
        self.read_latencies = []
        self.hosts = hosts
        for host in hosts:
            self.senders[host] = sd.Sender(host)

    def get_read_latency_non_block(self, host):
        if host in self.hosts:
            return self.senders[host].getReadLatencyNonBlock(self.read_nonBlockCallback)

    def read_nonBlockCallback(self, exe_time):
        self.latencies.append(exe_time)

    def getHosts(self):
        return self.hosts

    def getSenders(self):
        return self.senders

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