from cassandra.cluster import Cluster

import subprocess
 
p = subprocess.Popen("scripts/getIP.sh", stdout=subprocess.PIPE, shell=True)
(IP, status) = p.communicate()

cluster = Cluster([str(IP)])
session = cluster.connect()
session.execute('USE test')

rows = session.execute('SELECT emp_name, emp_city, emp_phone FROM emp')
for user_row in rows:
    print user_row.emp_name, user_row.emp_city, user_row.emp_phone

