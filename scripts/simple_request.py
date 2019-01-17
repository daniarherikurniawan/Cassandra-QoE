import sender
numRequest = 100;
startTime = time.time()
latencies = senders.sendMultipleReadRequest(numRequest, 0.001)
elapsedTime = time.time() - startTime
print("Elapsed time = " + str(elapsedTime))
print("Troughput = " + str(numRequest / elapsedTime))

