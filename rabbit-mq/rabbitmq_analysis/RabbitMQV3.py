import pandas as pd
import numpy as np
import bipartitegraph as bipart
import time
import random
import getSession as gs
import math
import load_rabbitlatency as lrabbit
import priority_latency as pl

'''
Third version of Priority Selection: Get per-request latency - FIFO/SLOPE/MATCH
'''

max_priority = 100
qoe_curve_filename = 'qoe_bins'

file = 'AM_12'
ori_data_original = pd.read_csv('data_hourly/' + file)
ori_data_original = bipart.filterData(ori_data_original)

# pages = ['SearchResults', 'Apps/Games PDP', 'PDP', 'SFW Category Page Template', 'RefineList']
pagetype = 'Apps/Games PDP' # note that we also need to modify this in biparititegraph.py.

r_times = 80

repeat_times = 15
exp_times = 30

classify_num = 400
max_sample_num = 10000

def get_expected_qoe(qoecurve, latencycurve, priority_level, nbk_latency):

    expected_qoe = 0.0
    # for times in range(0, repeat_times):
    #     bk_latency = rpl.replica_latency_random(workload, lccurve) #bk_latency = rpl.replica_latency_avg(workload, lccurve)
    #     expected_qoe += gs.QoECurve(bk_latency + nbk_latency, qoe_curve)

    bk_latency = pl.get_average(priority_level=priority_level, load_data=latencycurve)
    expected_qoe += gs.QoECurve(bk_latency + nbk_latency, qoecurve)

    return expected_qoe


def get_pri_slope(cluster_table, nbk):
    pri_level = 0

    min_distance = 200000000

    for i in range(0, len(cluster_table)):
        if abs(nbk - cluster_table[i]) < min_distance:
            min_distance = abs(nbk - cluster_table[i])
            pri_level = int(math.floor(i/4))

    return pri_level+1

def GreedySLOPE(make_table_data, nbk_delay, qoecurve, latencycurve):

    make_table_data_copy = make_table_data.copy()
    make_table_data_copy.sort(key = lambda ele: gs.QoESlope(ele, qoe_curve), reverse = True)

    answer_qoe = 0.0

    for i in range(0, len(nbk_delay)):
        bk_priority = get_pri_slope(make_table_data_copy, nbk_delay[i])
        bk_delay = pl.get_random(bk_priority, latencycurve)
        answer_qoe += gs.QoECurve(nbk_delay[i] + bk_delay, qoecurve)

    # print('answer_qoe:', answer_qoe)
    return answer_qoe


def get_pri_level(match_table, make_t_data, priority_y, nbk):
    pri_level = 0
    min_distance = 200000000

    for i in range(0, len(make_t_data)):
        if abs(make_t_data[i] - nbk) < min_distance:
            pri_level = priority_y[match_table[i]]
            min_distance = abs(make_t_data[i] - nbk)

    return pri_level

def cal_real_qoe(match_table, make_table_data, nb_delay, priority_y, qoe_curve, priority_curve):

    answer_qoe_optimal = 0.0

    task_num = len(nb_delay)

    for i in range(0, task_num):
        pri_level = get_pri_level(match_table, make_table_data, priority_y, nb_delay[i])
        b_delay = pl.get_random(priority_level=pri_level, load_data=priority_curve)
        answer_qoe_optimal += gs.QoECurve(nb_delay[i] + b_delay, qoe_curve)

    return answer_qoe_optimal


def make_graph(qoe_curve, priority_curve, nbk_delay):

    random.seed(time.time())

    workload = len(nbk_delay)

    normal_bin_size = int(math.floor(workload / max_priority))
    last_bin_size = workload - normal_bin_size * (max_priority - 1)
    priority_y = []
    for priority in range(2, max_priority+1):
        for priority_size in range(0, normal_bin_size):
            priority_y.append(priority)
    for priority_size in range(0, last_bin_size):
        priority_y.append(1)

    priority_y.sort()

    task_num = workload

    w = []

    for i in range(0, task_num):
        w.append([])
        for j in range(0, task_num):
            w[i].append(0.0)

    for i in range(0, task_num):
        for j in range(0, task_num):
            w[i][j] = get_expected_qoe(qoecurve=qoe_curve, latencycurve=priority_curve, priority_level = priority_y[j], nbk_latency=nbk_delay[i])

    match_table, answer_qoe_optimal = bipart.bipartite_graph(w)

    return match_table, priority_y


