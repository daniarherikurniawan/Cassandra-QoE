from cassandra.cluster import Cluster
import uuid
import subprocess
from faker import Faker
from random import randint

fake = Faker()

p = subprocess.Popen("scripts/getIP.sh", stdout=subprocess.PIPE, shell=True)
(IP, status) = p.communicate()
IP=IP.replace('\n','')
cluster = Cluster([str(IP)])
session = cluster.connect()
session.execute('USE CassDB')

rows = session.execute('SELECT name, address, phone FROM users')
for user_row in rows:
    print user_row.name, user_row.address, user_row.phone

session.execute(
    """
    INSERT INTO users (id, name, address, salary, phone)
    VALUES (%s, %s, %s, %s, %s)
    """,
    (uuid.uuid1(), fake.name(), fake.address(), randint(4000, 1000000), '765874678')
)

