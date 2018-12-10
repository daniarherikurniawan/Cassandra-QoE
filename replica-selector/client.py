import xmlrpc.client
from cassandra.cluster import Cluster
import uuid
import subprocess
from faker import Faker
from random import randint

fake = Faker()

# p = subprocess.Popen("scripts/getIP.sh", stdout=subprocess.PIPE, shell=True)
# (IP, status) = p.communicate()
IP=['155.98.38.66','155.98.38.70','155.98.38.57']
IPSelector='155.98.38.59'


clusters = [Cluster([str(IP[0])]), Cluster([str(IP[1])]), Cluster([str(IP[3])])]
sessions = [clusters[0].connect(), clusters[1].connect(), clusters[2].connect()]
proxy 	= 	xmlrpc.client.ServerProxy("http://"+str(IPSelector)+":8000/")


sessions[0].execute('USE CassDB')

rows = sessions[0].execute('SELECT name, address, phone FROM users')
for user_row in rows:
    print user_row.name, user_row.address, user_row.phone

sessions[0].execute(
    """
    INSERT INTO users (id, name, address, salary, phone)
    VALUES (%s, %s, %s, %s, %s)
    """,
    (uuid.uuid1(), fake.name(), fake.address(), randint(4000, 1000000), '765874678')
)


def sendRequest(latency):
	replicaAddress = proxy.getReplicaServer(latency)


print(str(proxy.getReplicaServer(1800)))



print(str(proxy.getReplicaServer(1000)))
print(str(proxy.getReplicaServer(7800)))
print(str(proxy.getQueue()))
print(str(proxy.reduceQueue(1)))
print(str(proxy.getQueue()))