def fifo_cal_qoe(ori_data, qoecurve, fifocurve):

    answer_qoe = 0.0

    for rr in range(0, r_times):
        for index, row in ori_data.iterrows():
            nbd = row['non_backend']
            bd = pl.get_random(0, fifocurve)
            answer_qoe += gs.QoECurve(nbd+bd, qoecurve)

    answer_qoe = answer_qoe/r_times
    return answer_qoe

def classify_data(ori_data):

    nb_delay = []
    for index, row in ori_data.iterrows():
        nb_delay.append(row['non_backend'])
    nb_delay.sort()

    num_in_class = int(max_sample_num/classify_num)
    cluster_median = []
    for cluster in range(0, classify_num):
        cluster_total = 0.0
        for index in range(cluster * num_in_class, (cluster +1) * num_in_class):
            cluster_total += nb_delay[index]

        cluster_median.append(cluster_total/num_in_class)

    return cluster_median


if __name__ == '__main__':

    print('This is the second version of RabbitMQ priority assignment.')

    qoe_curve = bipart.getcurve(qoe_curve_filename)

    #workloads =[90, 110, 120, 125, 126, 127, 128, 129, 130]
    #workloads = [90, 95, 100, 105, 110, 115, 118, 119, 120]
    # workloads = [120, 125, 128, 129, 130]
    workloads = [90, 95, 100, 105, 110, 115, 120]
    for workload in workloads:

        print('------------------------------')
        print('Start Workload', workload)
        latencydata_priority = lrabbit.get_rabbitmq_latency_data(max_priority, workload)
        latencydata_fifo = lrabbit.get_rabbitmq_fifo_latency_data(workload)

        ori_data_classify_sample = ori_data_original.sample(n = max_sample_num, random_state=int(time.time()), axis=0)

        make_table_data = classify_data(ori_data_classify_sample)
        table_match, priority_table = make_graph(qoe_curve=qoe_curve, priority_curve=latencydata_priority, nbk_delay = make_table_data)

        match_qoe = 0.0
        slope_qoe = 0.0
        fifo_qoe = 0.0

        workload = workload + 200

        for exp_num in range(0, exp_times):

            ori_data = ori_data_original.sample(n = workload, random_state=int(time.time()), axis=0)
            fifo_qoe += fifo_cal_qoe(ori_data, qoe_curve, latencydata_fifo)

            nb_delay = []
            for index, row in ori_data.iterrows():
                nb_delay.append(row['non_backend'])

            t_qoe_slope = 0.0
            t_qoe_match = 0.0
            for rrr in range(0, r_times):
                t_qoe_match += cal_real_qoe(match_table=table_match, make_table_data = make_table_data, nb_delay=nb_delay, priority_y=priority_table, priority_curve=latencydata_priority, qoe_curve=qoe_curve)
                t_qoe_slope += GreedySLOPE(make_table_data = make_table_data, nbk_delay=nb_delay, latencycurve=latencydata_priority, qoecurve=qoe_curve)
            t_qoe_slope = t_qoe_slope/r_times
            t_qoe_match = t_qoe_match/r_times
            match_qoe += t_qoe_match
            slope_qoe += t_qoe_slope

        # print('Throughput:', workload, 'rps')
        print('FIFO:', fifo_qoe, 'Slope:', slope_qoe, 'Match:', match_qoe)
        print('Slope Gain:', slope_qoe/fifo_qoe -1, 'Match Gain:', match_qoe/fifo_qoe -1)


