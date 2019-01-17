import time
from client_sender import ClientSender


def next_host():
    return hosts[0]


hosts = ['127.0.0.1', '127.0.0.2']
sender = ClientSender(hosts)
numRequest = 1000
interval = 0.000001 #interval in second
startTime = time.time()
latencies, operation_time = sender.sendMultipleReadRequestNonBlock(numRequest, interval, next_host)
elapsedTime = time.time() - startTime

with open('result.txt', 'w') as filehandle:
    filehandle.writelines("%s\n" % latency for latency in latencies)
print("Elapsed time = " + str(elapsedTime))
print("Operation time (excluding sleep interval) = " + str(operation_time))
print("Troughput (sleep interval is counted) = " + str(numRequest / elapsedTime))
print("Troughput (sleep interval is not counted) = " + str(numRequest / operation_time))

