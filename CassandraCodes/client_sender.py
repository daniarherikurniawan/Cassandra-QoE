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

    def get_read_latency_non_block(self, host, user_id):
        if host in self.hosts:
            return self.senders[host].get_read_latency_no_block(self.read_non_nonblock_callback, user_id)

    def read_non_nonblock_callback(self, exe_time):
        self.read_latencies.append(exe_time)
        return exe_time

    def get_update_latency_non_block(self, host, user_id, fields):
        if host in self.hosts:
            return self.senders[host].get_update_latency_no_block(self.update_nonblock_callback, user_id, fields)

    def update_nonblock_callback(self, exe_time):
        self.update_latencies.append(exe_time)
        return exe_time

    def get_scan_latency_non_block(self, host, user_id):
        if host in self.hosts:
            return self.senders[host].get_scan_latency_no_block(self.scan_nonblock_callback, user_id)

    def scan_nonblock_callback(self, exe_time):
        self.scan_latencies.append(exe_time)
        return exe_time

    def get_hosts(self):
        return self.hosts

    def get_senders(self):
        return self.senders

    def clear_latency_table(self):
        self.update_latencies = []
        self.read_latencies = []
        self.scan_latencies = []
        return 0
