from cassandra.cluster import Cluster

import subprocess
 
p = subprocess.Popen("scripts/getIP.sh", stdout=subprocess.PIPE, shell=True)
(IP, status) = p.communicate()

cluster = Cluster([str(IP)])

session.execute('USE test')

rows = session.execute('SELECT name, age, email FROM users')
for user_row in rows:
    print user_row.name, user_row.age, user_row.email

