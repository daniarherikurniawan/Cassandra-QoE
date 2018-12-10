import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
a = proxy.getReplicaServer(1800)
b = proxy.reduceQueue(1)
c = proxy.getQueue()

print(a)
print(b)
print(c)
