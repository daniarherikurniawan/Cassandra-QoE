import numpy as np
import pandas as pd
import sys
import string


def get_rabbitmq_latency_data_ver1(priority_level, workload):
    # priority_level = 10
    # workload = 128

    filename_array = []
    latency_data = {}

    for levels in range(1, priority_level + 1):
        filename = 'rabbitmqdata/'
        filename = filename + 'workload_' + str(workload) + '_priority_' + str(levels) + '.txt'
        filename_array.append(filename)
        t_data = np.loadtxt(filename)
        latency_data[levels] = np.array(t_data)

    return latency_data


def get_rabbitmq_fifo_latency_data_ver1(workload):

    # priority_level = 10
    # workload = 128
    filename = 'rabbitmqdata/workload_' + str(workload) + '_fifo.txt'

    latency_data = {}
    t_data = np.loadtxt(filename)
    latency_data[0] = np.array(t_data)

    return latency_data


def get_rabbitmq_latency_data(priority_level, workload):

    # priority_level = 10
    # workload = 128

    filename_array = []
    latency_data = {}

    for levels in range(1, priority_level + 1):
        latency_data[levels] = []
        for pris in range( (levels-1)*1+1, levels*1+1):
            filename = 'rabbitmqdata/'
            filename = filename + 'workload_' + str(workload) + '_priority_' + str(pris) + '.txt'
            filename_array.append(filename)
            t_data = np.loadtxt(filename)
            latency_data[levels].extend(t_data)

    return latency_data


def get_rabbitmq_fifo_latency_data(workload):

    # priority_level = 10
    # workload = 128
    filename = 'rabbitmqdata/workload_' + str(workload) + '_fifo.txt'

    latency_data = {}
    t_data = np.loadtxt(filename)
    latency_data[0] = np.array(t_data)

    return latency_data

