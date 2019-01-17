import time
from client_sender import ClientSender

sender = ClientSender(['127.0.0.1'])
numRequest = 1000;
interval = 0.001; #interval in second
startTime = time.time()
latencies = sender.sendMultipleReadRequest(numRequest, interval)
elapsedTime = time.time() - startTime

with open('result.txt', 'w') as filehandle:
    filehandle.writelines("%s\n" % latency for latency in latencies)
print("Elapsed time = " + str(elapsedTime))
print("Troughput = " + str(numRequest / elapsedTime))

