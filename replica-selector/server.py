# pip install freeport
# from xmlrpc.server import SimpleXMLRPCServer
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import subprocess

list_servers = [['155.98.38.66',0],['155.98.38.70',0], ['155.98.38.57',0]]

def getReplicaServer(latency):
	global list_servers
	if (latency < 1500):
		# group A
		list_servers[0][1] = list_servers[0][1]+1
		return list_servers[0][0]
	elif (latency > 5000):
		# group C
		list_servers[2][1] = list_servers[2][1]+1
		return list_servers[2][0]
	else:
		# group B
		list_servers[1][1] = list_servers[1][1]+1
		return list_servers[1][0]

def reduceQueue(id):
	global list_servers
	list_servers[id][1] = list_servers[id][1] - 1 
	return True

def getQueue():
	global list_servers
	return list_servers


p = subprocess.Popen("/tmp/Cassandra-QoE/scripts/getIP.sh", stdout=subprocess.PIPE, shell=True)
(IP, status) = p.communicate()
IP=IP.replace('\n','')
server = SimpleXMLRPCServer((str(IP), 8000))
server = SimpleXMLRPCServer((str(IP), 8000))
print("Listening on port 8000...")
server.register_function(getReplicaServer, 'getReplicaServer')
server.register_function(reduceQueue, 'reduceQueue')
server.register_function(getQueue, 'getQueue')
server.serve_forever()

