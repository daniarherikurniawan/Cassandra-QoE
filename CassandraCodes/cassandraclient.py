import xmlrpc.client
# for python 2.7 import xmlrpclib
from cassandra.cluster import Cluster
import uuid
import subprocess
from faker import Faker

import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import timedelta
from datetime import datetime
import time
import math
import string
import random

fake = Faker()

IP = ['cass-1.CassandraTest.DeepEdgeVideo.emulab.net', 'cass-2.CassandraTest.DeepEdgeVideo.emulab.net', 'cass-3.CassandraTest.DeepEdgeVideo.emulab.net']
clusters = [Cluster([str(IP[0])]), Cluster([str(IP[1])]), Cluster([str(IP[2])])]
sessions = [clusters[0].connect(), clusters[1].connect(), clusters[2].connect()]

'''
For debug, just use only 1 replica
'''
clusters = [Cluster([str(IP[0])])]
sessions = [clusters[0].connect()]
'''
For debug, just use only 1 replica
'''

id_list = []

def get_id_list():

    df = pd.read_csvshelkslkjsfasf
    return 0

def sys_main():
    for session in sessions:
        session.execute('USE ycsb')

    get_id_list()
    return 0


if __name__ == '__main__':
    print('Cassandra Client Start')
    sys_main()
